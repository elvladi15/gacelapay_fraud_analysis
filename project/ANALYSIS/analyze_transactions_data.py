import duckdb
from scipy.special import logit, expit
import project.utils
import project.ANALYSIS.features as features
import pandas as pd
import math
import multiprocessing as mp
import time
from pathlib import Path
from project.utils import generate_csv_file_from_df

joined_tables_for_analysis = duckdb.sql(open('project/SQL/JOIN_ALL_TABLES_FOR_ANALYSIS.sql', 'r').read()).df()

column_order = [
	'FRAUD_ANALYSIS_ID',
	'THRESHOLD',
	'FALSE_POSITIVE_RATE',
	'GRAND_TOTAL',
	'FRAUD_DETECTION_RATE',
	'PRECISION',
	'ACCURACY',
	'TOTAL_USD_FEES',
	'TOTAL_FRAUD_LOSS',
	'TOTAL_INVESTIGATION_COST',
	'TOTAL_CUSTOMER_SUPPORT_COST',
	'TOTAL_LOST_INTERCHANGE'
]

class Runner:
	def __init__(self, file_name, is_base_case):
		self.file_name = file_name
		self.is_base_case = is_base_case

	def create_test_cases_csv(self):
		df = pd.DataFrame(columns=column_order)

		df.to_csv(self.file_name, index=False)

		with mp.Pool(mp.cpu_count()) as pool:
			pool.map(self.append_test_case_to_csv, [700] if self.is_base_case else features.thresholds_list)

	def sort_generated_file(self):
		try:
			sorted_df = pd.read_csv(self.file_name)

			sorted_df = sorted_df.sort_values(by=['FALSE_POSITIVE_RATE', 'GRAND_TOTAL'], ascending=[True, False])

			sorted_df.to_csv(self.file_name, index=False)

			print(f'\tFile: {self.file_name} generated.')
		except Exception as e:
			print('\tError while sorting the file. Undergo manual review.')
			print(f'\tError message: {e}')

	def append_test_case_to_csv(self, threshold):
		test_case_transactions_df = get_test_case_transactions_df(threshold, self.is_base_case)

		fraud_statistics_df = duckdb.sql(open('project/SQL/GET_FRAUD_STATISTICS.sql', 'r').read()).df()

		fraud_statistics_df.at[0, 'THRESHOLD'] = threshold

		fraud_statistics_df = fraud_statistics_df.reindex(columns=column_order)

		fraud_statistics_df.to_csv(self.file_name, mode='a', index=False, header=False)

	@classmethod
	def run_many(cls, configs):
		for file_name, is_base_case in configs:
			cls(file_name, is_base_case).create_test_cases_csv()
			cls(file_name, is_base_case).sort_generated_file()

def get_test_case_transactions_df(threshold, is_base_case):
	threshold_probability = threshold / 1000

	for row in joined_tables_for_analysis.itertuples():
		ml_probability = joined_tables_for_analysis.at[row.Index, 'ML_PROBABILITY']

		logit_value = logit(ml_probability)

		for feature in features.features_list:
			parameter_list = []

			for column_name in feature['columns']:
				parameter_list.append(joined_tables_for_analysis.at[row.Index, column_name])

			weight = 0 if is_base_case else feature['function'](*parameter_list)

			logit_value += weight

		joined_tables_for_analysis.at[row.Index, 'FLAGGED'] = 1 if expit(logit_value) >= threshold_probability else 0

	sql_file = Path('project/SQL/TEST_CASE_RESULTS.sql')

	sql_query = open(sql_file, 'r').read()

	return duckdb.sql(sql_query).df()

def generate_compare_test_cases_csv():
	test_case_1 = pd.read_csv('project/ANALYSIS/FRAUD_STATISTICS_BASE_TEST_CASE.csv')
	test_case_2 = pd.read_csv('project/ANALYSIS/FRAUD_STATISTICS.csv').head(1)

	sql_file = Path('project/SQL/COMPARE_TEST_CASES.sql')

	sql_query = open(sql_file, 'r').read()

	duckdb.sql(sql_query).df().to_csv('project/ANALYSIS/COMPARE_TEST_CASES.csv', index = False, encoding='utf-8-sig')
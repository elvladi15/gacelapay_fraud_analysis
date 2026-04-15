import duckdb
from scipy.special import logit, expit
import project.utils
import project.ANALYSIS.features as features
import pandas as pd
import math
import multiprocessing as mp
import time
from pathlib import Path
from project.utils import generate_csv_file_from_sql

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

weight_columns = []

for i in range(len(features.features_list)):
	weight_columns.append(f'W{i + 1}')

column_order[2:2] = weight_columns

class Runner:
	def __init__(self, file_name, test_cases):
		self.file_name = file_name
		self.test_cases = test_cases
		self.start_time = time.time()

	def create_test_cases_csv(self):
		df = pd.DataFrame(columns=column_order)

		df.to_csv(self.file_name, index=False)

		with mp.Pool(mp.cpu_count()) as pool:
			pool.map(self.append_test_case_to_csv, self.test_cases)

	def sort_generated_file(self):
		try:
			sorted_df = pd.read_csv(self.file_name)

			sorted_df = sorted_df.sort_values(by=['FALSE_POSITIVE_RATE', 'GRAND_TOTAL'], ascending=[True, False])

			sorted_df.to_csv(self.file_name, index=False)

			print(f'Total time taken to generate and order the file: {self.file_name}: {time.time() - self.start_time:.2f} seconds.')
		except Exception as e:
			print('Error while sorting the file. Undergo manual review.')
			print(f'Error message: {e}')

	def append_test_case_to_csv(self, test_case):
		weights = test_case['weight_list']
		threshold = test_case['threshold']

		test_case_transactions_df = get_test_case_transactions_df(test_case)

		fraud_statistics_df = duckdb.sql(open('project/SQL/GET_FRAUD_STATISTICS.sql', 'r').read()).df()

		for index in range(len(features.features_list)):
			fraud_statistics_df.at[0, f'W{index + 1}'] = weights[index]

		fraud_statistics_df.at[0, 'THRESHOLD'] = threshold

		fraud_statistics_df = fraud_statistics_df.reindex(columns=column_order)

		fraud_statistics_df.to_csv(self.file_name, mode='a', index=False, header=False)

	@classmethod
	def run_many(cls, configs):
		for file_name, test_cases in configs:
			cls(file_name, test_cases).create_test_cases_csv()
			cls(file_name, test_cases).sort_generated_file()

def get_test_case_transactions_df(test_case):
	weights = test_case['weight_list']
	threshold = test_case['threshold']

	threshold_probability = threshold / 1000

	joined_tables_for_analysis = duckdb.sql(open('project/SQL/JOIN_ALL_TABLES_FOR_ANALYSIS.sql', 'r').read()).df()

	for row in joined_tables_for_analysis.itertuples():
		ml_probability = joined_tables_for_analysis.at[row.Index, 'ML_PROBABILITY']

		logit_value = logit(ml_probability)

		for index, feature in enumerate(features.features_list):
			parameter_list = []

			for column_name in feature['columns']:
				parameter_list.append(joined_tables_for_analysis.at[row.Index, column_name])

			condition_met = feature['function'](*parameter_list)

			if condition_met:
				logit_value += weights[index]

		joined_tables_for_analysis.at[row.Index, 'FLAGGED'] = 1 if expit(logit_value) >= threshold_probability else 0

	sql_file = Path('project/SQL/TEST_CASE_RESULTS.sql')

	sql_query = open(sql_file, 'r').read()

	return duckdb.sql(sql_query).df()

def get_test_cases(weight_parameters, threshold_parameters):
		test_case_parameters = []
		weight_list = []

		for weight_parameter in weight_parameters:
			weight_list.append(get_weights_list_for_parameter(weight_parameter))

		threshold_list = get_weights_list_for_parameter(threshold_parameters)

		weight_list.append(threshold_list)

		total_cases_quantity = 1
		list_weights_for_iteration = []

		for list in weight_list:
			total_cases_quantity *= len(list)

		weight = total_cases_quantity

		for list in weight_list:
			weight /= len(list)

			list_weights_for_iteration.append(weight)

		for i in range(total_cases_quantity):
			index_list = []

			remnant = i

			for weight in list_weights_for_iteration:
				index = math.floor(remnant /weight)

				index_list.append(index)

				remnant -= index * weight

			final_weight_list = []

			for index, item in enumerate(index_list[:-1]):
				final_weight_list.append(weight_list[index][item])

			final_threshold = threshold_list[index_list[-1]]

			test_case_parameters.append({'weight_list': final_weight_list, 'threshold': final_threshold})

		return test_case_parameters

def get_weights_list_for_parameter(weight_details):
		output_list = []
		for i in range(2 * weight_details['quantity'] + 1):
			output_list.append(round((i - weight_details['quantity']) * weight_details['steps'] + weight_details['value'], 4))

		return output_list

def compare_test_cases():
	test_case_1 = pd.read_csv('project/ANALYSIS/FRAUD_STATISTICS_BASE_TEST_CASE.csv')
	test_case_2 = pd.read_csv('project/ANALYSIS/FRAUD_STATISTICS.csv').head(1)

	sql_file = Path('project/SQL/COMPARE_TEST_CASES.sql')

	sql_query = open(sql_file, 'r').read()

	duckdb.sql(sql_query).df().to_csv('project/ANALYSIS/COMPARE_TEST_CASES.csv', index = False, encoding='utf-8-sig')

	print('Parameters of the best test case execution:')

	for column in test_case_2.columns:
		if(len(column) == 2 and column[0] == 'W'):
			print(f'{column}: {test_case_2[column][0]}')

	print(f'THRESHOLD: {test_case_2['THRESHOLD'][0]}')
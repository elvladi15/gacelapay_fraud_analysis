import duckdb
from scipy.special import logit, expit
import project.utils
import project.ANALYSIS.features as features
import pandas as pd
import math
import multiprocessing as mp
import time
from pathlib import Path

global_file_name = ''

column_order = [
		'FRAUD_ANALYSIS_ID',
		'W1',
		'W2',
		'W3',
		'THRESHOLD',
		'FALSE_POSITIVE_RATE',
		'GRAND_TOTAL',
		'FRAUD_DETECTION_RATE',
		'PRECISION',
		'ACCURACY',
		'USD_FEES',
		'TOTAL_FRAUD_LOSS',
		'TOTAL_INVESTIGATION_COST',
		'TOTAL_CUSTOMER_SUPPORT_COST',
		'TOTAL_LOST_INTERCHANGE'
]

def get_test_case_transactions_df(test_case):
	weights = test_case['weight_list']
	threshold = test_case['threshold']

	threshold_probability = threshold / 1000

	joined_tables_for_analysis = duckdb.sql(open('project/SQL/JOIN_ALL_TABLES_FOR_ANALYSIS.sql', 'r').read()).df()

	for row in joined_tables_for_analysis.itertuples():
		ml_probability = joined_tables_for_analysis.at[row.Index, 'ML_PROBABILITY']

		logit_value = logit(ml_probability)

		#feature 1
		if features.feature_1_test(joined_tables_for_analysis.at[row.Index, 'TIME']):
			logit_value += weights[0]

		#feature 2
		if features.feature_2_test(joined_tables_for_analysis.at[row.Index, 'CUSTOMER_COUNTRY']):
			logit_value += weights[1]

		#feature 3
		if features.feature_3_test(joined_tables_for_analysis.at[row.Index, 'TRANSACTION_USD_AMOUNT']):
			logit_value += weights[2]

		joined_tables_for_analysis.at[row.Index, 'FLAGGED'] = 1 if expit(logit_value) >= threshold_probability else 0

		#joined_tables_for_analysis = get_test_case_transactions_df({'weight_list': [-5.07343924, 2.4844875, 2.9017253], 'threshold': 850})

		sql_file = Path('project/SQL/TEST_CASE_RESULTS.sql')

		sql_query = open(sql_file, 'r').read()

		return duckdb.sql(sql_query).df()

def append_test_case_to_csv(test_case):
	weights = test_case['weight_list']
	threshold = test_case['threshold']

	test_case_transactions_df = get_test_case_transactions_df(test_case)

	fraud_statistics_df = duckdb.sql(open('project/SQL/GET_FRAUD_STATISTICS.sql', 'r').read()).df()

	fraud_statistics_df.at[0, 'W1'] = weights[0]
	fraud_statistics_df.at[0, 'W2'] = weights[1]
	fraud_statistics_df.at[0, 'W3'] = weights[2]

	fraud_statistics_df.at[0, 'THRESHOLD'] = threshold

	fraud_statistics_df = fraud_statistics_df.reindex(columns=column_order)

	fraud_statistics_df.to_csv(global_file_name, mode='a', index=False, header=False)

def get_weights_list_for_parameter(weight_details):
	output_list = []
	for i in range(2 * weight_details['quantity'] + 1):
		output_list.append(round((i - weight_details['quantity']) * weight_details['steps'] + weight_details['value'], 4))
	
	return output_list

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

def create_test_cases_csv(file_name, test_cases):
	global global_file_name

	global_file_name = file_name

	if __name__ == '__main__':
		df = pd.DataFrame(columns=column_order)
		
		df.to_csv(file_name, index=False)
		
		with mp.Pool(mp.cpu_count()) as pool:
			start_time = time.time()
			pool.map(append_test_case_to_csv, test_cases)
		
		sorted_df = pd.read_csv(file_name)

		sorted_df = sorted_df.sort_values(by=['FALSE_POSITIVE_RATE', 'GRAND_TOTAL'], ascending=[True, False])

		sorted_df.to_csv(file_name, index=False)

		print(f'Total time taken to generate file: {global_file_name}: {time.time() - start_time:.2f} seconds.')

weight_parameters = [
	{
		'value': -6.5734,
		'steps': 0.5,
		'quantity': 3
	},
	{
		'value': 1.9844,
		'steps': 0.5,
		'quantity': 3
	},
	{
		'value': 2.9017,
		'steps': 0.5,
		'quantity': 3
	},
]

threshold_parameters = {
	'value': 700,
	'steps': 50,
	'quantity': 3
}

create_test_cases_csv('project/ANALYSIS/FRAUD_STATISTICS_BASE_CASE.csv', [{'weight_list': [0, 0, 0], 'threshold': 700}])
#create_test_cases_csv('project/ANALYSIS/FRAUD_STATISTICS.csv', get_test_cases(weight_parameters, threshold_parameters))

#print(get_test_case_transactions_df({'weight_list': [-5.07343924, 2.4844875, 2.9017253], 'threshold': 850}))
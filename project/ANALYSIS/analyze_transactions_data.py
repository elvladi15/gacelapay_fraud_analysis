import duckdb
from scipy.special import logit, expit
import project.utils
import pandas as pd
import math
import multiprocessing as mp
import time

file_name = 'project/ANALYSIS/FRAUD_STATISTICS.csv'

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

def get_transaction_statistics_df(weights, threshold):
	threshold_probability = threshold / 1000

	joined_tables_for_analysis = duckdb.sql(open('project/SQL/JOIN_ALL_TABLES_FOR_ANALYSIS.sql', 'r').read()).df()

	if weights != None:
		for row in joined_tables_for_analysis.itertuples():
			ml_probability = joined_tables_for_analysis.at[row.Index, 'ML_PROBABILITY']

			logit_value = logit(ml_probability)

			 #feature 1
			if joined_tables_for_analysis.at[row.Index, 'TIME'] > '23:00:00':
				logit_value += weights[0]

			 #feature 2
			if joined_tables_for_analysis.at[row.Index, 'CUSTOMER_COUNTRY'] == 'Brazil':
				logit_value += weights[1]

			 #feature 3
			if joined_tables_for_analysis.at[row.Index, 'TRANSACTION_USD_AMOUNT'] > 10000:
				logit_value += weights[2]

			joined_tables_for_analysis.at[row.Index, 'FLAGGED'] = 1 if expit(logit_value) >= threshold_probability else 0

	fraud_statistics_df = duckdb.sql(open('project/SQL/GET_FRAUD_STATISTICS.sql', 'r').read()).df()

	fraud_statistics_df.at[0, 'W1'] = weights[0]
	fraud_statistics_df.at[0, 'W2'] = weights[1]
	fraud_statistics_df.at[0, 'W3'] = weights[2]
	fraud_statistics_df.at[0, 'THRESHOLD'] = threshold

	fraud_statistics_df = fraud_statistics_df.reindex(columns=column_order)

	return fraud_statistics_df

def get_weights_list_for_parameter(weight_details):
	output_list = []
	for i in range(2 * weight_details['quantity'] + 1):
		output_list.append((i - weight_details['quantity']) * weight_details['steps'] + weight_details['value'])
	
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

		list_weights_for_iteration.append({'count': len(list), 'weight': weight})

	for i in range(total_cases_quantity):
		index_list = []
		
		remnant = i

		for item in list_weights_for_iteration:
			index = math.floor(remnant /item['weight'])

			index_list.append(index)

			remnant -= index * item['weight']
		
		final_weight_list = []

		for index, item in enumerate(index_list[:-1]):
			final_weight_list.append(weight_list[index][item])

		final_threshold = threshold_list[index_list[-1]]

		test_case_parameters.append({'weight_list': final_weight_list, 'threshold': final_threshold})

	return test_case_parameters

def append_test_case_to_csv(test_case):
	df = get_transaction_statistics_df(test_case['weight_list'], test_case['threshold'])

	df.to_csv(file_name, mode='a', index=False, header=False)

if __name__ == "__main__":
	start_time = time.time()
	
	weight_parameters = [
		{
			'value': -6.57343924,
			'steps': 0.5,
			'quantity': 3
		},
		{
			'value': 1.9844875,
			'steps': 0.5,
			'quantity': 3
		},
		{
			'value': 2.9017253,
			'steps': 0.5,
			'quantity': 3
		},
	]

	threshold_parameters = {
		'value': 700,
		'steps': 50,
		'quantity': 3
	}

	df = pd.DataFrame(columns=column_order)
	
	df.to_csv(file_name, index=False)
	
	with mp.Pool(mp.cpu_count()) as pool:
		test_cases = get_test_cases(weight_parameters, threshold_parameters)

		print(len(test_cases))
		
		pool.map(append_test_case_to_csv, test_cases)
	
	sorted_df = pd.read_csv(file_name)

	sorted_df = sorted_df.sort_values(by=['FALSE_POSITIVE_RATE', 'GRAND_TOTAL'], ascending=[True, False])

	sorted_df.to_csv(file_name, index=False)

	print(f'Total time taken: {time.time() - start_time:.2f} seconds.')
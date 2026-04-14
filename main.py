from project.utils import generate_csv_file_from_sql
from project.ANALYSIS.analyze_transactions_data import Runner, get_test_cases, compare_test_cases

if __name__ == '__main__':
	#STEP 1: CLEAN DATASETS

	generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_EXCHANGE_RATES.sql', 'project/CLEAN_DATASETS/CLEAN_COMBINED_EXCHANGE_RATES.csv')
	print('file: CLEAN_COMBINED_EXCHANGE_RATES.csv created.')

	generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_ACCOUNTS.sql', 'project/CLEAN_DATASETS/ACCOUNTS.csv')
	print('file: ACCOUNTS.csv created.')

	generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_CUSTOMERS.sql', 'project/CLEAN_DATASETS/CUSTOMERS.csv')
	print('file: CUSTOMERS.csv created.')

	generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_DECISIONS.sql', 'project/CLEAN_DATASETS/FRAUD_DECISIONS.csv')
	print('file: FRAUD_DECISIONS.csv created.')

	generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_TRANSACTIONS.sql', 'project/CLEAN_DATASETS/TRANSACTIONS.csv')
	print('file: TRANSACTIONS.csv created.')

	generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_COSTS.sql', 'project/CLEAN_DATASETS/FRAUD_COSTS.csv')
	print('file: FRAUD_COSTS.csv created.')

	#STEP 2: DENORMALIZE TRANSACTIONS TO MAKE THEM EASIER TO ANALYZE

	generate_csv_file_from_sql('project/SQL/DENORMALIZE_TRANSACTIONS.sql', 'project/ANALYSIS/DENORMALIZED_TRANSACTIONS.csv')
	print('file: DENORMALIZED_TRANSACTIONS.csv created.')

	#STEP 3: CREATE THE BASE CASE FRAUD STATISTICS CSV AND THE TEST CASES CSV, BASED ON THE FEATURES AND WEIGHT
	# PARAMETERS PASSED TO EACH FEATURE TO DETERMINE THE BEST CASE SCENARIO AND ITS PARAMETERS, AND COMPARE IT TO THE
	# BASE CASE TO SEE IMPROVEMENTS

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

	test_cases = get_test_cases(weight_parameters, threshold_parameters)

	base_test_case = {'weight_list': [0, 0, 0], 'threshold': 700}

	Runner.run_many(
		[
			('project/ANALYSIS/FRAUD_STATISTICS_BASE_TEST_CASE.csv', [base_test_case]),
			('project/ANALYSIS/FRAUD_STATISTICS.csv', test_cases)
		]
	)

	compare_test_cases()
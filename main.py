from project.utils import generate_df_from_sql, generate_csv_file_from_df
from project.ANALYSIS.analyze_transactions_data import Runner, get_test_cases, compare_test_cases
from project.ANALYSIS.calculate_IV_per_column import get_IV_for_columns_df, get_combined_column_stats_df

if __name__ == '__main__':
	#STEP 1: CLEAN DATASETS

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_EXCHANGE_RATES.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/CLEAN_COMBINED_EXCHANGE_RATES.csv')
	print('file: CLEAN_COMBINED_EXCHANGE_RATES.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_ACCOUNTS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/ACCOUNTS.csv')
	print('file: ACCOUNTS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_CUSTOMERS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/CUSTOMERS.csv')
	print('file: CUSTOMERS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_DECISIONS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/FRAUD_DECISIONS.csv')
	print('file: FRAUD_DECISIONS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_TRANSACTIONS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/TRANSACTIONS.csv')
	print('file: TRANSACTIONS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_COSTS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/FRAUD_COSTS.csv')
	print('file: FRAUD_COSTS.csv created.')

	#STEP 2: DENORMALIZE TRANSACTIONS TO MAKE THEM EASIER TO ANALYZE

	df = generate_df_from_sql('project/SQL/DENORMALIZE_TRANSACTIONS.sql')
	generate_csv_file_from_df(df, 'project/ANALYSIS/DENORMALIZED_TRANSACTIONS.csv')
	print('file: DENORMALIZED_TRANSACTIONS.csv created.')

	# STEP 3: GET INFORMATION VALUE FOR EACH INDIVIDUAL COLUMNS (NO INTERACTION YET)

	all_ivs_df = get_IV_for_columns_df(2)

	single_column_ivs_df = all_ivs_df[all_ivs_df['IDS'].str.split(',').str.len() == 1]

	generate_csv_file_from_df(single_column_ivs_df, 'project/ANALYSIS/SINGLE_COLUMN_IVS.csv')

	# STEP 4: GET INFORMATION VALUE FOR N COLUMN INTERACTIONS TO KNOW WHICH COMBINATIONS ARE MORE EFFECTIVE AT DETECTING FRAUD

	combined_column_stats = get_combined_column_stats_df(all_ivs_df)

	generate_csv_file_from_df(combined_column_stats, 'project/ANALYSIS/COMBINED_COLUMN_STATS.csv')

	#STEP 5: CREATE THE BASE CASE FRAUD STATISTICS CSV AND THE TEST CASES CSV, BASED ON THE FEATURES AND WEIGHT
	# PARAMETERS PASSED TO EACH FEATURE TO DETERMINE THE BEST CASE SCENARIO AND ITS PARAMETERS, AND COMPARE IT TO THE
	# BASE CASE TO SEE IMPROVEMENTS

	test_cases = get_test_cases()

	base_test_case = {'weight_list': [0, 0, 0], 'threshold': 700}

	Runner.run_many(
		[
			('project/ANALYSIS/FRAUD_STATISTICS_BASE_TEST_CASE.csv', True),
			('project/ANALYSIS/FRAUD_STATISTICS.csv', False)
		]
	)

	compare_test_cases()
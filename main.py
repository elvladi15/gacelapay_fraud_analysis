import pandas as pd
from project.utils import generate_df_from_sql, generate_csv_file_from_df
from project.ANALYSIS.analyze_transactions_data import Runner, generate_compare_test_cases_csv
from project.ANALYSIS.calculate_IV_per_column import get_IV_for_columns_df, get_combined_column_stats_df
from project.ANALYSIS.calculate_bucket_weights import get_bucket_weights_df
from project.ANALYSIS.plot_results import get_test_case_transactions_df, plot_line_chart_for_statistic_comparison, generate_confusion_matrix, MY_BLUE_COLOR

threshold = 845

if __name__ == '__main__':
	#STEP 1: CLEAN DATASETS
	print('STEP 1: CLEAN DATASETS')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_EXCHANGE_RATES.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/CLEAN_COMBINED_EXCHANGE_RATES.csv')
	print('\tFile: CLEAN_COMBINED_EXCHANGE_RATES.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_ACCOUNTS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/ACCOUNTS.csv')
	print('\tFile: ACCOUNTS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_CUSTOMERS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/CUSTOMERS.csv')
	print('\tFile: CUSTOMERS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_DECISIONS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/FRAUD_DECISIONS.csv')
	print('\tFile: FRAUD_DECISIONS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_TRANSACTIONS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/TRANSACTIONS.csv')
	print('\tFile: TRANSACTIONS.csv created.')

	df = generate_df_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_COSTS.sql')
	generate_csv_file_from_df(df, 'project/CLEAN_DATASETS/FRAUD_COSTS.csv')
	print('\tFile: FRAUD_COSTS.csv created.')

	#STEP 2: DENORMALIZE TRANSACTIONS TO MAKE THEM EASIER TO ANALYZE
	print('\nSTEP 2: DENORMALIZE TRANSACTIONS TO MAKE THEM EASIER TO ANALYZE')

	df = generate_df_from_sql('project/SQL/DENORMALIZE_TRANSACTIONS.sql')
	generate_csv_file_from_df(df, 'project/ANALYSIS/DENORMALIZED_TRANSACTIONS.csv')
	print('\tFile: DENORMALIZED_TRANSACTIONS.csv created.')

	# STEP 3: GET INFORMATION VALUE FOR EACH INDIVIDUAL COLUMNS (NO INTERACTION YET)
	print('\nSTEP 3: GET INFORMATION VALUE FOR EACH INDIVIDUAL COLUMNS (NO INTERACTION YET)')

	all_ivs_df = get_IV_for_columns_df(2, None)

	single_column_ivs_df = all_ivs_df[all_ivs_df['IDS'].str.split(',').str.len() == 1]

	generate_csv_file_from_df(single_column_ivs_df, 'project/ANALYSIS/SINGLE_COLUMN_IVS.csv')
	print('\tFile: SINGLE_COLUMN_IVS.csv generated.')

	# STEP 4: GET INFORMATION VALUE FOR N COLUMN INTERACTIONS TO KNOW WHICH COMBINATIONS ARE MORE EFFECTIVE AT DETECTING FRAUD
	print('\nSTEP 4: GET INFORMATION VALUE FOR N COLUMN INTERACTIONS TO KNOW WHICH COMBINATIONS ARE MORE EFFECTIVE AT DETECTING FRAUD')

	combined_column_stats = get_combined_column_stats_df(all_ivs_df)

	generate_csv_file_from_df(combined_column_stats, 'project/ANALYSIS/COMBINED_COLUMN_STATS.csv')
	print('\tFile: COMBINED_COLUMN_STATS.csv generated.')

	#STEP 5: GENERATE CSV FILE WITH THE WEIGHTS TO BE USED
	print('\nSTEP 5: GENERATE CSV FILE WITH THE WEIGHTS TO BE USED')

	generate_csv_file_from_df(get_bucket_weights_df(), 'project/ANALYSIS/WEIGHTS.csv')
	print('\tFile: WEIGHTS.csv generated.')

	#STEP 6: CREATE THE BASE CASE FRAUD STATISTICS CSV AND THE TEST CASES CSV, BASED ON THE FEATURES AND WEIGHT
	# PARAMETERS PASSED TO EACH FEATURE TO DETERMINE THE BEST CASE SCENARIO AND ITS PARAMETERS, AND COMPARE IT TO THE
	# BASE CASE TO SEE IMPROVEMENTS
	print('''\nSTEP 6: CREATE THE BASE CASE FRAUD STATISTICS CSV AND THE TEST CASES CSV''')

	Runner.run_many(
		[
			('project/ANALYSIS/FRAUD_STATISTICS_BASE_TEST_CASE.csv', True),
			('project/ANALYSIS/FRAUD_STATISTICS.csv', False)
		]
	)

	base_test_case_results_df = pd.read_csv('project/ANALYSIS/FRAUD_STATISTICS_BASE_TEST_CASE.csv')

	best_test_case_results_df = pd.read_csv('project/ANALYSIS/FRAUD_STATISTICS.csv')
	best_test_case_results_df = best_test_case_results_df[best_test_case_results_df['THRESHOLD'] == threshold]
	
	generate_compare_test_cases_csv(base_test_case_results_df, best_test_case_results_df)

	print('\tFile: COMPARE_TEST_CASES.csv generated.')

	# STEP 7: GENERATE CHARTS

	print('STEP 7: GENERATE CHARTS')

	base_test_case_df = get_test_case_transactions_df(700, True)
	best_test_case_df = get_test_case_transactions_df(threshold, False)

	test_cases = [
		{
			'df': base_test_case_df,
			'label': 'BEFORE MODEL CHANGES',
			'color': '#ff7f0e',
			'linewidth': 2
		},
		{
			'df': best_test_case_df,
			'label': 'AFTER MODEL CHANGES',
			'color': MY_BLUE_COLOR,
			'linewidth': 4
		},
	]

	plot_line_chart_for_statistic_comparison(
		{
			'test_cases': [
				{
					'df': base_test_case_df,
					'label': 'BEFORE MODEL CHANGES',
					'color': MY_BLUE_COLOR,
					'linewidth': 4
				}
			],
			'kpi': 'FPR',
			'title': 'Steady increase on\nFalse Positive Rates over the last 4 years',
			'file_name': 'assets/current_fpr.png',
			'step_start': 0.0352,
			'step_end': 0.036,
			'step_value': 0.0002,
			'decimals': 2,
			'show_legend': False,
			'time_aggregation': 'Y',
			'time_step': 1,
			'y_axis_metric': 'percent'
		}
	)

	plot_line_chart_for_statistic_comparison(
		{
			'test_cases': test_cases,
			'kpi': 'FPR',
			'title': 'Improved False Positive Rates\nconsistently under 2%',
			'file_name': 'assets/fpr_comparison.png',
			'step_start': 0,
			'step_end': 0.04,
			'step_value': 0.01,
			'decimals': 0,
			'show_legend': True,
			'time_aggregation': 'M',
			'time_step': 12,
			'y_axis_metric': 'percent'
		}
	)

	plot_line_chart_for_statistic_comparison(
		{
			'test_cases': test_cases,
			'kpi': 'ACCURACY',
			'title': 'Accuracy',
			'file_name': 'assets/accuracy_comparison.png',
			'step_start': 0.94,
			'step_end': 0.99,
			'step_value': 0.02,
			'decimals': 0,
			'show_legend': True,
			'time_aggregation': 'M',
			'time_step': 12,
			'y_axis_metric': 'percent'
		}
	)

	plot_line_chart_for_statistic_comparison(
		{
			'test_cases': test_cases,
			'kpi': 'FDR',
			'title': 'FDR',
			'file_name': 'assets/fdr_comparison.png',
			'step_start': 0.2,
			'step_end': 1,
			'step_value': 0.2,
			'decimals': 0,
			'show_legend': True,
			'time_aggregation': 'M',
			'time_step': 12,
			'y_axis_metric': 'percent'
		}
	)

	plot_line_chart_for_statistic_comparison(
		{
			'test_cases': test_cases,
			'kpi': 'PRECISION',
			'title': 'Precision',
			'file_name': 'assets/precision_comparison.png',
			'step_start': 0.2,
			'step_end': 0.8,
			'step_value': 0.2,
			'decimals': 0,
			'show_legend': True,
			'time_aggregation': 'M',
			'time_step': 12,
			'y_axis_metric': 'percent'
		}
	)

	generate_confusion_matrix(base_test_case_df, 'Large amount of FP and FN', 'assets/current_confusion_matrix.png')
	generate_confusion_matrix(best_test_case_df, 'After model adjustments', 'assets/after_model_adjustments_confusion_matrix.png')

	print('\tAll charts have been generated.')
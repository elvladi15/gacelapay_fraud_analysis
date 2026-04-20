from project.ANALYSIS.analyze_transactions_data import joined_tables_for_analysis
import duckdb
import math
import pandas as pd

LAPLACE_SMOOTHING = 0.5

total_fraud, total_transactions = duckdb.sql('SELECT SUM(IS_FRAUD), COUNT(*) FROM joined_tables_for_analysis').fetchone()

total_non_fraud = total_transactions - total_fraud

def get_default_bucket_query(column):
	return f'''
		SELECT
			{column}		AS '{column}',
			SUM(IS_FRAUD)	AS IS_FRAUD_QUANTITY,
			COUNT(*)		AS TRANSACTION_QUANTITY
		FROM
			joined_tables_for_analysis
		GROUP BY
			{column};
	'''

def calculate_weight_of_evidence_and_percents(is_fraud_quantity, transaction_quantity):
	percent_fraud = (is_fraud_quantity + LAPLACE_SMOOTHING) / total_fraud

	non_fraud_quantity = transaction_quantity - is_fraud_quantity + LAPLACE_SMOOTHING

	percent_non_fraud = non_fraud_quantity / total_non_fraud

	WoE = round(math.log(percent_fraud / percent_non_fraud), 4)

	return WoE, percent_fraud, percent_non_fraud

def get_IV_for_column(bucket_query):
	information_value = 0

	discrete_values_quantity = 0

	categories_df = duckdb.sql(bucket_query).df()

	for index, row in categories_df.iterrows():
		WoE, percent_fraud, percent_non_fraud = calculate_weight_of_evidence_and_percents(row['IS_FRAUD_QUANTITY'], row['TRANSACTION_QUANTITY'])

		diff = percent_fraud - percent_non_fraud

		information_value += WoE * diff

		discrete_values_quantity += 1

	return information_value, discrete_values_quantity

def get_IV_for_columns():
	column_IVs = []

	columns_to_skip = [
		'IS_FRAUD',
		'FLAGGED',
		'DATE',
		'TIME',
		'ML_SCORE',
		'ML_PROBABILITY',
		'COST_VARIATION_FACTOR',
		'ID',
		'UNPROCESSED_USD_FEES',
		'TRANSACTION_USD_AMOUNT',
		'FULL_NAME',
		'STATUS',
		'AGE',
		'BALANCE',
		'OPEN_DATE',
		'CUSTOMER_LIFETIME_VALUE',
		'CREDIT_LIMIT'
	]

	special_grouping_columns = [
		{
			'name': 'TRANSACTION_MONTH (FROM DATE)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/TRANSACTION_MONTH.sql'
		},
		{
			'name': 'HOUR (FROM DATE)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/HOUR.sql'
		},
		{
			'name': 'TRANSACTION_USD_AMOUNT (BUCKETED 2000 GROUPS)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/TRANSACTION_USD_AMOUNT.sql'
		},
		{
			'name': 'AGE (bucketed 10 year range)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/AGE.sql'
		},
		{
			'name': 'BALANCE (bucketed 5000 range)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/BALANCE.sql'
		},
		{
			'name': 'OPEN_DATE_MONTH (FROM OPEN_DATE)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/OPEN_DATE_MONTH.sql'
		},
		{
			'name': 'CUSTOMER_LIFETIME_VALUE (custom bucketing)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/CUSTOMER_LIFETIME_VALUE.sql'
		},
		{
			'name': 'CREDIT_LIMIT (custom bucketing)',
			'sql_file': 'project/SQL/BUCKETS/ANALYSIS_BUCKETS/CREDIT_LIMIT.sql'
		}
	]

	for column in joined_tables_for_analysis.columns:
		if column in columns_to_skip: continue

		bucket_query = get_default_bucket_query(column)

		iv, discrete_values_quantity = get_IV_for_column(bucket_query)

		column_IVs.append({'column': column, 'IV': iv, 'discrete_values_quantity': discrete_values_quantity})
	
	for column in special_grouping_columns:
		bucket_query = open(column['sql_file'], 'r').read()

		iv, discrete_values_quantity = get_IV_for_column(bucket_query)

		column_IVs.append({'column': column['name'], 'IV': iv, 'discrete_values_quantity': discrete_values_quantity})

	column_IVs.sort(key=lambda x: x['IV'], reverse=True)

	for column_IV in column_IVs:
		print(f'{column_IV['column']}, IV: {column_IV['IV']}, Discrete values quantity: {column_IV['discrete_values_quantity']}')

	return pd.DataFrame(column_IVs)

print(get_IV_for_columns().to_string(index=False))
#print(joined_tables_for_analysis['STATUS'].drop_duplicates())
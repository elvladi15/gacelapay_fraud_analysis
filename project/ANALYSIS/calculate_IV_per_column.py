from project.ANALYSIS.analyze_transactions_data import joined_tables_for_analysis
import duckdb
import math
import pandas as pd
from pathlib import Path
from itertools import combinations
import multiprocessing as mp

LAPLACE_SMOOTHING = 0.5

transaction_totals_query = open('project/SQL/TRANSACTION_TOTALS.sql', 'r').read()

total_fraud, total_transactions = duckdb.sql(transaction_totals_query).fetchone()

total_non_fraud = total_transactions - total_fraud

analysis_buckets_directory = Path('project/SQL/BUCKETS/ANALYSIS_BUCKETS')

def get_columns_bucket_query(column_list):
	name = ''

	name = 'x'.join(map(lambda x: x['name'], column_list))

	return len(column_list), name, f'''
		WITH
			{','.join(map(lambda x: f'BUCKET{x[0] + 1} AS({x[1]['query']})', enumerate(column_list)))}
		SELECT
			{','.join(map(lambda x: f'BUCKET{x[0] + 1}.BUCKET', enumerate(column_list)))},
			SUM(JTA.IS_FRAUD)	AS IS_FRAUD_QUANTITY,
			COUNT(*)			AS TRANSACTION_QUANTITY
		FROM
			joined_tables_for_analysis	JTA
			{' '.join(map(lambda x: f'INNER JOIN BUCKET{x[0] + 1} ON JTA.ID = BUCKET{x[0] + 1}.ID', enumerate(column_list)))}
		GROUP BY
			{','.join(map(lambda x: f'BUCKET{x[0] + 1}.BUCKET', enumerate(column_list)))};
	'''

def calculate_weight_of_evidence_and_percents(is_fraud_quantity, transaction_quantity):
	percent_fraud = (is_fraud_quantity + LAPLACE_SMOOTHING) / total_fraud

	non_fraud_quantity = transaction_quantity - is_fraud_quantity + LAPLACE_SMOOTHING

	percent_non_fraud = non_fraud_quantity / total_non_fraud

	WoE = round(math.log(percent_fraud / percent_non_fraud), 4)

	return WoE, percent_fraud, percent_non_fraud

def get_IV_for_column(bucket_df):
	information_value = 0

	discrete_values_quantity = 0

	for index, row in bucket_df.iterrows():
		WoE, percent_fraud, percent_non_fraud = calculate_weight_of_evidence_and_percents(row['IS_FRAUD_QUANTITY'], row['TRANSACTION_QUANTITY'])

		diff = percent_fraud - percent_non_fraud

		information_value += WoE * diff

		discrete_values_quantity += 1

	return information_value, discrete_values_quantity

def process_parameter(parameter):
	parameter = list(parameter)

	column_quantity, bucket_name_final, bucket_query_final = get_columns_bucket_query(parameter)

	bucket_df = duckdb.sql(bucket_query_final).df()

	iv, discrete_values_quantity = get_IV_for_column(bucket_df)

	return {'COLUMN_QUANTITY':column_quantity, 'NAME': bucket_name_final,'IV': iv, 'DISCRETE_VALUES_QUANTITY': discrete_values_quantity}

def get_IV_for_columns_df(col_combination_quantity):
	column_IVs = []
	bucket_queries = []
	parameters = []

	for file_path in analysis_buckets_directory.iterdir():
		sql_query = open(file_path, 'r').read()

		bucket_queries.append({'name': file_path.stem,'query': sql_query})

	for i in range(col_combination_quantity):
		parameters += list(combinations(bucket_queries, i + 1))

	with mp.Pool(mp.cpu_count()) as pool:
		column_IVs = list(pool.map(process_parameter, parameters))

	column_IVs.sort(key=lambda x: x['IV'], reverse=True)

	return pd.DataFrame(column_IVs)
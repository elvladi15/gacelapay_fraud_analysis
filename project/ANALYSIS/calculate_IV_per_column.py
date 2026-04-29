from project.ANALYSIS.analyze_transactions_data import joined_tables_for_analysis
import duckdb
import math
import pandas as pd
from pathlib import Path
from itertools import combinations
import multiprocessing as mp
from project.utils import generate_csv_file_from_df

LAPLACE_SMOOTHING = 0.5

transaction_totals_query = open('project/SQL/TRANSACTION_TOTALS.sql', 'r').read()

total_fraud, total_transactions = duckdb.sql(transaction_totals_query).fetchone()

total_non_fraud = total_transactions - total_fraud

analysis_buckets_directory = Path('project/SQL/BUCKETS/ANALYSIS_BUCKETS')

def get_columns_bucket_query(column_list):
	ids = ','.join(map(lambda x: str(x['id']), column_list))

	name = 'x'.join(map(lambda x: x['name'], column_list))

	return ids, name, f'''
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

	ids, bucket_name_final, bucket_query_final = get_columns_bucket_query(parameter)

	bucket_df = duckdb.sql(bucket_query_final).df()

	iv, discrete_values_quantity = get_IV_for_column(bucket_df)

	return {
		'ids': ids,
		'name': bucket_name_final,
		'iv': iv,
		'discrete_values_quantity': discrete_values_quantity
	}

def get_IV_for_columns_df(col_combination_quantity):
	column_IVs = []
	bucket_queries = []
	parameters = []

	for index, file_path in enumerate(analysis_buckets_directory.iterdir()):
		sql_query = open(file_path, 'r').read()

		bucket_queries.append({
			'id': index + 1,
			'name': file_path.stem,
			'query': sql_query
		})

	for i in range(col_combination_quantity):
		parameters += list(combinations(bucket_queries, i + 1))

	with mp.Pool(mp.cpu_count()) as pool:
		column_IVs = list(pool.map(process_parameter, parameters))

	column_IVs.sort(key=lambda x: x['iv'], reverse=True)

	return pd.DataFrame(column_IVs)

def get_combined_column_stats_df(df):
	df_object = []
	
	for index, row in df.iterrows():

		column_ids = row['ids'].split(',')

		if len(column_ids) == 1: continue

		column_details = []

		for curr_id in column_ids:
			for index, curr_row in df.iterrows():
				if curr_row['ids'] == curr_id:
					column_details.append({
						'name': curr_row['name'],
						'iv': curr_row['iv']
					})

		combined_iv = row['iv']

		individual_ivs = ','.join(map(lambda x: str(x['iv']), column_details))

		individual_ivs_sum = sum(map(lambda x: float(x['iv']), column_details))

		df_object.append({
			'columns': ','.join(map(lambda x: str(x['name']), column_details)),
			'discrete_values_quantity': row['discrete_values_quantity'],
			'combined_iv': combined_iv,
			'individual_ivs': individual_ivs,
			'is_combined_iv_higher': combined_iv > individual_ivs_sum
		})

	return pd.DataFrame(df_object)
	
if __name__ == '__main__':
	all_ivs_df = get_IV_for_columns_df(2)

	combined_column_stats = get_combined_column_stats_df(all_ivs_df)

	combined_column_stats.columns = combined_column_stats.columns.str.upper()

	generate_csv_file_from_df(combined_column_stats, 'project/ANALYSIS/COMBINED_COLUMN_STATS.csv')
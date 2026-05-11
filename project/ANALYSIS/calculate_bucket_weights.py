import duckdb
from project.ANALYSIS.calculate_IV_per_column import joined_tables_for_analysis, calculate_weight_of_evidence_and_percents
from pathlib import Path
import pandas as pd
from project.utils import generate_csv_file_from_df

weight_calculation_buckets_directory = Path('project/SQL/BUCKETS/WEIGHT_CALCULATION_BUCKETS')

def get_bucket_weights_per_query_df(sql_file):
	sql_query = open(sql_file, 'r').read()

	buckets_df = duckdb.sql(sql_query).df()

	for row in buckets_df.itertuples():
		buckets_df.at[row.Index, 'WOE'] = calculate_weight_of_evidence_and_percents(buckets_df.at[row.Index, 'IS_FRAUD_QUANTITY'], buckets_df.at[row.Index, 'TRANSACTION_QUANTITY'])[0]

	return buckets_df

def get_bucket_weights_df():
	df_object_list = []

	for file_path in weight_calculation_buckets_directory.iterdir():
		weights_df = get_bucket_weights_per_query_df(file_path)

		df_object_list.append({'NAME': file_path.stem, 'WOE': weights_df['WOE'].item()})

	df_object_list.sort(key=lambda x: x['WOE'], reverse=True)

	return pd.DataFrame(df_object_list)

print(get_bucket_weights_per_query_df('project/SQL/BUCKETS/WEIGHT_CALCULATION_BUCKETS/TEST.sql'))

#generate_csv_file_from_df(get_bucket_weights_df(), 'project/ANALYSIS/WEIGHTS.csv')
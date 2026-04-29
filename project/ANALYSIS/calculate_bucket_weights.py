import duckdb
from project.ANALYSIS.calculate_IV_per_column import joined_tables_for_analysis, calculate_weight_of_evidence_and_percents

def get_bucket_weights(sql_file):
	sql_query = open(sql_file, 'r').read()

	buckets_df = duckdb.sql(sql_query).df()

	for row in buckets_df.itertuples():
		buckets_df.at[row.Index, 'WOE'] = calculate_weight_of_evidence_and_percents(buckets_df.at[row.Index, 'IS_FRAUD_QUANTITY'], buckets_df.at[row.Index, 'TRANSACTION_QUANTITY'])[0]

	return buckets_df
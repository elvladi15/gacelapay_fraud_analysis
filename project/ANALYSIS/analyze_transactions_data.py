import duckdb
import pandas as pd
from pathlib import Path
from project.utils import generate_csv_file_from_sql

def get_transaction_flag_result(transaction_id):
	return 1
	#return duckdb.sql(
	#	f'''
	#		SELECT
	#			FLAGGED
	#		FROM
	#			'project/CLEAN_DATASETS/FRAUD_DECISIONS.csv'
	#		WHERE
	#			TRANSACTION_ID = '{transaction_id}'
	#	'''
	#).fetchone()[0]

def get_transaction_statistics(weights, threshold):
	flag_results_list = []
	clean_transactions_df = pd.read_csv('project/CLEAN_DATASETS/TRANSACTIONS.csv')

	joined_tables_for_analysis = duckdb.sql(open('project/SQL/JOIN_ALL_TABLES_FOR_ANALYSIS.sql', 'r').read()).df()

	#for row in df.itertuples():
	#	df.at[row.Index, 'FLAGGED'] = 0
	duckdb.sql(open('project/SQL/GET_FRAUD_STATISTICS.sql', 'r').read()).show()

get_transaction_statistics(None, None)
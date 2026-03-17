import duckdb
from pathlib import Path

def generate_csv_file_from_sql(sql_query_path, output_file_path):
	sql_file = Path(sql_query_path)

	sql_query= open(sql_file, 'r').read()

	duckdb.sql(sql_query).df().to_csv(output_file_path, index=False)

def get_ml_result(is_fraud, flagged):
	result = 'TRUE ' if is_fraud == flagged else 'FALSE '
	result += 'POSITIVE' if flagged else 'NEGATIVE'
	return result
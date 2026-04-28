import duckdb
from duckdb.sqltypes import VARCHAR, BOOLEAN
from pathlib import Path
import gender_guesser.detector as gender
import pycountry

d = gender.Detector()

def guess_gender(first_name):
	return d.get_gender(first_name)

def detect_country(country_code):
	return pycountry.countries.lookup(country_code).name

def get_confusion_matrix_result(is_fraud, flagged):
	result = 'TRUE ' if is_fraud == flagged else 'FALSE '
	result += 'POSITIVE' if flagged else 'NEGATIVE'
	return result

duckdb.create_function('GUESS_GENDER', guess_gender, [VARCHAR], VARCHAR)
duckdb.create_function('DETECT_COUNTRY', detect_country, [VARCHAR], VARCHAR)
duckdb.create_function('GET_ML_RESULT', get_confusion_matrix_result, [BOOLEAN, BOOLEAN], VARCHAR)

def generate_df_from_sql(sql_query_path):
	sql_file = Path(sql_query_path)

	sql_query = open(sql_file, 'r').read()

	return duckdb.sql(sql_query).df()

def generate_csv_file_from_df(df, output_file_path):
	df.to_csv(output_file_path, index = False, encoding='utf-8-sig')
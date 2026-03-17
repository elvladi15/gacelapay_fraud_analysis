import os
from project.utils import generate_csv_file_from_sql

if not os.path.exists('project/CLEANED_COMBINED_EXCHANGE_RATES.csv'):
	generate_csv_file_from_sql('project/SQL/CLEAN_EXCHANGE_RATES.sql', 'project/CLEANED_COMBINED_EXCHANGE_RATES.csv')

if not os.path.exists('project/CLEAN_DATASETS/ACCOUNTS.csv'):
	generate_csv_file_from_sql('project/SQL/CLEAN_ACCOUNTS.sql', 'project/CLEAN_DATASETS/ACCOUNTS.csv')
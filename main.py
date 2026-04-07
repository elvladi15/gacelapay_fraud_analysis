from project.utils import generate_csv_file_from_sql
#from project.ANALYSIS.analyze_transactions_data import create_test_cases_csv

#STEP 1: CLEAN DATASETS
#generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_EXCHANGE_RATES.sql', 'project/CLEAN_DATASETS/CLEAN_COMBINED_EXCHANGE_RATES.csv')
#generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_ACCOUNTS.sql', 'project/CLEAN_DATASETS/ACCOUNTS.csv')
#generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_CUSTOMERS.sql', 'project/CLEAN_DATASETS/CUSTOMERS.csv')
#generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_DECISIONS.sql', 'project/CLEAN_DATASETS/FRAUD_DECISIONS.csv')
#generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_TRANSACTIONS.sql', 'project/CLEAN_DATASETS/TRANSACTIONS.csv')
#generate_csv_file_from_sql('project/SQL/DATA_CLEANING/CLEAN_FRAUD_COSTS.sql', 'project/CLEAN_DATASETS/FRAUD_COSTS.csv')

#STEP 2: DENORMALIZE TRANSACTIONS
#generate_csv_file_from_sql('project/SQL/DENORMALIZE_TRANSACTIONS.sql', 'project/ANALYSIS/DENORMALIZED_TRANSACTIONS.csv')
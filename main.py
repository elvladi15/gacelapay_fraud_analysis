import os
from project.utils import generate_csv_file_from_sql


#generate_csv_file_from_sql('project/SQL/CLEAN_EXCHANGE_RATES.sql', 'project/CLEAN_DATASETS/CLEAN_COMBINED_EXCHANGE_RATES.csv')
#generate_csv_file_from_sql('project/SQL/CLEAN_ACCOUNTS.sql', 'project/CLEAN_DATASETS/ACCOUNTS.csv')
#generate_csv_file_from_sql('project/SQL/CLEAN_CUSTOMERS.sql', 'project/CLEAN_DATASETS/CUSTOMERS.csv')
generate_csv_file_from_sql('project/SQL/CLEAN_TRANSACTIONS.sql', 'project/CLEAN_DATASETS/TRANSACTIONS.csv')

#generate_csv_file_from_sql('project/SQL/CLEAN_FRAUD_DECISIONS.sql', 'project/CLEAN_DATASETS/FRAUD_DECISIONS.csv')
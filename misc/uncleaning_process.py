import os
from misc.synthetic_dataset_creator import generate_synthetic_dataset
from project.utils import generate_df_from_sql, generate_csv_file_from_df


#STEP 1: GENERATE SYNTHETIC CLEAN DATA
if not os.path.isdir('misc/SYNTHETIC_DATASET_TEST'):
	generate_synthetic_dataset('misc/SYNTHETIC_DATASET_TEST')

#STEP 2: FIX SOME COLUMN VALUES TO MAKE MORE SENSE

#STEP 3 (ONLY APPLIES TO CERTAIN TABLES): APPLY SQL SCRIPT TO UNCLEAN THE DATASET
if not os.path.exists('misc/STEP_3/accounts.csv'):
	df = generate_df_from_sql('misc/SQL/UNCLEAN_ACCOUNTS.sql')
	generate_csv_file_from_df(df, 'misc/STEP_3/accounts.csv')

#STEP 4: INSERT RANDOM ROWS MANUALLY
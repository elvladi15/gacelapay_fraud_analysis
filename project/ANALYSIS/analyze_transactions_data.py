import duckdb
from scipy.special import logit, expit
import project.utils

def get_transaction_statistics_df(weights, threshold):
	threshold_probability = threshold / 1000

	joined_tables_for_analysis = duckdb.sql(open('project/SQL/JOIN_ALL_TABLES_FOR_ANALYSIS.sql', 'r').read()).df()

	if weights != None:
		for row in joined_tables_for_analysis.itertuples():
			ml_probability = joined_tables_for_analysis.at[row.Index, 'ML_PROBABILITY']

			logit_value = logit(ml_probability)

			# feature 1
			if joined_tables_for_analysis.at[row.Index, 'TIME'] > '23:00:00':
				logit_value += weights[0]

			# feature 2
			if joined_tables_for_analysis.at[row.Index, 'CUSTOMER_COUNTRY'] == 'Brazil':
				logit_value += weights[1]

			# feature 3
			if joined_tables_for_analysis.at[row.Index, 'TRANSACTION_USD_AMOUNT'] > 10000:
				logit_value += weights[2]

			joined_tables_for_analysis.at[row.Index, 'FLAGGED'] = 1 if expit(logit_value) >= threshold_probability else 0

	fraud_statistics_df = duckdb.sql(open('project/SQL/GET_FRAUD_STATISTICS.sql', 'r').read()).df()

	fraud_statistics_df.at[0, 'W1'] = weights[0]
	fraud_statistics_df.at[0, 'W2'] = weights[1]
	fraud_statistics_df.at[0, 'W3'] = weights[2]

	fraud_statistics_df = fraud_statistics_df.reindex(columns=
	[
		'FRAUD_ANALYSIS_ID',
		'W1',
		'W2',
		'W3',
		'FALSE_POSITIVE_RATE',
		'GRAND_TOTAL',
		'FRAUD_DETECTION_RATE',
		'PRECISION',
		'ACCURACY',
		'USD_FEES',
		'TOTAL_FRAUD_LOSS',
		'TOTAL_INVESTIGATION_COST',
		'TOTAL_CUSTOMER_SUPPORT_COST',
		'TOTAL_LOST_INTERCHANGE'
	])

	return fraud_statistics_df


def create_fraud_statistics_csv():

	for i in range(3):
		match i:
			case 0:
				df = get_transaction_statistics_df([0, 0, 0], 700) #Default case
			case 1:
				df = get_transaction_statistics_df([0.5, 0.6, 0.7], 700)
			case 2:
				df = get_transaction_statistics_df([0.8, 0.9, 1], 700)

		if i == 0:
			df.to_csv('project/ANALYSIS/FRAUD_STATISTICS.csv', index=False)
		else:
			df.to_csv('project/ANALYSIS/FRAUD_STATISTICS.csv', mode='a', index=False, header=False)

create_fraud_statistics_csv()
def feature_1_test(time):
	return time > '23:00:00'

def feature_2_test(customer_country):
	return customer_country == 'BRAZIL'

def feature_3_test(transaction_usd_amount):
	return transaction_usd_amount > 5000

features_list = [
	{
		'columns': ['TIME'],
		'function': feature_1_test
	},
	{
		'columns': ['CUSTOMER_COUNTRY'],
		'function': feature_2_test
	},
	{
		'columns': ['TRANSACTION_USD_AMOUNT'],
		'function': feature_3_test
	}
]
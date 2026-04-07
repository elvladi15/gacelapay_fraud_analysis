def feature_1_test(time):
	return time > '23:00:00'

def feature_2_test(customer_country):
	return customer_country == 'Brazil'

def feature_3_test(transaction_usd_amount):
	return transaction_usd_amount > 10000
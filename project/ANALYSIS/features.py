from datetime import datetime

thresholds_list = list(range(930, 941, 1))

def feature_1_test(date, time):
	time = datetime.strptime(str(time), "%H:%M:%S").time()

	if date.month in(1, 11, 12) and 12 <= time.hour <= 17: return 1.4361 - 0.4
	if date.month in(1, 11, 12): return 0.8113 - 0.4
	if 12 <= time.hour <= 17: return 0.6016

	return 0

def feature_2_test(merchant_category):
	if merchant_category in('HIGH VALUE RETAIL', 'TRAVEL', 'DIGITAL GOODS'): return 0.7586

	return 0

def feature_3_test(channel):
	if channel in('VIRTUAL CARD', 'FAKE MOBILE APP', 'MOBILE APP', 'SIM SWAP'): return 0.3398

	return 0

features_list = [
	{
		'columns': ['DATE', 'TIME'],
		'function': feature_1_test
	},
	{
		'columns': ['MERCHANT_CATEGORY'],
		'function': feature_2_test
	},
	{
		'columns': ['CHANNEL'],
		'function': feature_3_test
	}
]
from datetime import datetime

thresholds_list = [700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800]

def feature_1_test(date, time):
	time = datetime.strptime(str(time), "%H:%M:%S").time()

	if date.month in(1, 11, 12) and 12 <= time.hour <= 17: return 3
	if date.month in(1, 11, 12): return 1
	if 12 <= time.hour <= 17: return 1

	return 0

features_list = [
	{
		'columns': ['DATE', 'TIME'],
		'function': feature_1_test
	}
]
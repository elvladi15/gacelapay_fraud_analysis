import matplotlib.pyplot as plt
from project.ANALYSIS.analyze_transactions_data import get_test_case_transactions_df
import matplotlib.ticker as mtick

kpi_names = ['FDR', 'FPR']

def get_kpi_for_test_case(test_case_df, kpi):
	test_case_df['YEAR_MONTH'] = test_case_df['DATE'].dt.to_period('M')

	grouped_df = (
		test_case_df.groupby('YEAR_MONTH')
		.agg(
			FALSE_POSITIVE = ('ML_RESULT', lambda x: (x == 'FALSE POSITIVE').sum()),
			FALSE_NEGATIVE = ('ML_RESULT', lambda x: (x == 'FALSE NEGATIVE').sum()),
			TRUE_POSITIVE = ('ML_RESULT', lambda x: (x == 'TRUE POSITIVE').sum()),
			TRUE_NEGATIVE = ('ML_RESULT', lambda x: (x == 'TRUE NEGATIVE').sum()),
			GRAND_TOTAL = ('GRAND_TOTAL', 'sum')
		)
		.reset_index()
	)

	grouped_df['YEAR_MONTH'] = grouped_df['YEAR_MONTH'].astype(str)

	match kpi:
		case 'FDR': grouped_df[kpi] = grouped_df['TRUE_POSITIVE'] / (grouped_df['TRUE_POSITIVE'] + grouped_df['FALSE_NEGATIVE'])
		case 'FPR': grouped_df[kpi] = grouped_df['FALSE_POSITIVE'] / (grouped_df['FALSE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'])
		case 'PRECISION': grouped_df[kpi] = grouped_df['TRUE_POSITIVE'] / (grouped_df['TRUE_POSITIVE'] + grouped_df['FALSE_POSITIVE'])
		case 'ACCURACY': grouped_df[kpi] = grouped_df['TRUE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'] / (grouped_df['TRUE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'] + grouped_df['FALSE_POSITIVE'] + grouped_df['FALSE_NEGATIVE'])

	grouped_df = grouped_df.sort_values('YEAR_MONTH')

	return grouped_df

def plot_statistic_comparison(test_case_1, test_case_2, kpi):
	plt.figure(figsize=(10, 5))

	line_1_data = get_kpi_for_test_case(test_case_1, kpi)
	plt.plot(
		line_1_data['YEAR_MONTH'],
		line_1_data[kpi],
		marker='o'
	)

	line_2_data = get_kpi_for_test_case(test_case_2, kpi)
	plt.plot(
		line_2_data['YEAR_MONTH'],
		line_2_data[kpi],
		marker='o'
	)

	step = 4

	plt.xticks(
		ticks=range(0, len(line_1_data), step),
		labels=line_1_data['YEAR_MONTH'][::step],
		rotation=45
	)

	if kpi != 'GRAND_TOTAL':
		ax = plt.gca()
		ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=2))

	plt.xlabel('Month')
	plt.ylabel(kpi)
	plt.title(f'{kpi} over time')

	plt.xticks(rotation=45)

base_test_case_df = get_test_case_transactions_df(700, True)
best_test_case_df = get_test_case_transactions_df(934, False)

plot_statistic_comparison(base_test_case_df, best_test_case_df, 'ACCURACY')

plt.tight_layout()
plt.show()
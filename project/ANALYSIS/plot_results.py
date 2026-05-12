import matplotlib.pyplot as plt
from project.ANALYSIS.analyze_transactions_data import get_test_case_transactions_df
import matplotlib.ticker as mtick
import pandas as pd

kpi_names = ['FDR', 'FPR', 'PRECISION', 'ACCURACY']

fig, axs = plt.subplots(2, 2, figsize=(15, 8))

plt.subplots_adjust(hspace=0.5)

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

	grouped_df['GRAND_TOTAL'] = -grouped_df['GRAND_TOTAL']

	grouped_df['YEAR_MONTH'] = grouped_df['YEAR_MONTH'].astype(str)

	match kpi:
		case 'FDR': grouped_df[kpi] = grouped_df['TRUE_POSITIVE'] / (grouped_df['TRUE_POSITIVE'] + grouped_df['FALSE_NEGATIVE'])
		case 'FPR': grouped_df[kpi] = grouped_df['FALSE_POSITIVE'] / (grouped_df['FALSE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'])
		case 'PRECISION': grouped_df[kpi] = grouped_df['TRUE_POSITIVE'] / (grouped_df['TRUE_POSITIVE'] + grouped_df['FALSE_POSITIVE'])
		case 'ACCURACY': grouped_df[kpi] = (grouped_df['TRUE_POSITIVE'] + grouped_df['TRUE_NEGATIVE']) / (grouped_df['TRUE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'] + grouped_df['FALSE_POSITIVE'] + grouped_df['FALSE_NEGATIVE'])

	grouped_df = grouped_df.sort_values('YEAR_MONTH')

	return grouped_df

def plot_statistic_comparison(row_index, col_index, test_cases, kpi):
	df = pd.DataFrame()

	for test_case in test_cases:
		df = get_kpi_for_test_case(test_case, kpi)

		axs[row_index, col_index].plot(
			df['YEAR_MONTH'],
			df[kpi],
			marker='o'
		)

	axs[row_index, col_index].set_xticks(range(0, len(df['YEAR_MONTH']), 4))

	axs[row_index, col_index].tick_params(axis='x', rotation=45)

	if kpi != 'GRAND_TOTAL':
		ax = axs[row_index, col_index]

		ax.yaxis.set_major_formatter(
			mtick.PercentFormatter(1.0, decimals=2)
		)

	axs[row_index, col_index].set_xlabel('Month')
	axs[row_index, col_index].set_ylabel(kpi)
	axs[row_index, col_index].set_title(f'{kpi} over time')

base_test_case_df = get_test_case_transactions_df(700, True)
best_test_case_df = get_test_case_transactions_df(940, False)

for index, kpi in enumerate(kpi_names):
	row = index // 2
	col = index % 2

	plot_statistic_comparison(row, col, [base_test_case_df, best_test_case_df], kpi)

plt.show()
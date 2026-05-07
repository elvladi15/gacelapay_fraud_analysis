import matplotlib.pyplot as plt
from project.ANALYSIS.analyze_transactions_data import get_test_case_transactions_df
import matplotlib.ticker as mtick

def get_false_positive_rate_per_month_for_test_case(test_case_df):
	test_case_df['YEAR_MONTH'] = test_case_df['DATE'].dt.to_period('M')

	grouped_df = (
		test_case_df.groupby('YEAR_MONTH')
		.agg(
			FALSE_POSITIVE=('ML_RESULT', lambda x: (x == 'FALSE POSITIVE').sum()),
			FALSE_NEGATIVE=('ML_RESULT', lambda x: (x == 'FALSE NEGATIVE').sum()),
			TRUE_POSITIVE=('ML_RESULT', lambda x: (x == 'TRUE POSITIVE').sum()),
			TRUE_NEGATIVE=('ML_RESULT', lambda x: (x == 'TRUE NEGATIVE').sum()),
		)
		.reset_index()
	)

	grouped_df['YEAR_MONTH'] = grouped_df['YEAR_MONTH'].astype(str)

	grouped_df['FPR'] = grouped_df['FALSE_POSITIVE'] / (grouped_df['FALSE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'])

	grouped_df = grouped_df.sort_values('YEAR_MONTH')

	return grouped_df

base_test_case_df = get_test_case_transactions_df(700, True)
best_test_case_df = get_test_case_transactions_df(934, False)

# Plot
plt.figure(figsize=(10, 5))

line_1_data = get_false_positive_rate_per_month_for_test_case(base_test_case_df)
plt.plot(
	line_1_data['YEAR_MONTH'],
	line_1_data['FPR'],
	marker='o'
)

line_2_data = get_false_positive_rate_per_month_for_test_case(best_test_case_df)
plt.plot(
	line_2_data['YEAR_MONTH'],
	line_2_data['FPR'],
	marker='o'
)

step = 4

plt.xticks(
	ticks=range(0, len(line_1_data), step),
	labels=line_1_data['YEAR_MONTH'][::step],
	rotation=45
)

ax = plt.gca()
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=2))

plt.xlabel('Month')
plt.ylabel('FPR')
plt.title('FPR over time')

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
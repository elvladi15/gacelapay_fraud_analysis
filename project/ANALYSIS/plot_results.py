import matplotlib.pyplot as plt
from project.ANALYSIS.analyze_transactions_data import get_test_case_transactions_df
import matplotlib.ticker as mtick
import pandas as pd
from sklearn.metrics import confusion_matrix

fig, axs = plt.subplots(2, 2, figsize=(15, 8))

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

def save_base_and_best_case_comparison(test_case_df_1, test_case_df_2, file_name):
	plt.close('all')

	plt.subplots_adjust(hspace=0.5)

	kpi_names = ['FDR', 'FPR', 'PRECISION', 'ACCURACY']

	for index, kpi in enumerate(kpi_names):
		row = index // 2
		col = index % 2

		plot_statistic_comparison(row, col, [test_case_df_1, test_case_df_2], kpi)

	plt.savefig(file_name)

def generate_confusion_matrix(test_case_df, plot_title, file_name):
	my_color = '#028895'

	plt.close('all')

	cm = confusion_matrix(test_case_df['IS_FRAUD'].tolist(), test_case_df['FLAGGED'].tolist())
	
	cm = cm[::-1, ::-1]

	fig, ax = plt.subplots(figsize=(12, 11))

	ax.set_position([
		0.15,
		0.03,
		0.75,
		0.75
	])

	ax.set_box_aspect(1)

	ax.imshow(cm)

	ax.set_title(plot_title, fontsize=35, pad=35, color=my_color, fontweight='bold')

	ax.set_xlabel('FLAGGED', fontsize=25, fontweight='bold', color=my_color, labelpad=25)
	ax.set_ylabel('IS FRAUD', fontsize=25, fontweight='bold', color=my_color, labelpad=25)

	ax.xaxis.tick_top()
	ax.xaxis.set_label_position('top')

	for label in ax.get_xticklabels():
		label.set_fontweight('bold')
		label.set_color(my_color)

	for label in ax.get_yticklabels():
		label.set_fontweight('bold')
		label.set_color(my_color)

	ax.set_xticks([0, 1])
	ax.set_yticks([0, 1])

	ax.set_xticklabels(['YES', 'NO'], fontsize=25)
	ax.set_yticklabels(['YES', 'NO'], fontsize=25)

	ax.tick_params(axis='both', length=0)

	ax.set_ylim(1.5, -0.5)

	for spine in ax.spines.values():
		spine.set_visible(False)

	for x in [-0.5, 0.5, 1.5]:
		ax.axhline(x, color='white', linewidth=8)
		ax.axvline(x, color='white', linewidth=8)

	for patch in ax.patches[:]:
		patch.remove()

	for i in range(2):
		for j in range(2):
			binary_result = 'T' if i == j else 'F'
			binary_result += 'P' if j == 0 else 'N'

			rect = plt.Rectangle(
				(j - 0.5, i - 0.5),
				1,
				1,
				fill=True,
				color=my_color
			)

			ax.add_patch(rect)

			ax.text(
				j,
				i,
				f'{binary_result}\n{cm[i, j]:,}',
				ha='center',
				va='center',
				color='white',
				fontsize=35,
				fontweight='bold'
			)

	plt.savefig(file_name)
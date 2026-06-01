import matplotlib.pyplot as plt
from project.ANALYSIS.analyze_transactions_data import get_test_case_transactions_df
import matplotlib.ticker as mtick
import pandas as pd
from sklearn.metrics import confusion_matrix
from main import MY_BLUE_COLOR, MY_GOLDEN_COLOR
import numpy as np

font_family = 'Tahoma'

def get_kpi_for_test_case(test_case_df, kpi):
	test_case_df['YEAR_MONTH'] = test_case_df['DATE'].dt.to_period('M')

	grouped_df = (
		test_case_df.groupby('YEAR_MONTH')
		.agg(
			FALSE_POSITIVE = ('ML_RESULT', lambda x: (x == 'FALSE POSITIVE').sum()),
			FALSE_NEGATIVE = ('ML_RESULT', lambda x: (x == 'FALSE NEGATIVE').sum()),
			TRUE_POSITIVE = ('ML_RESULT', lambda x: (x == 'TRUE POSITIVE').sum()),
			TRUE_NEGATIVE = ('ML_RESULT', lambda x: (x == 'TRUE NEGATIVE').sum()),
			TOTAL_COSTS = ('TOTAL_COSTS', 'sum'),
			USD_FEES = ('USD_FEES', 'sum'),
			GRAND_TOTAL = ('GRAND_TOTAL', 'sum'),
		)
		.reset_index()
	)

	grouped_df['TOTAL_COSTS'] = -grouped_df['TOTAL_COSTS']
	grouped_df['GRAND_TOTAL'] = -grouped_df['GRAND_TOTAL']

	grouped_df['YEAR_MONTH'] = grouped_df['YEAR_MONTH'].dt.to_timestamp()

	match kpi:
		case 'FDR': grouped_df[kpi] = grouped_df['TRUE_POSITIVE'] / (grouped_df['TRUE_POSITIVE'] + grouped_df['FALSE_NEGATIVE'])
		case 'FPR': grouped_df[kpi] = grouped_df['FALSE_POSITIVE'] / (grouped_df['FALSE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'])
		case 'PRECISION': grouped_df[kpi] = grouped_df['TRUE_POSITIVE'] / (grouped_df['TRUE_POSITIVE'] + grouped_df['FALSE_POSITIVE'])
		case 'ACCURACY': grouped_df[kpi] = (grouped_df['TRUE_POSITIVE'] + grouped_df['TRUE_NEGATIVE']) / (grouped_df['TRUE_POSITIVE'] + grouped_df['TRUE_NEGATIVE'] + grouped_df['FALSE_POSITIVE'] + grouped_df['FALSE_NEGATIVE'])

	grouped_df = grouped_df.sort_values('YEAR_MONTH')

	return grouped_df

def plot_line_chart_for_statistic_comparison(test_cases, kpi, title, file_name, step_start, step_end, step_value):
	plt.close('all')
	
	fig, ax = plt.subplots(figsize=(12, 9))

	df = pd.DataFrame()

	colors = []

	for test_case in test_cases:

		df = get_kpi_for_test_case(test_case['df'], kpi)

		plt.plot(
			df['YEAR_MONTH'],
			df[kpi],
			color=test_case['color'],
			linewidth=test_case['linewidth'],
			label=test_case['label']
		)

		colors.append(test_case['color'])

	ticks = df['YEAR_MONTH'][0::12]

	ax.set_xticks(ticks)

	ax.set_xticklabels(
		ticks.dt.strftime('%Y'),
		rotation=45,
		ha='right'
	)
	
	title_lines = title.count('\n') + 1

	fig.suptitle(
		title,
		fontname=font_family,
		fontsize=30,
		y=0.93 + ((title_lines - 1) * 0.03)
	)

	plt.legend(handlelength=1, labelcolor=colors, frameon=False, prop={'weight': 'bold', 'size': 14}, loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=2)
	
	ax.set_position([0.15, 0.2, 0.8, 0.55])

	plt.xlabel('')
	plt.ylabel(kpi.replace('_', ' '), fontsize=20, fontweight='bold', labelpad=10)

	ax.tick_params(axis='x', labelsize=16, width=2, length=9)
	ax.tick_params(axis='y', labelsize=16, width=2, length=9)

	for label in ax.get_xticklabels():
		label.set_fontweight('bold')

	for label in ax.get_yticklabels():
		label.set_fontweight('bold')

	for spine in ax.spines.values():
		spine.set_visible(False)

	plt.yticks(
		np.arange(step_start, step_end + step_value, step_value)
	)

	if kpi in ('TOTAL_COSTS', 'GRAND_TOTAL', 'USD_FEES'):
		plt.gca().yaxis.set_major_formatter(
			mtick.FuncFormatter(
				lambda x, p: (
					f'{x/1000:.{1 if kpi == 'USD_FEES' else 0}f}K' if x >= 1000 else f'{x:.0f}'
				)
			)
		)
	else:
		ax.yaxis.set_major_formatter(
			mtick.PercentFormatter(1.0, decimals=0)
		)

	plt.savefig(file_name)

def generate_confusion_matrix(test_case_df, plot_title, file_name):
	plt.close('all')

	cm = confusion_matrix(test_case_df['IS_FRAUD'].tolist(), test_case_df['FLAGGED'].tolist())
	
	cm = cm[::-1, ::-1]

	fig, ax = plt.subplots(figsize=(12, 11))

	ax.set_position([0.15, 0.03, 0.75, 0.75])

	ax.set_box_aspect(1)

	ax.imshow(cm)

	ax.set_title(plot_title, fontname=font_family, fontsize=35, pad=35)

	ax.set_xlabel('FLAGGED', fontsize=25, fontweight='bold', labelpad=25)
	ax.set_ylabel('IS FRAUD', fontsize=25, fontweight='bold', labelpad=25)

	ax.xaxis.tick_top()
	ax.xaxis.set_label_position('top')

	for label in ax.get_xticklabels():
		label.set_fontweight('bold')

	for label in ax.get_yticklabels():
		label.set_fontweight('bold')

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
				color=MY_BLUE_COLOR if i == j else MY_GOLDEN_COLOR
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
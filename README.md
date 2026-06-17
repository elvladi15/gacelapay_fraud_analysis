<div align='center'>
	<h1>Transaction Fraud Analysis Report</h1>
</div>

<div align='center'>
	<img width='30%' src='assets/gacela_pay_full_logo.png'/>
</div>

## Company Background
**GacelaPay** is a Mexico-based digital financial institution that provides payment and banking services to retail customers across Latin America and Europe, serving thousands of customers in these regions. Founded in 2018 and headquartered in Mexico City, the company has experienced rapid growth by offering a mobile-first experience focused on speed, accessibility, and low fees. It currently processes over **50K** transactions.

GacelaPay's product ecosystem includes:
1. Debit accounts for everyday spending and transfers
2. Credit cards with integrated rewards programs
3. Crypto accounts that allow customers to buy, sell, and hold selected cryptocurrencies
4. Peer-to-peer and international transfers
5. Digital wallets and virtual cards for e-commerce transactions

Over the last few years, the company has struggled with customer retention and rising costs associated with incorrect fraud flagging, as it relied on legacy machine learning models and static thresholds that were not regularly recalibrated to keep pace with evolving fraud patterns.

## Project Overview

For the scope of this project, we will focus on transactions from 2022 to 2025, as this period has been the most underperforming range, largely due to the after-effects of the COVID-19 pandemic.

During these years, the company processed **50,128** transactions, of which **977** were confirmed as fraudulent, representing **1.95%** of all transactions.

Machine learning models analyze transaction patterns over time and output a flag score ranging from 0 to 1000, representing the probability that a given transaction is fraudulent. The system then compares this score with a fixed threshold of 700, meaning that every transaction with a score greater than or equal to this threshold is flagged as fraud and blocked.

The following confusion matrix shows the flagging results:

<div align='center'>
	<img width='60%' src='assets/current_confusion_matrix.png'/>
</div>
<br>

Based on these values, the key metrics are as follows:

| Metric | Value |
| --- | --- |
| False Positive Rate (FPR) | 3.56% |
| Fraud Detection Rate (FDR) | 61.72% |
| Precision | 25.63% |
| Accuracy | 95.76% |

Such a high false positive rate aligns with rising customer churn over the years.

<div align='center'>
	<img width='80%' src='assets/current_fpr.png'/>
</div>
<br>

It has also been reported that total costs associated with fraud activity and incorrect flaggings exceed **$560K**.

## Objective and Key Points (OKR)

The Fraud Strategy and Finance teams have made it clear that they need to meet the following goals:

### 1. Halve False Positive Rates by December 2026
### 2. Reduce Annual Fraud-Related Costs by 25% by Year-End

## Stakeholder Questions

### Fraud Strategy
1. Which fields are most useful for improving fraud detection?
2. Are there any meaningful interactions between these fields?
3. Should the flagging threshold be adjusted, and if so, what value should be used?
4. When a transaction appears to have a high fraud probability, how should that probability be scaled?
5. What features and parameters are recommended to reduce FPR and total costs?

## Dataset Structure and ERD (Entity Relationship Diagram)

<div align='center'>
	<img width='80%' src='assets/entity_relationship_diagram.png'/>
</div>

## Transaction Field Analysis

We will use **logistic regression** to adjust the machine learning score and better estimate the probability of fraud, since this method always outputs a value between 0 and 1, keeping the scale within the 0% to 100% range.

First, we need to calculate the Information Value (IV) for each individual column and for interactions between two fields so that we can better understand which columns are most effective at identifying fraud and use them to derive valuable insights.

IV Reference Table:

| IV | Interpretation |
| --- | --- |
| <0.1 | Weak |
| 0.1 - 0.3 | Medium / useful |
| >0.3 | Strong |

<br>

<div align='center'>
	<img width='80%' src='assets/best_columns.png'/>
</div>

<br>
<br>

<div align='center'>
	<img width='80%' src='assets/combined_IVs_table.png'/>
</div>

## Insights Deep-Dive

<div align='center'>
	<img width='80%' src='assets/fraud_over_time.png'/>
</div>
<br>

- November, December, and January consistently show higher fraud rates post-pandemic, with **fraud rates above 4%**.

- Special holidays during this season (**Black Friday, Christmas, New Year, etc.**) lead to increased sales and transaction volume, creating more opportunities for malicious actors.

- The WoE (Weight of Evidence) for transactions made between November and January is 0.8113, which increases the odds of fraud by **2.25x** compared with other periods.

<br>
<br>

<div align='center'>
	<img width='80%' src='assets/hours_bar_chart.png'/>
</div>
<br>

- More people make purchases during **lunch breaks and throughout the workday**, giving fraudsters more legitimate transactions to hide among.

- Transactions made in the afternoon often look ordinary. **A purchase at 2 PM is typically less suspicious than one at 3 AM**.

- **Fraud rings often operate during standard working hours**, when customer service teams, mule accounts, and collaborators are active and can respond quickly if issues arise.

- The WoE is 0.6016, increasing the odds of fraud by around **83%**.

<br>
<br>

<div align='center'>
	<img width='80%' src='assets/heatmap.png'/>
</div>
<br>

- Fraud detection can become more precise when two or more fields are present in a transaction. When both fields are high risk, it is unsurprising that fraud rates increase when they are combined.

- The WoE is 1.4361, increasing the odds of fraud by around **4.2x**, which performs better than flagging each indicator individually.

<br>
<br>

<div align='center'>
	<img width='80%' src='assets/merchant_category_bar_chart.png'/>
</div>
<br>

- Digital goods such as gift cards, gaming credits, software licenses, and subscriptions are delivered immediately, giving fraudsters **little time to stop**.

- Flights, hotels, and vacation packages can generate **large profits** from a single successful fraud attempt, which helps explain why the travel category shows these numbers.

- High-value products such as smartphones, laptops, and designer goods can be **converted into cash** relatively easily.

- The WoE is 0.5786, increasing the odds of fraud by around **78%**.

<br>
<br>

<div align='center'>
	<img width='80%' src='assets/channel_bar_chart.png'/>
</div>
<br>

- Fraud rates increase as transactions move farther away from physical possession and rely more heavily on digital identity.

- Traditional channels tend to involve stronger friction and verification.

- Mobile app fraud is frequently linked to account takeover.

- The WoE is 0.3398, increasing the odds of fraud by **40%**.

<br>
<br>

<div align='center'>
	<img width='80%' src='assets/transaction_amount_table.png'/>
</div>
<br>

- Larger transactions are more attractive to fraudsters because they are less common than low-value transactions.

- Although these transactions are more routine and concentrate higher volume, malicious actors appear to find them worthwhile.

- Risk often increases outside the normal spending band.

- The WoE is -1.6775, reducing the odds of fraud by **81%**.

## Final Results

After analyzing these fields and obtaining the best logit values based on Weight of Evidence calculations, we can turn this information into conditional features that, when met by a transaction, can increase or decrease its likelihood of being fraudulent.

The next step is to determine the best threshold for classifying a transaction as legitimate or fraudulent. The focus is on reducing false positive rates and total fraud-related costs.

It is worth noting that:

> [!NOTE]
> Higher thresholds naturally decrease false positive rates, but they may also increase false negatives, which significantly raises costs because failing to catch actual fraud reduces the chances of recovering funds and may lead to chargebacks of 100% or more.

<br>

The results are shown below:

<div align='center'>
	<img width='80%' src='assets/best_threshold.png'/>
</div>

<br>

This threshold was carefully chosen because it **reduces costs to under $400K and keeps fraud rates below 1%**.

<br>

<table>
	<tr>
		<td>
			<img src='assets/before_confusion_matrix.png'/>
		</td>
		<td>
			<img src='assets/after_model_adjustments_confusion_matrix.png'/>
		</td>
	</tr>
</table>

<br>

<div align='center'>
	<img width='80%' src='assets/final_comparison.png'/>
</div>

## Key Takeaways and Recommendations

For the Fraud Strategy team:

- Use logistic regression as the main method for adjusting and testing fraud detection approaches.

- Pay particular attention to the following fields: transaction month, hour, merchant category, channel, and transaction USD amount, as these columns offer higher precision and accuracy when flagging fraud activity.

- Use these logit values as a reference for calibrating flagging rules:

| Columns | Conditions | Logit |
| --- | --- | --- |
| Transaction month | November, December, and January | 0.8113 |
| Transaction hour | Between 12 PM and 5 PM | 0.6016 |
| Month + hour | Risky month and risky hours as previously described | 1.4361 |
| Merchant category | High-value retail, travel, and digital goods | 0.5786 |
| Channel | Virtual card, fake mobile app, mobile app, and SIM swap | 0.3398 |
| Transaction USD amount | Between $0.51 and $832.03 | -1.6775 |

> [!WARNING]
> Use these parameters only as a general reference, since they were the ones that produced better results during testing.

<br>

- Closely monitor key KPIs every month (FPR and total costs) and adjust parameters to improve future results.
- Avoid overfitting with too many features and conditions, as this can seriously hurt detection performance on future, rapidly changing data.

## Notes

This is a portfolio project using synthetic, AI-generated data to simulate a real-life fraud analytics scenario. GacelaPay is a fictional company shown only for portfolio purposes.

Technologies used:

- SQL
- Python (Matplotlib, Pandas, NumPy, DuckDB, etc.)
- Tableau

Python package versions:

| Package | Version |
| --- | --- |
| duckdb | 1.5.0 |
| gender-guesser | 0.4.0 |
| matplotlib | 3.10.8 |
| openpyxl | 3.1.5 |
| pip | 26.0.1 |
| pycountry | 26.2.16 |
| scikit-learn | 1.8.0 |
| xlwings | 0.33.20 |
| yfinance | 1.2.0 |
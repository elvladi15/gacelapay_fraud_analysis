<div align='center'>
	<h1>Transaction Fraud Analysis Report</h1>
</div>

<div align='center'>
	<img width='30%' src='assets/gacela_pay_full_logo.png'/>
</div>

## Company Background
**GacelaPay** is a Mexico-based digital financial institution that provides payment and banking services to retail customers across Latin America and Europe, serving thousands of customers across these regions. Founded in 2018 and headquartered in Mexico City, the company has experienced rapid growth by offering a mobile-first experience focused on speed, accessibility, and low fees. It currently features over **50K** transactions.

GacelaPay's product ecosystem includes:
1. Debit accounts for everyday spending and transfers
1. Credit cards with integrated rewards programs
1. Crypto accounts that allow customers to buy, sell, and hold selected cryptocurrencies
1. Peer-to-peer and international transfers
1. Digital wallets and virtual cards for e-commerce transactions

Over the last few years, the company has been struggling with customer retention and increasing costs associated with incorrect fraud flagging, as they relied on legacy machine learning models and static thresholds that were not regularly recalibrated to evolving fraud patterns.

## Project overview

For the scope of this project, we will focus con transactions between the period of 2022 and 2025, since this has been the most underperforming range, largely due to the COVID-19 pandemic after-effects.

During these years, the company has processed **50,128** transactions, from which **977** have been confirmed to be fraudulent transactions, representing **1.95%** of total transactions.

Machine learning models analize transaction patterns over time and output a flag score that ranges between 0 and 1000, representing the probability that a given transaction is fraud. After that, the system compares this score with a fixed threshold of 700, meaning that every transaction with a score greater or equal to this threshold is flagged as fraud and blocked.

The following confusion matrix shows the flag results:

<div align='center'>
	<img width='60%' src='assets/current_confusion_matrix.png'/>
</div>
<br>

Given these values, the resulting core metrics arise:

| Metric | Value |
| --- | --- |
| False Positive Rate (FPR) | 3.56% |
| Fraud Detection Rate (FDR) | 61.72% |
| Precision | 25.63% |
| Accuracy | 95.76% |

Such high False Positive Rate coincides with customer churn rising over the years.

<div align='center'>
	<img width='80%' src='assets/current_fpr.png'/>
</div>
<br>

Aside from this, it's been reported that total costs associated with fraud activity and incorrect flaggings total over **$560K** dollars.

## Objective and Key Points (OKR)

Fraud Strategy and Financial department has made it clear that they need to meet the following goals:

### 1. Halve False Positive Rates by December 2026
### 2. Reduce Annual costs associated to fraud 25% by EOY 

## Stakeholder questions

### Fraud Strategy
1. What are the best fields we can use to increase system fraud detection?
1. Are there any helpful interactions between these fields?
1. Do we have to adjust the flagging threshold? if yes, which value should be used?
1. When a transaction seems to have high fraud probability, how should we scale up that probability?
1. What features and parameters are recommended to reduce FPR and total costs?

## Dataset Structure and ERD (Entity Relationship Diagram)

<div align='center'>
	<img width='80%' src='assets/entity_relationship_diagram.png'/>
</div>

## Transaction field analysis

We will utilize **logistic regression** to adjust the Machine Learning Score and better adjust probability of fraud as this method always outputs a number from 0 and 1, so that the scales don't go outside the range of 0% and 100%.

First, we need to calculate the Information Value (IV) of each of the individual columns and interaction between 2 fields, so that we have a better understanding of what columns are better at catching fraud and use them to get valuable insights.

IV value Reference table:

| IV | Interpretation |
| --- | --- |
| <0.1 | Weak |
| 0.1 - 0.3 | Medium/useful|
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

- November, december and january consistently register higher fraud post-pandemic with **fraud rates over 4%**.

- Special holidays during this season **(Black Friday, Chrismas, New Year, etc)** see an increase in sales and transaction volume, offering bigger opportunities for malicious entities to operate.

- WoE (Weight of Evidence) of transactions done between november and january is 1.4361, which increases the odds of these transactions of being fraud by **4.2x** more than the others.

<br>
<br>

<div align='center'>
	<img width='80%' src='assets/hours_bar_chart.png'/>
</div>
<br>

- More people make purchases during **lunch breaks and throughout the workday**, giving fraudsters more legitimate transactions to hide among.

- Transactions made in the afternoon look "ordinary". **A purchase at 2 PM is often less suspicious than one at 3 AM**.

- **Fraud rings often operate during standard working hours** when customer service teams, mule accounts, and collaborators are active and can respond quickly if issues arise.

- WoE: 0.6016, increasing odds by around **83%** of being fraud.

<br>
<br>
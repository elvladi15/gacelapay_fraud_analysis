# generate_fraud_dataset.py
# Run with: python generate_fraud_dataset.py
# Requires: pandas, numpy
# Install: pip install pandas numpy

import random, string, os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(42)
np.random.seed(42)

# === CONFIG ===
N_TRANSACTIONS = 50128
N_CUSTOMERS = 15960   # realistic ratio for 50k tx
N_ACCOUNTS = 19500

# === UTILS ===
def make_id(prefix, n, length=12):
    chars = string.ascii_letters + string.digits + "-_@"
    ids = set()
    while len(ids) < n:
        ids.add(prefix + ''.join(random.choices(chars, k=length)))
    return list(ids)

# === LOCATION / CURRENCY SETUP ===
# Countries chosen to concentrate fraud in: United States, Brazil, Mexico, Germany, France
COUNTRIES = [
    ("United States", "USD"),
    ("Brazil", "BRL"),
    ("Mexico", "MXN"),
    ("Germany", "EUR"),
    ("France", "EUR"),
    ("United Kingdom", "GBP"),
    ("Canada", "USD"),
    ("Spain", "EUR"),
    ("Argentina", "USD"),
    ("Colombia", "USD"),
    ("Chile", "USD"),
    ("Peru", "USD"),
    ("Netherlands", "EUR"),
    ("Italy", "EUR"),
    ("Portugal", "EUR"),
]
COUNTRY_NAMES = [c[0] for c in COUNTRIES]
COUNTRY_TO_CURRENCY = {c[0]: c[1] for c in COUNTRIES}

# === NAME POOLS (curated per-country samples) ===
FIRST_NAMES = {
    "United States": ["Liam","Noah","Oliver","Elijah","James","Emma","Olivia","Ava","Sophia","Isabella"],
    "Brazil": ["Miguel","Arthur","Heitor","Theo","Davi","Helena","Alice","Laura","Valentina","Sofia"],
    "Mexico": ["Santiago","Mateo","Sebastián","Diego","Luis","Sofía","Valeria","Camila","Lucía","María"],
    "Germany": ["Ben","Paul","Leon","Oskar","Lukas","Emma","Mia","Hannah","Sophia","Anna"],
    "France": ["Gabriel","Louis","Raphaël","Arthur","Jules","Léa","Emma","Chloé","Manon","Inès"],
    "United Kingdom": ["Oliver","George","Arthur","Noah","Harry","Olivia","Amelia","Isla","Ava","Mia"],
    "Canada": ["Liam","Noah","Jackson","Lucas","Benjamin","Olivia","Emma","Charlotte","Ava","Amelia"],
    "Spain": ["Hugo","Mateo","Martín","Lucas","Liam","Lucía","Sofía","Martina","María","Paula"],
    "Argentina": ["Santiago","Mateo","Benjamín","Thiago","Luca","Sofía","Valentina","Camila","Martina","Isabella"],
    "Colombia": ["Santiago","Mateo","Samuel","Alejandro","Juan","Sofía","Valentina","María","Isabella","Camila"],
    "Chile": ["Agustín","Benjamín","Matías","Tomás","Lucas","Isidora","Sofía","Antonia","Florencia","Camila"],
    "Peru": ["Santiago","Diego","Mateo","José","Luis","Valeria","Sofía","Camila","Isabella","María"],
    "Netherlands": ["Daan","Lucas","Levi","Noah","Finn","Emma","Sophie","Julia","Tess","Anna"],
    "Italy": ["Leonardo","Francesco","Alessandro","Lorenzo","Mattia","Sofia","Giulia","Aurora","Giorgia","Alice"],
    "Portugal": ["Martim","João","Miguel","Rodrigo","Tomás","Matilde","Maria","Beatriz","Carolina","Leonor"]
}
LAST_NAMES = {
    "United States": ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez"],
    "Brazil": ["Silva","Santos","Oliveira","Souza","Rodrigues","Ferreira","Alves","Pereira","Lima","Gomes"],
    "Mexico": ["Hernández","García","Martínez","López","González","Pérez","Sánchez","Ramírez","Torres","Flores"],
    "Germany": ["Müller","Schmidt","Schneider","Fischer","Weber","Meyer","Wagner","Becker","Schulz","Bauer"],
    "France": ["Martin","Bernard","Thomas","Petit","Robert","Richard","Durand","Dubois","Moreau","Laurent"],
    "United Kingdom": ["Smith","Jones","Taylor","Brown","Williams","Wilson","Evans","Thomas","Roberts","Johnson"],
    "Canada": ["Smith","Tremblay","Brown","Martin","Roy","Wilson","Johnson","Macdonald","Taylor","White"],
    "Spain": ["García","Martínez","López","Sánchez","Pérez","Gómez","Martín","Jiménez","Ruiz","Hernández"],
    "Argentina": ["González","Rodríguez","Gómez","Fernández","López","Martínez","Pérez","Sánchez","Romero","Torres"],
    "Colombia": ["González","Rodríguez","Gómez","Martínez","López","Pérez","Sánchez","Ramírez","Vargas","Morales"],
    "Chile": ["González","Muñoz","Rojas","Rodríguez","Soto","López","Contreras","Silva","Martínez","Pérez"],
    "Peru": ["Quispe","Flores","Gonzales","Torres","Huaman","Pérez","Ramírez","Guzmán","Salazar","Rojas"],
    "Netherlands": ["de Jong","Jansen","de Vries","van den Berg","Bakker","Janssen","Visser","Smit","Meijer","de Boer"],
    "Italy": ["Rossi","Russo","Ferrari","Esposito","Bianchi","Romano","Colombo","Ricci","Marino","Greco"],
    "Portugal": ["Silva","Santos","Ferreira","Pereira","Oliveira","Costa","Rodrigues","Martins","Jesus","Sousa"]
}

# Gender proportions: 48% Male, 50% Female, 2% Non-Binary
GENDERS = ["Male","Female","Non-Binary"]
GENDER_PROBS = [0.48, 0.50, 0.02]

# Merchant categories & channels (fraud biases will use these)
MERCHANT_CATEGORIES = [
    "digital_goods","travel","high_value_retail","groceries","utilities","entertainment",
    "dining","pharmacy","p2p_transfer","telecom","gas_station"
]
CHANNELS = [
    "mobile_app","web","pos_physical_card","virtual_card","atm","p2p","fake_mobile_app","sim_swap","call_center"
]

# === GENERATE IDs ===
customer_ids = make_id("CUST_", N_CUSTOMERS, length=10)
account_ids = make_id("ACCT_", N_ACCOUNTS, length=10)
transaction_ids = make_id("TXN_", N_TRANSACTIONS, length=12)

# === CUSTOMERS ===
# Age distribution: gaussian centered near mid-40s (makes 42-52 common)
ages = np.clip(np.random.normal(loc=47, scale=9, size=N_CUSTOMERS).round().astype(int), 18, 90)

# Customer since: random between 2015-01-01 and 2025-03-01
start_cs = datetime(2015,1,1)
end_cs = datetime(2025,3,1)
def random_dates_list(n, start, end):
    start_u = int(start.timestamp())
    end_u = int(end.timestamp())
    return [datetime.fromtimestamp(int(random.uniform(start_u, end_u))) for _ in range(n)]
customer_since = random_dates_list(N_CUSTOMERS, start_cs, end_cs)

# Credit limits and CLV (skewed log-normal and proportional)
credit_limits = np.round(np.random.lognormal(mean=7.5, sigma=0.9, size=N_CUSTOMERS)).astype(int)
clv = np.round(credit_limits * np.random.uniform(0.5, 50.0, size=N_CUSTOMERS)).astype(int)

# Country assignment: bias to fraud-prone countries
country_weights = [3.0 if c[0] in {"United States","Brazil","Mexico","Germany","France"} else 1.0 for c in COUNTRIES]
country_weights = np.array(country_weights) / np.sum(country_weights)
customer_country = np.random.choice(COUNTRY_NAMES, size=N_CUSTOMERS, p=country_weights)

customers = pd.DataFrame({
    "ID": customer_ids,
    "FIRST_NAME": [random.choice(FIRST_NAMES[c]) for c in customer_country],
    "LAST_NAME":  [random.choice(LAST_NAMES[c]) for c in customer_country],
    "AGE": ages,
    "GENDER": np.random.choice(GENDERS, size=N_CUSTOMERS, p=GENDER_PROBS),
    "COUNTRY": customer_country,
    "CUSTOMER_SINCE": [d.strftime("%Y-%m-%d") for d in customer_since],
    "CREDIT_LIMIT": credit_limits,
    "CUSTOMER_LIFETIME_VALUE": clv
})
# Ensure basic capitalization rules (only first letter capitalized)
customers["FIRST_NAME"] = customers["FIRST_NAME"].str.capitalize()
customers["LAST_NAME"] = customers["LAST_NAME"].str.replace(r" +", " ", regex=True)

# === ACCOUNTS ===
# Choose account owners (some customers will get multiple accounts)
chosen_customers_for_accounts = np.random.choice(customer_ids, size=N_ACCOUNTS, replace=True)
accounts = pd.DataFrame({"ID": account_ids, "CUSTOMER_ID": chosen_customers_for_accounts})

def account_currency_for_customer(cid):
    rows = customers.loc[customers["ID"]==cid, "COUNTRY"].values
    if len(rows) == 0:
        return random.choice(["USD","EUR","GBP","MXN","BRL"])
    country = rows[0]
    if random.random() < 0.8:
        return COUNTRY_TO_CURRENCY.get(country, random.choice(["USD","EUR","GBP","MXN","BRL"]))
    else:
        return random.choice(["USD","EUR","GBP","MXN","BRL"])

account_types = ["wallet","savings","checking","credit","virtual_wallet"]
statuses = ["Active","Inactive","Blocked"]

accounts["TYPE"] = [random.choice(account_types) for _ in range(N_ACCOUNTS)]
accounts["CURRENCY"] = [account_currency_for_customer(cid) for cid in accounts["CUSTOMER_ID"]]

balances = []
open_dates = []
for t in accounts["TYPE"]:
    if t == "wallet":
        bal = int(max(0, np.random.normal(300, 600)))
    elif t == "virtual_wallet":
        bal = int(max(0, np.random.normal(200, 400)))
    elif t == "savings":
        bal = int(max(0, np.random.normal(3000, 4000)))
    elif t == "checking":
        bal = int(max(0, np.random.normal(1200, 2000)))
    elif t == "credit":
        bal = int(max(0, np.random.normal(5000, 8000)))
    balances.append(bal)
    od = random.choice(customer_since) + timedelta(days=random.randint(0, 2000))
    open_dates.append(od.strftime("%Y-%m-%d"))

accounts["BALANCE"] = balances
accounts["OPEN_DATE"] = open_dates
accounts["STATUS"] = [random.choices(statuses, weights=[0.85,0.10,0.05])[0] for _ in range(N_ACCOUNTS)]

# === TRANSACTIONS ===
start_tx = datetime(2022,1,1)
end_tx = datetime(2025,12,31,23,59,59)
def rand_ts(n, start, end):
    s = int(start.timestamp()); e = int(end.timestamp())
    return [datetime.fromtimestamp(int(random.randint(s, e))) for _ in range(n)]

tx_timestamps = rand_ts(N_TRANSACTIONS, start_tx, end_tx)

active_account_ids = [aid for aid, st in zip(accounts["ID"], accounts["STATUS"]) if st=="Active"]
tx_account_ids = [random.choice(active_account_ids) for _ in range(N_TRANSACTIONS)]

# Amounts: mixture of exponentials to create long tail
n1 = int(N_TRANSACTIONS * 0.75)
n2 = int(N_TRANSACTIONS * 0.20)
n3 = N_TRANSACTIONS - n1 - n2
amounts_parts = list(np.random.exponential(scale=30, size=n1)) + list(np.random.exponential(scale=200, size=n2)) + list(np.random.exponential(scale=1000, size=n3))
amounts = [round(a + 1.0, 2) for a in amounts_parts[:N_TRANSACTIONS]]

acct_currency_map = dict(zip(accounts["ID"], accounts["CURRENCY"]))
tx_currencies = [acct_currency_map.get(aid, random.choice(["USD","EUR","GBP","MXN","BRL"])) if random.random() < 0.85 else random.choice(["USD","EUR","GBP","MXN","BRL"]) for aid in tx_account_ids]

tx_merchants = [random.choices(MERCHANT_CATEGORIES, weights=[0.10,0.08,0.07,0.20,0.08,0.07,0.10,0.05,0.10,0.08,0.07])[0] for _ in range(N_TRANSACTIONS)]
tx_channels = [random.choices(CHANNELS, weights=[0.30,0.20,0.15,0.10,0.05,0.08,0.05,0.04,0.03])[0] for _ in range(N_TRANSACTIONS)]
acct_owner = dict(zip(accounts["ID"], accounts["CUSTOMER_ID"]))
cust_country_map = dict(zip(customers["ID"], customers["COUNTRY"]))
tx_countries = [cust_country_map.get(acct_owner.get(aid, ""), random.choice(COUNTRY_NAMES)) for aid in tx_account_ids]

tx_rows = {
    "ID": transaction_ids,
    "ACCOUNT_ID": tx_account_ids,
    "TIMESTAMP": [t.strftime("%Y-%m-%d %H:%M:%S") for t in tx_timestamps],
    "AMOUNT": amounts,
    "CURRENCY": tx_currencies,
    "MERCHANT_CATEGORY": tx_merchants,
    "CHANNEL": tx_channels,
    "COUNTRY": tx_countries
}
transactions = pd.DataFrame(tx_rows)

# === FRAUD SELECTION (exact target proportion, but weighted by time/merchant/channel/country) ===
target_fraud_count = int(round(0.0195 * N_TRANSACTIONS))  # ~1.95%
weights = np.ones(N_TRANSACTIONS, dtype=float)

for i, ts in enumerate(pd.to_datetime(transactions["TIMESTAMP"])):
    w = 1.0
    # Month bias: Jan, Nov, Dec
    if ts.month in [1, 11, 12]:
        w *= 3.5
    # Day-of-week bias: Monday (0) & Friday (4)
    if ts.weekday() in [0, 4]:
        w *= 2.0
    # Hour bias: 12:00-17:00 (12-17)
    if 12 <= ts.hour <= 17:
        w *= 2.5
    # Merchant bias
    if transactions.at[i, "MERCHANT_CATEGORY"] in ["digital_goods", "travel", "high_value_retail"]:
        w *= 2.5
    # Channel bias
    if transactions.at[i, "CHANNEL"] in ["mobile_app", "fake_mobile_app", "sim_swap", "virtual_card"]:
        w *= 2.5
    # Country bias
    if transactions.at[i, "COUNTRY"] in ["United States", "Brazil", "Mexico", "Germany", "France"]:
        w *= 1.5
    weights[i] = w

weights = weights / np.sum(weights)
fraud_indices = np.random.choice(np.arange(N_TRANSACTIONS), size=target_fraud_count, replace=False, p=weights)
is_fraud = np.zeros(N_TRANSACTIONS, dtype=int)
is_fraud[fraud_indices] = 1
transactions["IS_FRAUD"] = is_fraud

# === FRAUD_DECISIONS (ML) ===
# ML score distribution chosen to make model imperfect:
# - True fraud: mean ~750, sd ~240  (so some missed)
# - Non-fraud: mean ~300, sd ~220 (so some false positives)
ml_scores = []
for f in transactions["IS_FRAUD"]:
    if f == 1:
        s = int(np.clip(np.random.normal(750, 240), 0, 1000))
    else:
        s = int(np.clip(np.random.normal(300, 220), 0, 1000))
    ml_scores.append(s)

fraud_decisions = pd.DataFrame({
    "ID": make_id("FD_", N_TRANSACTIONS, length=12),
    "TRANSACTION_ID": transactions["ID"],
    "ML_SCORE": ml_scores
})
fraud_decisions["THRESHOLD"] = 700
fraud_decisions["FLAGGED"] = (fraud_decisions["ML_SCORE"] > fraud_decisions["THRESHOLD"]).astype(int)
fraud_decisions["DECISION_TIME"] = np.random.randint(20, 2000, size=N_TRANSACTIONS)  # ms

# === FRAUD_COSTS ===
# Only filled when ML catches fraud (i.e., FLAGGED == 1 and IS_FRAUD == 1).
# Investigation/support costs scale with amount; lost interchange approximated at 2% plus small noise
investigation_cost = np.zeros(N_TRANSACTIONS, dtype=float)
customer_support_cost = np.zeros(N_TRANSACTIONS, dtype=float)
lost_interchange = np.zeros(N_TRANSACTIONS, dtype=float)

for i, row in transactions.iterrows():
    if (transactions.at[i, "IS_FRAUD"] == 1) and (fraud_decisions.at[i, "FLAGGED"] == 1):
        amt = float(transactions.at[i, "AMOUNT"])
        investigation_cost[i] = round(random.uniform(50, 150) + 0.005 * amt, 2)
        customer_support_cost[i] = round(random.uniform(20, 80) + 0.002 * amt, 2)
        lost_interchange[i] = round(0.02 * amt + random.uniform(0,5.0), 2)

fraud_costs = pd.DataFrame({
    "TRANSACTION_ID": transactions["ID"],
    "INVESTIGATION_COST": investigation_cost,
    "CUSTOMER_SUPPORT_COST": customer_support_cost,
    "LOST_INTERCHANGE": lost_interchange
})

# === QA and SAVE ===
# Basic uniqueness checks
assert customers["ID"].is_unique
assert accounts["ID"].is_unique
assert transactions["ID"].is_unique
assert fraud_decisions["TRANSACTION_ID"].is_unique
assert fraud_costs["TRANSACTION_ID"].is_unique

def generate_synthetic_dataset(output_dir):
	# Save CSVs
	os.makedirs(output_dir, exist_ok=True)
	customers.to_csv(os.path.join(output_dir, "customers.csv"), index=False)
	accounts.to_csv(os.path.join(output_dir, "accounts.csv"), index=False)
	transactions.to_csv(os.path.join(output_dir, "transactions.csv"), index=False)
	fraud_decisions.to_csv(os.path.join(output_dir, "fraud_decisions.csv"), index=False)
	fraud_costs.to_csv(os.path.join(output_dir, "fraud_costs.csv"), index=False)

	# Print summary so you know what was created
	print("Wrote CSVs to", os.path.abspath(output_dir))
	print(f"Customers: {len(customers)}, Accounts: {len(accounts)}, Transactions: {len(transactions)}")
	print(f"Target fraud count (1.95%): {int(sum(transactions['IS_FRAUD']))}")
	print(f"Flagged by ML (ML_SCORE > 700): {int(fraud_decisions['FLAGGED'].sum())}")
import os
from misc.utils import generate_exchange_rates

os.makedirs('project/UNCLEANED_CURRENCY_EXCHANGE_RATES', exist_ok=True)

generate_exchange_rates()
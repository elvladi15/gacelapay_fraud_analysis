import os
from misc.utils import generate_exchange_rates

if not os.path.isdir('project/UNCLEANED_CURRENCY_EXCHANGE_RATES'):
	os.makedirs('project/UNCLEANED_CURRENCY_EXCHANGE_RATES')
	generate_exchange_rates()
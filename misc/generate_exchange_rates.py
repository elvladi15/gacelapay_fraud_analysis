import os
from misc.utils import generate_exchange_rates

if not os.path.isdir('project/UNCLEAN_DATASETS/UNCLEAN_CURRENCY_EXCHANGE_RATES'):
	os.makedirs('project/UNCLEAN_DATASETS/UNCLEAN_CURRENCY_EXCHANGE_RATES')
	generate_exchange_rates()
import xlwings as xw
import duckdb
import os
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

def generate_exchange_rate(forex_pair):
	start_date = date(2022, 1, 1)
	end_date = date(2025, 12, 31)

	data = yf.download(forex_pair + '=X', start=start_date, end=end_date + timedelta(days=1), interval='1d')

	df = data[['Open']].copy()

	full_range = pd.date_range(start=start_date, end=end_date, freq='D')

	df = df.reindex(full_range)

	df['Open'] = df['Open'].bfill()

	df.to_csv('project/UNCLEAN_CURRENCY_EXCHANGE_RATES/' + forex_pair + '_RATES.csv')

def generate_exchange_rates():
	exchange_rates = ['BRLMXN', 'EURBRL', 'EURMXN', 'EURUSD', 'GBPBRL', 'GBPEUR', 'GBPMXN', 'GBPUSD', 'USDBRL', 'USDMXN']

	for exchange_rate in exchange_rates:
		generate_exchange_rate(exchange_rate)

def output_query_result_from_sql(sql_query_path):
	sql_file = Path(sql_query_path)

	output_file = Path('misc/QUERY_RESULTS.xlsx')
	
	if os.path.exists(output_file):
		wb = xw.Book(output_file)
		wb.save(output_file)
	else:
		wb = xw.Book()

	sheet =  wb.sheets[0]

	sql_query= open(sql_file, 'r').read()

	df = duckdb.sql(sql_query).df()

	sheet.clear_contents()

	sheet.range('A1').options(index=False).value = df

	sheet.used_range.api.AutoFilter(Field:=1) 

	sheet.autofit(axis='columns') 

	wb.api.RefreshAll()

	wb.save(output_file)
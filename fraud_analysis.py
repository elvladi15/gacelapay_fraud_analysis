import duckdb
from pathlib import Path

sql_file = Path('project/SQL/GET_DF_STATISTICS.sql')

sql_query = open(sql_file, 'r').read()

total_usd_fees_amount, total_costs, *rest = duckdb.sql(sql_query).fetchone()

print(total_usd_fees_amount)
print(total_costs)
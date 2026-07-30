from dashboard.utils.db import *

print(get_companies().head())

print(get_financial_ratios().head())

print(get_market_cap().head())

print(get_stock_prices().head())
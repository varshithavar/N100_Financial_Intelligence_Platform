from dashboard.utils.db import (
    get_companies,
    get_financial_ratios,
    get_market_cap,
    get_peer_groups,
    get_sectors,
    get_stock_prices,
)

print("===== Companies =====")
print(get_companies().head())

print("\n===== Financial Ratios =====")
print(get_financial_ratios().head())

print("\n===== Market Cap =====")
print(get_market_cap().head())

print("\n===== Peer Groups =====")
print(get_peer_groups().head())

print("\n===== Sectors =====")
print(get_sectors().head())

print("\n===== Stock Prices =====")
print(get_stock_prices().head())
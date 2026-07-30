from src.dashboard.utils.db import (
    get_total_companies,
    get_companies,
    get_ratios
)


print("========== Dashboard DB Test ==========")


print("\nTotal Companies:")
total = get_total_companies()
print(total)


print("\nCompanies:")
companies = get_companies()
print(companies)


print("\nRatios:")
ratios = get_ratios()
print(ratios.head())


print("\n========== Test Completed Successfully ==========")
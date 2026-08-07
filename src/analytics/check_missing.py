import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

print("===== Profit Loss (Company 10) =====")
print(pd.read_sql("""
SELECT financial_year
FROM profit_loss
WHERE company_id = 10
""", conn))

print("===== Balance Sheet (Company 10) =====")
print(pd.read_sql("""
SELECT financial_year
FROM balance_sheet
WHERE company_id = 10
""", conn))

print("===== Cash Flow (Company 10) =====")
print(pd.read_sql("""
SELECT financial_year
FROM cash_flow
WHERE company_id = 10
""", conn))

print("===== Balance Sheet (Company 78) =====")
print(pd.read_sql("""
SELECT financial_year
FROM balance_sheet
WHERE company_id = 78
""", conn))

print("===== Cash Flow (Company 78) =====")
print(pd.read_sql("""
SELECT financial_year
FROM cash_flow
WHERE company_id = 78
""", conn))

conn.close()
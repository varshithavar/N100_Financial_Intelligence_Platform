import pandas as pd

for f in ["output/screener_output.xlsx", "output/peer_comparison.xlsx"]:
    print(f"\nChecking: {f}")
    try:
        xls = pd.ExcelFile(f)
        print("Workbook is valid.")
        print("Sheets:", xls.sheet_names)
    except Exception as e:
        print("Error:", e)
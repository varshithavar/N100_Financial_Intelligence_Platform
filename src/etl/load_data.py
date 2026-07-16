import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Database
DB_PATH = BASE_DIR / "database" / "nifty100.db"
engine = create_engine(f"sqlite:///{DB_PATH}")


def load_excel_to_db(file_path, table_name):
    df = pd.read_excel(file_path)

    # Companies
    if table_name == "companies":
        df = df.rename(columns={
            "ticker": "symbol",
            "sector_id": "sector"
        })

        if "industry" not in df.columns:
            df["industry"] = None

    # Profit & Loss
    elif table_name == "profit_loss":
        df = df.rename(columns={
            "year": "financial_year",
            "sales": "revenue"
        })

        if "eps" not in df.columns:
            df["eps"] = None

    # Balance Sheet
    elif table_name == "balance_sheet":
        df = df.rename(columns={
            "year": "financial_year",
            "assets": "total_assets",
            "liabilities": "total_liabilities"
        })

        if "equity" not in df.columns:
            df["equity"] = None

    # Cash Flow
    elif table_name == "cash_flow":
        df = df.rename(columns={
            "year": "financial_year",
            "operating_cashflow": "operating_cf"
        })

        if "investing_cf" not in df.columns:
            df["investing_cf"] = None

        if "financing_cf" not in df.columns:
            df["financing_cf"] = None

    # Prices
    elif table_name == "prices":
        df = df.rename(columns={
            "date": "trade_date"
        })

        for col in ["open_price", "high_price", "low_price", "volume"]:
            if col not in df.columns:
                df[col] = None

    # Ratios
    elif table_name == "ratios":
        df = df.rename(columns={
            "pe": "pe_ratio"
        })

        if "financial_year" not in df.columns:
            df["financial_year"] = None

        if "debt_equity" not in df.columns:
            df["debt_equity"] = None

    print(f"Loading {table_name} ({len(df)} rows)")

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"✓ Loaded {table_name}")


def main():
    files = {
        "data/raw/companies.xlsx": "companies",
        "data/raw/profitandloss.xlsx": "profit_loss",
        "data/raw/balancesheet.xlsx": "balance_sheet",
        "data/raw/cashflow.xlsx": "cash_flow",
        "data/raw/stock_prices.xlsx": "prices",
        "data/raw/financial_ratios.xlsx": "ratios",
        "data/raw/sectors.xlsx": "sector",
    }

    for file_path, table_name in files.items():
        load_excel_to_db(file_path, table_name)

    print("\nAll data loaded successfully!")


if __name__ == "__main__":
    main()
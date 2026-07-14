PRAGMA foreign_keys = ON;

-- ===========================
-- 1. Companies
-- ===========================
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    symbol TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    sector TEXT,
    industry TEXT
);

-- ===========================
-- 2. Profit & Loss
-- ===========================
CREATE TABLE IF NOT EXISTS profit_loss (
    pl_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    financial_year INTEGER,
    revenue REAL,
    net_profit REAL,
    eps REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- ===========================
-- 3. Balance Sheet
-- ===========================
CREATE TABLE IF NOT EXISTS balance_sheet (
    bs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    financial_year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    equity REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- ===========================
-- 4. Cash Flow
-- ===========================
CREATE TABLE IF NOT EXISTS cash_flow (
    cf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    financial_year INTEGER,
    operating_cf REAL,
    investing_cf REAL,
    financing_cf REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- ===========================
-- 5. Stock Prices
-- ===========================
CREATE TABLE IF NOT EXISTS prices (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    trade_date DATE,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- ===========================
-- 6. Ratios
-- ===========================
CREATE TABLE IF NOT EXISTS ratios (
    ratio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    financial_year INTEGER,
    pe_ratio REAL,
    roe REAL,
    debt_equity REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- ===========================
-- 7. Dividends
-- ===========================
CREATE TABLE IF NOT EXISTS dividends (
    dividend_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    dividend_date DATE,
    dividend_per_share REAL,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- ===========================
-- 8. Sector
-- ===========================
CREATE TABLE IF NOT EXISTS sector (
    sector_id INTEGER PRIMARY KEY,
    sector_name TEXT UNIQUE NOT NULL
);

-- ===========================
-- 9. Market Index
-- ===========================
CREATE TABLE IF NOT EXISTS market_index (
    index_id INTEGER PRIMARY KEY AUTOINCREMENT,
    index_name TEXT,
    trade_date DATE,
    close_value REAL
);

-- ===========================
-- 10. Load Audit
-- ===========================
CREATE TABLE IF NOT EXISTS load_audit (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT,
    rows_loaded INTEGER,
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT
);
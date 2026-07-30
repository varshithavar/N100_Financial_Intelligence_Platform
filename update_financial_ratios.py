import sqlite3


DB_PATH = "database/nifty100.db"


conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


# Update ROE values
cursor.execute(
    """
    UPDATE financial_ratios
    SET return_on_equity_pct = (
        SELECT roe
        FROM ratios
        WHERE ratios.company_id = financial_ratios.company_id
    )
    """
)


# Update PE values
# (add column only if available)
try:

    cursor.execute(
        """
        ALTER TABLE financial_ratios
        ADD COLUMN pe_ratio REAL
        """

    )

except sqlite3.OperationalError:
    pass



cursor.execute(
    """
    UPDATE financial_ratios
    SET pe_ratio = (
        SELECT pe_ratio
        FROM ratios
        WHERE ratios.company_id = financial_ratios.company_id
    )
    """
)



conn.commit()

conn.close()


print("financial_ratios updated successfully")
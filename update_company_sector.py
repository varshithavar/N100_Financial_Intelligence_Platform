import sqlite3


DB = "database/nifty100.db"

conn = sqlite3.connect(DB)

cursor = conn.cursor()


# Sector IDs
# 1 = IT
# 2 = Energy
# 3 = Banking
# 4 = Finance
# 5 = Healthcare
# 6 = Automobile
# 7 = Consumer


company_sector_map = {

    # Healthcare
    "Abbott India": 5,
    "Apollo": 5,
    "Cipla": 5,
    "Dr Reddy": 5,
    "Sun Pharmaceutical": 5,
    "Divis": 5,
    "Torrent Pharmaceuticals": 5,


    # Energy
    "Adani": 2,
    "NTPC": 2,
    "Reliance": 2,
    "ONGC": 2,
    "Coal India": 2,
    "GAIL": 2,
    "Indian Oil": 2,
    "Bharat Petroleum": 2,
    "JSW Energy": 2,
    "NHPC": 2,
    "Tata Power": 2,
    "Power Grid": 2,
    "Tata Steel": 2,
    "Hindalco": 2,
    "Jindal Steel": 2,
    "JSW Steel": 2,
    "Larsen": 2,
    "Macrotech": 2,
    "DLF": 2,
    "Shree Cement": 2,


    # IT
    "Infosys": 1,
    "Tata Consultancy": 1,
    "HCL": 1,
    "Tech Mahindra": 1,
    "LTIMindtree": 1,
    "Bharti Airtel": 1,
    "Info Edge": 1,


    # Banking
    "Axis Bank": 3,
    "Bank of Baroda": 3,
    "HDFC Bank": 3,
    "ICICI Bank": 3,
    "IndusInd Bank": 3,
    "Kotak": 3,
    "State Bank": 3,
    "Punjab National Bank": 3,
    "Canara Bank": 3,


    # Finance
    "Bajaj Finance": 4,
    "Bajaj Finserv": 4,
    "Bajaj Holdings": 4,
    "Cholamandalam": 4,
    "Jio Financial": 4,
    "Life Insurance Corporation": 4,
    "LIC": 4,
    "Indian Railway Finance": 4,
    "Power Finance": 4,
    "REC": 4,
    "Shriram": 4,


    # Automobile
    "Bajaj Auto": 6,
    "Bosch": 6,
    "Eicher": 6,
    "Hero": 6,
    "Maruti": 6,
    "Mahindra": 6,
    "TVS": 6,
    "Samvardhana Motherson": 6,


    # Consumer
    "Asian Paints": 7,
    "Britannia": 7,
    "Nestle": 7,
    "ITC": 7,
    "Titan": 7,
    "Dabur": 7,
    "Pidilite": 7,
    "Ambuja": 7,
    "Godrej Consumer": 7,
    "Hindustan Unilever": 7,
    "Tata Consumer": 7,
    "Trent": 7,
    "Avenue Supermarts": 7,
    "Havells": 7,
    "Siemens": 7,
    "Bharat Electronics": 7,
    "Bharat Heavy": 7,
    "Hindustan Aeronautics": 7,
    "Grasim": 7,
    "Interglobe": 7,

    # Added missing company
    "Indian Railway Catering": 7

}


# Update company sectors

for keyword, sector_id in company_sector_map.items():

    cursor.execute(
        """
        UPDATE companies
        SET sector = ?
        WHERE company_name LIKE ?
        """,
        (
            sector_id,
            f"%{keyword}%"
        )
    )


conn.commit()


# Validation

assigned = cursor.execute(
    """
    SELECT COUNT(*)
    FROM companies
    WHERE sector IS NOT NULL
    """
).fetchone()[0]


missing = cursor.execute(
    """
    SELECT COUNT(*)
    FROM companies
    WHERE sector IS NULL
    """
).fetchone()[0]


print("Company sectors updated successfully!")
print("Assigned sectors:", assigned)
print("Missing sectors:", missing)


if missing > 0:

    print("\nMissing Companies:")

    rows = cursor.execute(
        """
        SELECT company_id, company_name
        FROM companies
        WHERE sector IS NULL
        """
    ).fetchall()

    for row in rows:
        print(row)


conn.close()
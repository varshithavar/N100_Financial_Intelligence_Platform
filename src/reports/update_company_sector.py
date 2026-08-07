import sqlite3


DB = "database/nifty100.db"


conn = sqlite3.connect(DB)

cursor = conn.cursor()


sector_mapping = {

    "IT": [
        "Infosys",
        "TCS",
        "HCL",
        "Tech Mahindra",
        "LTIMindtree"
    ],


    "Energy": [
        "Adani",
        "NTPC",
        "Power Grid",
        "Reliance",
        "ONGC",
        "Coal India",
        "GAIL",
        "Indian Oil",
        "BPCL"
    ],


    "Banking": [
        "Bank",
        "SBI",
        "HDFC",
        "ICICI",
        "IndusInd",
        "Kotak"
    ],


    "Finance": [
        "Bajaj Finance",
        "Bajaj Finserv",
        "PFC",
        "REC",
        "Shriram"
    ],


    "Healthcare": [
        "Abbott",
        "Apollo",
        "Cipla",
        "Dr Reddy",
        "Sun Pharma",
        "Divis"
    ],


    "Automobile": [
        "Auto",
        "Motors",
        "Bosch",
        "Eicher",
        "Maruti",
        "Hero"
    ],


    "Consumer": [
        "Asian Paints",
        "Britannia",
        "Nestle",
        "ITC",
        "Titan",
        "Dabur",
        "Pidilite"
    ]

}



for sector, keywords in sector_mapping.items():

    sector_id = cursor.execute(
        """
        SELECT sector_id
        FROM sector
        WHERE sector_name = ?
        """,
        (sector,)
    ).fetchone()[0]


    for keyword in keywords:

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


print("Company sectors updated successfully!")


# Validation

print(
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM companies
        WHERE sector IS NOT NULL
        """
    ).fetchone()
)


conn.close()
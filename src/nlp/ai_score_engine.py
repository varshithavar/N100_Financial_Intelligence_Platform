import pandas as pd
from pathlib import Path


# ------------------------------------
# Paths
# ------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "output" / "company_summary.csv"
NLP_FILE = BASE_DIR / "output" / "pros_cons_generated.csv"

OUTPUT_FILE = BASE_DIR / "output" / "ai_investment_score.csv"


# ------------------------------------
# Load Data
# ------------------------------------

summary = pd.read_csv(INPUT_FILE)
nlp = pd.read_csv(NLP_FILE)


# ------------------------------------
# Calculate NLP Confidence
# ------------------------------------

nlp_score = (
    nlp.groupby("company_name")["confidence_pct"]
    .mean()
    .reset_index()
)


# ------------------------------------
# Merge Data
# ------------------------------------

df = summary.merge(
    nlp_score,
    on="company_name",
    how="left"
)


df.rename(
    columns={
        "confidence_pct": "nlp_confidence"
    },
    inplace=True
)


# ------------------------------------
# AI Score Calculation
# ------------------------------------

def calculate_score(row):

    score = 0


    # Profitability
    if row.get("return_on_equity_pct",0) >= 15:
        score += 25

    if row.get("net_profit_margin_pct",0) >= 10:
        score += 20


    # Debt
    if row.get("debt_to_equity",1) <= 0.5:
        score += 20


    # Cash Flow
    if row.get("free_cash_flow",0) > 0:
        score += 15


    # NLP Confidence
    if row.get("nlp_confidence",0) >= 75:
        score += 20


    return score



df["ai_score"] = df.apply(
    calculate_score,
    axis=1
)


# ------------------------------------
# Rating
# ------------------------------------

def rating(score):

    if score >= 80:
        return "Strong"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Moderate"

    else:
        return "Weak"


df["ai_rating"] = df["ai_score"].apply(rating)


# ------------------------------------
# Save Output
# ------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("="*50)
print("AI Investment Score Generated")
print("="*50)
print(f"Companies Processed : {len(df)}")
print(f"Saved : {OUTPUT_FILE}")
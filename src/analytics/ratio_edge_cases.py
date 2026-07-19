from src.analytics.ratio_edge_cases import initialize_log, log_edge_case
from pathlib import Path

# Create output directory if it doesn't exist
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = OUTPUT_DIR / "ratio_edge_cases.log"


def initialize_log():
    """
    Creates a fresh edge case log file.
    """
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("FINANCIAL RATIO EDGE CASES LOG\n")
        f.write("=" * 80 + "\n\n")


def classify_anomaly(company, ratio, computed, source):
    """
    Categorize anomaly based on the difference.
    """

    difference = abs(computed - source)

    # Known source issue
    if company.upper() == "TCS" and ratio == "ROE":
        return "Data Source Issue"

    if difference > 20:
        return "Data Source Issue"

    elif difference > 10:
        return "Version Difference"

    else:
        return "Formula Discrepancy"


def log_edge_case(company, year, ratio, computed, source):
    """
    Logs anomaly only if difference > 5%.
    """

    difference = abs(computed - source)

    if difference <= 5:
        return

    category = classify_anomaly(
        company,
        ratio,
        computed,
        source
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"Company      : {company}\n")
        f.write(f"Year         : {year}\n")
        f.write(f"Ratio        : {ratio}\n")
        f.write(f"Computed     : {computed:.2f}\n")
        f.write(f"Source       : {source:.2f}\n")
        f.write(f"Difference   : {difference:.2f}\n")
        f.write(f"Category     : {category}\n")
        f.write("-" * 80 + "\n")
import re


def normalize_year(year):
    """
    Convert different year formats to an integer.

    Examples:
    2024 -> 2024
    "2024" -> 2024
    "FY2024" -> 2024
    "2024-25" -> 2024
    """

    if year is None:
        return None

    year = str(year).strip()

    match = re.search(r"(20\d{2})", year)

    if match:
        return int(match.group(1))

    return None


def normalize_ticker(ticker):
    """
    Normalize stock ticker symbols.

    Examples:
    infy -> INFY
    TCS.NS -> TCS
    SBIN.BO -> SBIN
    """

    if ticker is None:
        return None

    ticker = str(ticker).strip().upper()

    ticker = ticker.replace(".NS", "")
    ticker = ticker.replace(".BO", "")

    return ticker
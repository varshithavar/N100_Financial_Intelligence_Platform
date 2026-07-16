from src.analytics.ratios import *


# -----------------------------
# Debt Equity Tests
# -----------------------------

def test_debt_free_returns_zero():

    result = debt_to_equity(
        0,
        100
    )

    assert result == 0



def test_debt_to_equity_normal():

    result = debt_to_equity(
        500,
        1000
    )

    assert result == 0.5



def test_negative_equity_returns_none():

    result = debt_to_equity(
        500,
        -100
    )

    assert result is None



# -----------------------------
# High Leverage Flag Tests
# -----------------------------

def test_high_leverage_flag():

    result = high_leverage_flag(
        6,
        "IT"
    )

    assert result is True



def test_financial_sector_no_warning():

    result = high_leverage_flag(
        8,
        "Financials"
    )

    assert result is False



# -----------------------------
# Interest Coverage Tests
# -----------------------------

def test_interest_zero_debt_free():

    icr, label = interest_coverage(
        100,
        20,
        0
    )

    assert icr is None
    assert label == "Debt Free"



def test_icr_risk():

    icr, label = interest_coverage(
        100,
        0,
        100
    )

    assert icr == 1
    assert icr_warning_flag(icr) is True



# -----------------------------
# Asset Turnover Test
# -----------------------------

def test_asset_turnover_zero_assets():

    result = asset_turnover(
        1000,
        0
    )

    assert result is None
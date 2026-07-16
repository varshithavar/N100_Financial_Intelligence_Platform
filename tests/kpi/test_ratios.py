from src.analytics.ratios import *


# -----------------------------
# Net Profit Margin Tests
# -----------------------------

def test_net_profit_margin():

    result = net_profit_margin(
        100,
        1000
    )

    assert result == 10



def test_sales_zero():

    result = net_profit_margin(
        100,
        0
    )

    assert result is None



# -----------------------------
# ROE Tests
# -----------------------------

def test_negative_equity():

    result = return_on_equity(
        100,
        -50,
        -20
    )

    assert result is None



def test_roe_normal_case():

    result = return_on_equity(
        200,
        500,
        500
    )

    assert result == 20



# -----------------------------
# ROA Tests
# -----------------------------

def test_roa_zero_assets():

    result = return_on_assets(
        100,
        0
    )

    assert result is None



# -----------------------------
# ROCE Tests
# -----------------------------

def test_roce_normal_case():

    result = return_on_capital_employed(
        300,
        500,
        300,
        200
    )

    assert result == 30



# -----------------------------
# Debt Equity Tests
# -----------------------------

def test_debt_free():

    result = debt_to_equity(
        0,
        100
    )

    assert result == 0



# -----------------------------
# OPM Cross Check Test
# -----------------------------

def test_opm_mismatch():

    result = operating_profit_margin(
        200,
        1000,
        10
    )

    assert result == 20
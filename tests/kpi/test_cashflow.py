from src.analytics.cashflow_kpis import *


# =====================================
# Day 11 - Cash Flow KPI Tests
# =====================================


# -------------------------------------
# Free Cash Flow
# -------------------------------------

def test_free_cash_flow():

    result = free_cash_flow(
        500,
        -200
    )

    assert result == 300



# -------------------------------------
# CFO Quality Score
# -------------------------------------

def test_cfo_quality_high():

    score, category = cfo_quality_score(
        [120, 150, 200],
        [100, 100, 100]
    )

    assert score > 1
    assert category == "High Quality"



def test_cfo_quality_zero_pat():

    score, category = cfo_quality_score(
        [100],
        [0]
    )

    assert score is None
    assert category is None



# -------------------------------------
# CapEx Intensity
# -------------------------------------

def test_capex_asset_light():

    value, category = capex_intensity(
        -20,
        1000
    )

    assert value == 2
    assert category == "Asset Light"



def test_capex_capital_intensive():

    value, category = capex_intensity(
        -200,
        1000
    )

    assert category == "Capital Intensive"



# -------------------------------------
# FCF Conversion
# -------------------------------------

def test_fcf_conversion():

    result = fcf_conversion_rate(
        500,
        1000
    )

    assert result == 50



def test_fcf_conversion_zero_profit():

    result = fcf_conversion_rate(
        500,
        0
    )

    assert result is None



# -------------------------------------
# Capital Allocation Pattern
# -------------------------------------

def test_capital_allocation_reinvestor():

    result = capital_allocation_pattern(
        100,
        -50,
        -20
    )

    assert result == "Reinvestor"
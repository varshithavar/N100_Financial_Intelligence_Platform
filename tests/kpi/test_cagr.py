from src.analytics.cagr import *


# -----------------------------
# Normal CAGR Tests
# -----------------------------

def test_normal_cagr():

    result = calculate_cagr(
        100,
        200,
        5
    )

    assert result["flag"] is None
    assert result["value"] == 14.87



def test_revenue_cagr():

    result = revenue_cagr(
        100,
        200,
        5
    )

    assert result["value"] == 14.87



# -----------------------------
# Edge Case Tests
# -----------------------------

def test_decline_to_loss():

    result = calculate_cagr(
        100,
        -50,
        5
    )

    assert result["value"] is None
    assert result["flag"] == "DECLINE_TO_LOSS"



def test_turnaround():

    result = calculate_cagr(
        -100,
        50,
        5
    )

    assert result["value"] is None
    assert result["flag"] == "TURNAROUND"



def test_both_negative():

    result = calculate_cagr(
        -100,
        -50,
        5
    )

    assert result["value"] is None
    assert result["flag"] == "BOTH_NEGATIVE"



def test_zero_base():

    result = calculate_cagr(
        0,
        100,
        5
    )

    assert result["value"] is None
    assert result["flag"] == "ZERO_BASE"



def test_insufficient_years():

    result = calculate_cagr(
        100,
        200,
        0
    )

    assert result["value"] is None
    assert result["flag"] == "INSUFFICIENT"



# -----------------------------
# PAT and EPS CAGR Tests
# -----------------------------

def test_pat_cagr():

    result = pat_cagr(
        200,
        400,
        5
    )

    assert result["flag"] is None



def test_eps_cagr():

    result = eps_cagr(
        20,
        40,
        5
    )

    assert result["flag"] is None



def test_negative_eps_turnaround():

    result = eps_cagr(
        -10,
        20,
        5
    )

    assert result["flag"] == "TURNAROUND"
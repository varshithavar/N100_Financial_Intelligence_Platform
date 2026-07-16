"""
CAGR Engine
Sprint 2 - Day 10

Handles Revenue, PAT and EPS CAGR calculations
with edge case handling.
"""


def calculate_cagr(start_value, end_value, years):
    """
    CAGR Formula:

    ((End / Start) ^ (1 / Years) - 1) * 100

    Returns:
    {
        "value": CAGR percentage,
        "flag": edge case flag
    }
    """

    # Insufficient years
    if years <= 0:
        return {
            "value": None,
            "flag": "INSUFFICIENT"
        }


    # Zero base case
    if start_value == 0:
        return {
            "value": None,
            "flag": "ZERO_BASE"
        }


    # Positive to Negative
    if start_value > 0 and end_value < 0:
        return {
            "value": None,
            "flag": "DECLINE_TO_LOSS"
        }


    # Negative to Positive
    if start_value < 0 and end_value > 0:
        return {
            "value": None,
            "flag": "TURNAROUND"
        }


    # Both Negative
    if start_value < 0 and end_value < 0:
        return {
            "value": None,
            "flag": "BOTH_NEGATIVE"
        }


    # Normal CAGR
    cagr = (
        (end_value / start_value)
        ** (1 / years)
        - 1
    ) * 100


    return {
        "value": round(cagr, 2),
        "flag": None
    }



def revenue_cagr(start_revenue, end_revenue, years):
    """
    Revenue CAGR
    """

    return calculate_cagr(
        start_revenue,
        end_revenue,
        years
    )



def pat_cagr(start_pat, end_pat, years):
    """
    PAT CAGR
    """

    return calculate_cagr(
        start_pat,
        end_pat,
        years
    )



def eps_cagr(start_eps, end_eps, years):
    """
    EPS CAGR
    """

    return calculate_cagr(
        start_eps,
        end_eps,
        years
    )
"""
CAGR Engine
Sprint 2 - Day 10

Handles Revenue, PAT and EPS CAGR calculations
with edge case handling.
"""

from typing import Optional, Dict


def calculate_cagr(
    start_value: Optional[float],
    end_value: Optional[float],
    years: int
) -> Dict:
    """
    CAGR Formula:

    ((End / Start) ^ (1 / Years) - 1) * 100

    Returns:
    {
        "value": CAGR percentage,
        "flag": edge case flag
    }
    """

    # Missing data
    if start_value is None or end_value is None:
        return {
            "value": None,
            "flag": "MISSING_DATA"
        }

    # Insufficient period
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

    # Normal CAGR calculation
    try:
        cagr = (
            (end_value / start_value)
            ** (1 / years)
            - 1
        ) * 100

        return {
            "value": round(cagr, 2),
            "flag": None
        }

    except Exception:
        return {
            "value": None,
            "flag": "CALCULATION_ERROR"
        }



def revenue_cagr(
    start_revenue,
    end_revenue,
    years
):
    """
    Revenue CAGR calculation
    """

    return calculate_cagr(
        start_revenue,
        end_revenue,
        years
    )



def pat_cagr(
    start_pat,
    end_pat,
    years
):
    """
    PAT CAGR calculation
    """

    return calculate_cagr(
        start_pat,
        end_pat,
        years
    )



def eps_cagr(
    start_eps,
    end_eps,
    years
):
    """
    EPS CAGR calculation
    """

    return calculate_cagr(
        start_eps,
        end_eps,
        years
    )
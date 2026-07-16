"""
Financial Ratio Engine
Sprint 2 - Day 08 & Day 09

Contains profitability, leverage and efficiency calculations.
"""


# -----------------------------
# Profitability Ratios
# -----------------------------


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin %
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100



def operating_profit_margin(
        operating_profit,
        sales,
        source_opm=None
):
    """
    Operating Profit Margin %

    Cross checks against source OPM
    """

    if sales == 0:
        return None

    calculated_opm = (
        operating_profit / sales
    ) * 100


    if source_opm is not None:

        difference = abs(
            calculated_opm - source_opm
        )

        if difference > 1:
            print(
                f"OPM mismatch: "
                f"Calculated={calculated_opm:.2f}, "
                f"Source={source_opm}"
            )

    return calculated_opm



def return_on_equity(
        net_profit,
        equity_capital,
        reserves
):
    """
    ROE %

    Returns None for negative equity
    """

    equity = equity_capital + reserves


    if equity <= 0:
        return None


    return (
        net_profit / equity
    ) * 100



def return_on_assets(
        net_profit,
        total_assets
):
    """
    ROA %
    """

    if total_assets == 0:
        return None


    return (
        net_profit / total_assets
    ) * 100



def return_on_capital_employed(
        ebit,
        equity,
        reserves,
        borrowings
):
    """
    ROCE %
    """

    capital_employed = (
        equity +
        reserves +
        borrowings
    )


    if capital_employed <= 0:
        return None


    return (
        ebit / capital_employed
    ) * 100



# -----------------------------
# Leverage Ratios
# -----------------------------


def debt_to_equity(
        borrowings,
        equity
):
    """
    Debt Equity Ratio
    """

    if borrowings == 0:
        return 0


    if equity <= 0:
        return None


    return borrowings / equity



def interest_coverage(
        operating_profit,
        other_income,
        interest
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None, "Debt Free"


    icr = (
        operating_profit +
        other_income
    ) / interest


    if icr < 1.5:
        return icr, "Risk"


    return icr, None



def net_debt(
        borrowings,
        investments
):
    """
    Net Debt
    """

    return borrowings - investments



def asset_turnover(
        sales,
        total_assets
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None


    return sales / total_assets
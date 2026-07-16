"""
Financial Ratio Engine
Sprint 2 - Day 08 & Day 09

Profitability, Leverage and Efficiency Ratios
"""


# =====================================================
# Day 08 - Profitability Ratios
# =====================================================


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin %

    Formula:
    Net Profit / Sales * 100
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

    Cross-check with source OPM
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
    Return on Equity %

    Returns None if equity <= 0
    """

    equity = (
        equity_capital +
        reserves
    )


    if equity <= 0:
        return None


    return (
        net_profit / equity
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



# =====================================================
# Day 09 - Leverage & Efficiency Ratios
# =====================================================


def debt_to_equity(
        borrowings,
        equity
):
    """
    Debt Equity Ratio

    Debt free company returns 0
    """

    if borrowings == 0:
        return 0


    if equity <= 0:
        return None


    return borrowings / equity



def high_leverage_flag(
        debt_equity,
        sector
):
    """
    High leverage warning

    D/E > 5
    Financial sector ignored
    """

    if sector == "Financials":
        return False


    if debt_equity is None:
        return False


    return debt_equity > 5



def interest_coverage(
        operating_profit,
        other_income,
        interest
):
    """
    Interest Coverage Ratio

    Returns Debt Free label
    """

    if interest == 0:
        return None, "Debt Free"


    icr = (
        operating_profit +
        other_income
    ) / interest


    return icr, None



def icr_warning_flag(icr):
    """
    Interest coverage risk flag
    """

    if icr is None:
        return False


    return icr < 1.5



def net_debt(
        borrowings,
        investments
):
    """
    Net Debt

    Borrowings - Investments
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
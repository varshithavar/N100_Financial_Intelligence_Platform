"""
Cash Flow KPI Engine
Sprint 2 - Day 11
"""


# =====================================
# Free Cash Flow
# =====================================

def free_cash_flow(
        operating_activity,
        investing_activity
):
    """
    FCF = CFO + CFI
    """

    return operating_activity + investing_activity



# =====================================
# CFO Quality Score
# =====================================

def cfo_quality_score(
        cfo_values,
        pat_values
):
    """
    Average CFO/PAT ratio
    """

    ratios = []

    for cfo, pat in zip(cfo_values, pat_values):

        if pat == 0:
            continue

        ratios.append(cfo / pat)


    if len(ratios) == 0:
        return None, None


    avg_ratio = sum(ratios) / len(ratios)


    if avg_ratio > 1:
        category = "High Quality"

    elif avg_ratio >= 0.5:
        category = "Moderate"

    else:
        category = "Accrual Risk"


    return round(avg_ratio,2), category



# =====================================
# CapEx Intensity
# =====================================

def capex_intensity(
        investing_activity,
        sales
):
    """
    CapEx / Sales %
    """

    if sales == 0:
        return None, None


    value = (
        abs(investing_activity) / sales
    ) * 100


    if value < 3:
        category = "Asset Light"

    elif value <= 8:
        category = "Moderate"

    else:
        category = "Capital Intensive"


    return round(value,2), category



# =====================================
# FCF Conversion
# =====================================

def fcf_conversion_rate(
        free_cash_flow_value,
        operating_profit
):
    """
    FCF Conversion %
    """

    if operating_profit == 0:
        return None


    return (
        free_cash_flow_value /
        operating_profit
    ) * 100



# =====================================
# Capital Allocation Pattern
# =====================================

def capital_allocation_pattern(
        cfo,
        cfi,
        cff
):

    pattern = (
        "+" if cfo > 0 else "-",
        "+" if cfi > 0 else "-",
        "+" if cff > 0 else "-"
    )


    mapping = {

        ("+","-","-"): "Reinvestor",

        ("+","-","+"): "Mixed",

        ("+","+","-"): "Liquidating Assets",

        ("+","+","+"): "Cash Accumulator",

        ("-","+","+"): "Distress Signal",

        ("-","-","+"): "Growth Funded by Debt",

        ("-","-","-"): "Pre-Revenue"
    }


    return mapping.get(
        pattern,
        "Unknown"
    )
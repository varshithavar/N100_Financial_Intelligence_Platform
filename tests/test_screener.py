from src.analytics.screener import merge_data


def test_merge_data():
    df = merge_data()

    assert len(df) > 0
    assert "roe" in df.columns
    assert "pe" in df.columns
    assert "market_cap" in df.columns
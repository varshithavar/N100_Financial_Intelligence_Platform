from src.analytics.peer_analysis import load_data


def test_peer_data():
    df = load_data()

    assert len(df) > 0
    assert "peer" in df.columns
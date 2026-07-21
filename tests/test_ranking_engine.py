from src.analytics.ranking_engine import rank_companies


def test_rank_companies():
    df = rank_companies()

    assert len(df) > 0
    assert "total_score" in df.columns
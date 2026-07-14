import pandas as pd
from src.etl.validator import validate

def test_validate_returns_dataframe():
    df = pd.DataFrame({"id": [1, 2, 3]})
    result = validate(df)
    assert isinstance(result, pd.DataFrame)

def test_null_primary_key():
    df = pd.DataFrame({"id": [1, None, 3]})
    result = validate(df)
    assert len(result) == 1

def test_duplicate_primary_key():
    df = pd.DataFrame({"id": [1, 2, 2]})
    result = validate(df)
    assert len(result) == 1
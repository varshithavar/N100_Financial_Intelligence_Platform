from src.etl.normaliser import normalize_year
from src.etl.normaliser import normalize_ticker


def test_year_integer():
    assert normalize_year(2024) == 2024


def test_year_string():
    assert normalize_year("2023") == 2023


def test_year_fy():
    assert normalize_year("FY2022") == 2022


def test_year_range():
    assert normalize_year("2021-22") == 2021


def test_year_none():
    assert normalize_year(None) is None


def test_ticker_lower():
    assert normalize_ticker("infy") == "INFY"


def test_ticker_upper():
    assert normalize_ticker("INFY") == "INFY"


def test_ticker_ns():
    assert normalize_ticker("TCS.NS") == "TCS"


def test_ticker_bo():
    assert normalize_ticker("SBIN.BO") == "SBIN"


def test_ticker_spaces():
    assert normalize_ticker(" reliance ") == "RELIANCE"


def test_ticker_none():
    assert normalize_ticker(None) is None
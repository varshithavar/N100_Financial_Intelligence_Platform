from pathlib import Path
import pandas as pd

from src.etl.loader import load_excel


def test_load_excel(tmp_path):

    df = pd.DataFrame({
        "Company": ["ABC"],
        "Year": [2024]
    })

    file_path = tmp_path / "sample.xlsx"

    df.to_excel(file_path, index=False)

    loaded = load_excel(file_path)

    assert loaded.shape == (1, 2)
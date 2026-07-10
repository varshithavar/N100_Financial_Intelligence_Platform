from pathlib import Path
import pandas as pd

RAW_FOLDER = Path("data/raw")


def load_excel(file_path):
    """
    Load a single Excel file.
    """
    return pd.read_excel(file_path)


def load_all_excel_files():
    """
    Load all Excel files from data/raw.
    """

    datasets = {}

    excel_files = list(RAW_FOLDER.glob("*.xlsx"))

    for file in excel_files:
        datasets[file.stem] = pd.read_excel(file)

    return datasets


if __name__ == "__main__":

    data = load_all_excel_files()

    print(f"Loaded {len(data)} Excel files")

    for name, df in data.items():
        print(f"{name}: {df.shape}")
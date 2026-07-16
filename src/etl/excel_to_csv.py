import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_PATH = BASE_DIR / "data" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "processed"


def convert_excel_to_csv():

    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    for file in RAW_PATH.glob("*.xlsx"):

        df = pd.read_excel(file)

        csv_name = file.stem + ".csv"

        output = PROCESSED_PATH / csv_name

        df.to_csv(output, index=False)

        print(f"{csv_name} created")


if __name__ == "__main__":
    convert_excel_to_csv()
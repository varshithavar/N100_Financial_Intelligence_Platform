import pandas as pd
import os

folders = [
    "data/raw",
    "data/supporting"
]

for folder in folders:
    print(f"\n========== {folder} ==========")

    for file in os.listdir(folder):
        if file.endswith(".xlsx"):
            path = os.path.join(folder, file)

            print(f"\nFile: {file}")

            try:
                df = pd.read_excel(path)

                print("Rows:", len(df))
                print("Columns:")
                print(df.columns.tolist())

            except Exception as e:
                print("Error:", e)
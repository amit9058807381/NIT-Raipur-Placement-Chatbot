import pandas as pd
import os

data_folder = "data"

files = os.listdir(data_folder)

print("Files found:")
for file in files:
    print(file)

print("\n" + "=" * 60)

for file in files:

    if file.endswith(".xlsx"):

        path = os.path.join(data_folder, file)

        print("\nFILE:", file)

        excel_file = pd.ExcelFile(path)

        print("Sheets:", excel_file.sheet_names)

        for sheet in excel_file.sheet_names:

            df = pd.read_excel(path, sheet_name=sheet)

            print("\nSheet:", sheet)
            print("Rows:", len(df))
            print("Columns:")

            for column in df.columns:
                print(" -", column)

            print("\nFirst 2 rows:")
            print(df.head(2).to_string(index=False))

        print("\n" + "=" * 60)
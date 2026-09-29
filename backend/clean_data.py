import pandas as pd
import os


# ============================================================
# 1. Excel file paths
# ============================================================

file_1 = "data/Interview Experience (Responses).xlsx"
file_2 = "data/OA_Interview Experience (Batch 2026).xlsx"


# ============================================================
# 2. Read Excel files
# ============================================================

df_1 = pd.read_excel(file_1)
df_2 = pd.read_excel(file_2)


# ============================================================
# 3. Function to clean column names
# ============================================================

def clean_column_name(column):

    column = str(column)

    # Remove new lines
    column = column.replace("\n", " ")

    # Remove extra spaces
    column = " ".join(column.split())

    # Rename columns to simple names
    if column.startswith("Test Pattern"):
        return "Test Pattern"

    elif column.startswith("Test Duration"):
        return "Test Duration"

    elif column.startswith("Question Topics"):
        return "Question Topics"

    elif column.startswith("Interview Duration"):
        return "Interview Duration"

    elif column.startswith("Topics Asked"):
        return "Topics Asked"

    elif column.startswith("Coding Questions Asked"):
        return "Coding Questions Asked"

    elif column.startswith("Core Subject Questions"):
        return "Core Subject Questions"

    elif column.startswith("Project Discussion"):
        return "Project Discussion"

    elif column.startswith("Miscellaneous"):
        return "Miscellaneous"

    return column


# ============================================================
# 4. Clean column names in both files
# ============================================================

df_1.columns = [
    clean_column_name(col)
    for col in df_1.columns
]

df_2.columns = [
    clean_column_name(col)
    for col in df_2.columns
]


# ============================================================
# 5. Add CTC column if missing
# ============================================================

if "CTC" not in df_2.columns:

    df_2["CTC"] = "Not Available"


# ============================================================
# 6. Add source information
# ============================================================

df_1["Source"] = "Interview Experience"

df_2["Source"] = "Batch 2026"


# ============================================================
# 7. Columns required for chatbot
# ============================================================

common_columns = [

    "Company Name",

    "CTC",

    "Test Pattern",

    "Test Duration",

    "Question Topics",

    "Interview Duration",

    "Topics Asked",

    "Coding Questions Asked",

    "Core Subject Questions",

    "Project Discussion",

    "Miscellaneous",

    "Source"
]


# ============================================================
# 8. Select only required columns
# ============================================================

df_1 = df_1[common_columns]

df_2 = df_2[common_columns]


# ============================================================
# 9. Replace empty values
# ============================================================

df_1 = df_1.fillna("Not Available")

df_2 = df_2.fillna("Not Available")


# ============================================================
# 10. Combine both datasets
# ============================================================

df = pd.concat(
    [df_1, df_2],
    ignore_index=True
)


# ============================================================
# 11. Normalize company names
# ============================================================

def normalize_company_name(name):

    # Convert to string
    name = str(name)

    # Remove hidden/non-breaking spaces
    name = name.replace("\xa0", " ")

    # Remove leading/trailing spaces
    name = name.strip()

    # Remove multiple spaces
    name = " ".join(name.split())

    # Case-insensitive comparison
    key = name.casefold()

    mapping = {

        "pine labs": "Pine Labs",

        "deloitte": "Deloitte",

        "deloitte usi": "Deloitte USI",

        "nucleusteq": "Nucleusteq",

        "pharmeasy": "Pharmeasy",

        "mphasis": "Mphasis",

        "optum": "Optum",

        "kanerika": "Kanerika",

        "intellect design arena": "Intellect Design Arena",

        "quantiphi analytics": "Quantiphi Analytics",

        "texas instruments": "Texas Instruments",

        "epam systems": "EPAM Systems",

        "qolaris data": "Qolaris Data",

        "infosys": "Infosys",

        "accenture": "Accenture"
    }

    return mapping.get(key, name)


df["Company Name"] = df["Company Name"].apply(
    normalize_company_name
)


# ============================================================
# 12. Create processed folder
# ============================================================

os.makedirs(
    "data/processed",
    exist_ok=True
)


# ============================================================
# 13. Save cleaned data
# ============================================================

output_file = "data/processed/placement_data.csv"

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)


# ============================================================
# 14. Display result
# ============================================================

print("\n" + "=" * 60)

print("DATA CLEANING COMPLETED!")

print("=" * 60)

print("\nTotal records:", len(df))

print("\nSaved to:", output_file)


print("\nRecords by source:")

print(df["Source"].value_counts())


print("\nCompanies:")

print(df["Company Name"].unique())


print("\nCompany-wise record count:")

print(df["Company Name"].value_counts())


print("\nFinal columns:")

for column in df.columns:

    print("-", column)
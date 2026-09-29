import pandas as pd


# ============================================================
# 1. Read cleaned CSV
# ============================================================

file_path = "data/processed/placement_data.csv"

df = pd.read_csv(file_path)


# ============================================================
# 2. Basic information
# ============================================================

print("=" * 60)
print("FINAL CSV VERIFICATION")
print("=" * 60)

print("\nTotal records:", len(df))

print("Total columns:", len(df.columns))


# ============================================================
# 3. Columns
# ============================================================

print("\nColumns:")

for column in df.columns:
    print("-", column)


# ============================================================
# 4. Missing values
# ============================================================

print("\nMissing values:")

print(df.isnull().sum())


# ============================================================
# 5. Company-wise records
# ============================================================

print("\nCompany-wise record count:")

print(
    df["Company Name"].value_counts()
)


# ============================================================
# 6. Source-wise records
# ============================================================

print("\nRecords by source:")

print(
    df["Source"].value_counts()
)


# ============================================================
# 7. First 3 records
# ============================================================

print("\nFirst 3 records:")

print(
    df.head(3).to_string(index=False)
)
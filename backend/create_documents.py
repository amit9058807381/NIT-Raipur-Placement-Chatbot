import pandas as pd
import os


# ============================================================
# 1. Read cleaned CSV
# ============================================================

file_path = "data/processed/placement_data.csv"

df = pd.read_csv(file_path)


# ============================================================
# 2. Create documents folder
# ============================================================

os.makedirs(
    "data/documents",
    exist_ok=True
)


# ============================================================
# 3. Convert each row into a text document
# ============================================================

documents = []

for index, row in df.iterrows():

    document = f"""
Company: {row['Company Name']}

Source: {row['Source']}

CTC: {row['CTC']}

Test Pattern:
{row['Test Pattern']}

Test Duration:
{row['Test Duration']} minutes

Question Topics:
{row['Question Topics']}

Interview Duration:
{row['Interview Duration']} minutes

Topics Asked:
{row['Topics Asked']}

Coding Questions Asked:
{row['Coding Questions Asked']}

Core Subject Questions:
{row['Core Subject Questions']}

Project Discussion:
{row['Project Discussion']}

Miscellaneous:
{row['Miscellaneous']}
""".strip()

    documents.append(document)


# ============================================================
# 4. Save documents
# ============================================================

output_file = "data/documents/placement_documents.txt"

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:

    for i, document in enumerate(documents):

        file.write(
            f"\n{'=' * 80}\n"
        )

        file.write(
            f"DOCUMENT {i + 1}\n"
        )

        file.write(
            f"{'=' * 80}\n\n"
        )

        file.write(document)

        file.write("\n\n")


# ============================================================
# 5. Display result
# ============================================================

print("\n" + "=" * 60)

print("DOCUMENT CREATION COMPLETED!")

print("=" * 60)

print("\nTotal documents:", len(documents))

print("\nSaved to:", output_file)


print("\nFirst document:")

print("=" * 60)

print(documents[0])

print("=" * 60)
document_file = "data/documents/placement_documents.txt"

with open(
    document_file,
    "r",
    encoding="utf-8"
) as file:

    text = file.read()


# Split using DOCUMENT marker instead of the ===== separator
raw_documents = text.split("DOCUMENT ")


documents = []

for document in raw_documents:

    document = document.strip()

    if document and document[0].isdigit():

        documents.append("DOCUMENT " + document)


print("Total documents:", len(documents))

print("\n" + "=" * 60)
print("FIRST DOCUMENT")
print("=" * 60)

print(documents[0])
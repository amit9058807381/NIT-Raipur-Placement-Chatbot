import chromadb

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

# Get collection
collection = chroma_client.get_collection(
    name="placement_documents"
)

# Get first 3 documents
results = collection.get(
    limit=3
)

print("\n" + "=" * 60)
print("CHROMADB DOCUMENT CHECK")
print("=" * 60)

for i, document in enumerate(results["documents"]):

    print(f"\n--- Document {i + 1} ---")
    print(document)
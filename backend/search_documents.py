import os

from dotenv import load_dotenv
from google import genai
import chromadb


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    exit()


# ============================================================
# 2. Create Gemini client
# ============================================================

client = genai.Client(
    api_key=api_key
)


# ============================================================
# 3. Connect to existing ChromaDB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)


# ============================================================
# 4. Get collection
# ============================================================

collection = chroma_client.get_collection(
    name="placement_documents"
)


# ============================================================
# 5. User query
# ============================================================

query = "What coding questions were asked in Pine Labs?"


# ============================================================
# 6. Convert query into embedding
# ============================================================

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=query
)

query_embedding = response.embeddings[0].values


# ============================================================
# 7. Search ChromaDB
# ============================================================

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)


# ============================================================
# 8. Display results
# ============================================================

print("\n" + "=" * 60)

print("SEARCH QUERY")

print("=" * 60)

print(query)


print("\n" + "=" * 60)

print("RELEVANT DOCUMENTS")

print("=" * 60)


for i, document in enumerate(results["documents"][0]):

    print(f"\n--- Result {i + 1} ---\n")

    print(document)
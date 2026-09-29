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
# 3. Connect to ChromaDB
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
# 5. User question
# ============================================================

query = "What coding questions were asked in Pine Labs?"


# ============================================================
# 6. Convert question into embedding
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
# 8. Combine retrieved documents
# ============================================================

context = "\n\n".join(
    results["documents"][0]
)


# ============================================================
# 9. Create RAG prompt
# ============================================================

prompt = f"""
You are a placement interview assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer is not available in the context,
say that the information is not available.

Do not invent or assume information.

Context:
{context}

User Question:
{query}

Answer clearly and concisely.
"""


# ============================================================
# 10. Generate answer using Gemini
# ============================================================

answer = client.models.generate_content(
   model="gemini-3.1-flash-lite",
    contents=prompt
)


# ============================================================
# 11. Display answer
# ============================================================

print("\n" + "=" * 60)
print("USER QUESTION")
print("=" * 60)

print(query)

print("\n" + "=" * 60)
print("RAG ANSWER")
print("=" * 60)

print(answer.text)
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
# 3. Create ChromaDB client
# ============================================================

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)


# ============================================================
# 4. Delete old collection
# ============================================================

try:

    chroma_client.delete_collection(
        name="placement_documents"
    )

    print("Old collection deleted.")

except Exception:

    print("No old collection found.")


# ============================================================
# 5. Create fresh collection
# ============================================================

collection = chroma_client.create_collection(
    name="placement_documents"
)


# ============================================================
# 6. Read documents
# ============================================================

document_file = "data/documents/placement_documents.txt"

with open(
    document_file,
    "r",
    encoding="utf-8"
) as file:

    text = file.read()


# ============================================================
# 7. Split documents correctly
# ============================================================

raw_documents = text.split("DOCUMENT ")

documents = []

for document in raw_documents:

    document = document.strip()

    if document and document[0].isdigit():

        documents.append(
            "DOCUMENT " + document
        )


print("\nTotal documents:", len(documents))


# ============================================================
# 8. Generate embeddings and store documents
# ============================================================

for index, document in enumerate(documents):

    # --------------------------------------------------------
    # Generate embedding using Gemini
    # --------------------------------------------------------

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=document
    )

    embedding = response.embeddings[0].values


    # --------------------------------------------------------
    # Store document in ChromaDB
    # --------------------------------------------------------

    collection.add(
        ids=[f"document_{index}"],
        documents=[document],
        embeddings=[embedding]
    )


    print(
        f"Stored document {index + 1}/{len(documents)}"
    )


# ============================================================
# 9. Final information
# ============================================================

print("\n" + "=" * 60)

print("CHROMADB CREATION COMPLETED!")

print("=" * 60)

print(
    "Total documents stored:",
    collection.count()
)

print(
    "Database location:",
    "chroma_db"
)
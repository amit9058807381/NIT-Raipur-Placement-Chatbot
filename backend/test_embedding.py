import os

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()


# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    exit()


print("API key loaded successfully!")


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


# Test embedding
response = client.models.embed_content(
    model="gemini-embedding-001",
    contents="Pine Labs interview asked DSA and DBMS questions."
)


print("\nEmbedding generated successfully!")

print("Embedding length:", len(response.embeddings[0].values))

print("First 5 values:")
print(response.embeddings[0].values[:5])
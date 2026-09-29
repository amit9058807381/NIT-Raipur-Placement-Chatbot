import os

from dotenv import load_dotenv
from google import genai


# Load .env file
load_dotenv()


# Get API key
api_key = os.getenv("GEMINI_API_KEY")


# Check API key
if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    exit()


print("API key loaded successfully!")


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


# Test Gemini
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say hello in one sentence."
)


print("\nGemini response:")
print(response.text)
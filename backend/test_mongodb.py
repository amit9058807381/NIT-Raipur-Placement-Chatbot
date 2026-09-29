import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

mongodb_uri = os.getenv("MONGODB_URI")

if not mongodb_uri:
    print("ERROR: MONGODB_URI not found!")
    exit()


try:
    client = MongoClient(mongodb_uri)

    # Test connection
    client.admin.command("ping")

    database = client["placement_chatbot"]

    print("MongoDB connected successfully!")
    print("Database:", database.name)

except Exception as e:
    print("MongoDB connection failed!")
    print("Error:", e)
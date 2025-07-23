from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
    client.server_info()
    print("MongoDB connection successful")
except Exception as e:
    print("MongoDB connection failed")
    print("Error:", e)

db = client["CodeSyncer"]

def get_mongo_client():
    return db


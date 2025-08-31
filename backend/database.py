from pymongo import MongoClient
from .config import settings

# database connection settings
client = MongoClient(settings.DATABASE_URL)
db = client.get_database("test")
UserCollection = db.get_collection("users")

# cluster = secure-input-ingestion
# database = test
# collection = users
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise Exception("MONGODB_URI is not set in the environment.")

client = AsyncIOMotorClient(MONGODB_URI)
# Specify your database name
db = client["chat_history_db"]

# from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from core.config import DATABASE_URL, DB_NAME
from pymongo import AsyncMongoClient
import gridfs


client = AsyncMongoClient(DATABASE_URL)
db = client[DB_NAME]
fs = gridfs.AsyncGridFSBucket(db)

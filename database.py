import os
import motor.motor_asyncio
from models import Fisherman
from dotenv import load_dotenv

# usage of the dotenv module may have to be removed for deployment
load_dotenv()

# these environmental variables can be saved directly in heroku
username = os.getenv("ATLAS_USER")
password = os.getenv("ATLAS_PASSWORD")

conn_str = f"mongodb+srv://{username}:{password}@cluster0.1kofm.mongodb.net/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(
    conn_str, serverSelectionTimeoutMS=10_000
)

database = client.FishTrak


async def fetch_all_fishermen() -> list:
    collection = database.fishermen
    fishermen = []
    cursor = collection.find({})
    async for document in cursor:
        fishermen.append(Fisherman(**document))
    return fishermen


async def create_fisherman(fisherman: dict) -> dict:
    collection = database.fishermen
    await collection.insert_one(fisherman)
    return fisherman

from bson import ObjectId
from model import Letter

# MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://192.168.178.53:27017')
database = client.Letters
collection = database.letter

def format_letter(letter) -> dict:
    return {
        "id": str(letter["_id"]),
        "title": letter["title"],
        "description": letter["description"],
    }

async def fetch_one_letter(title):
    document = await collection.find_one({"_id":ObjectId(title)})
    return document

# https://testdriven.io/blog/fastapi-mongo/
# id must be casted to ObjectId
async def fetch_one_letter_by_id(id):
    document = await collection.find_one({"_id":ObjectId(id)})
    return document

async def fetch_all_letters():
    letters = []
    cursor = collection.find({})
    async for document in cursor:
        letters.append(Letter(**document))
    return letters

async def create_letter(letter):
    document = letter
    result = await collection.insert_one(document)
    return document


async def update_letter(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document

async def remove_letter(title):
    await collection.delete_one({"title": title})
    return True
from motor.motor_asyncio import AsyncIOMotorClient

from .config import DATABASE_NAME, MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]
user_collection = database.get_collection("users")


async def init_db():
    # apart from the _id, make email unique
    await user_collection.create_index("email", unique=True)

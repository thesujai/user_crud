from bson import ObjectId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import DuplicateKeyError

from app.models import UserCreate, UserInDB, UserUpdate


async def create_user(collection: AsyncIOMotorCollection, user: UserCreate) -> UserInDB:
    try:
        result = await collection.insert_one(user.model_dump())
        created_user = await collection.find_one({"_id": result.inserted_id})
        return created_user
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )


async def get_user(collection: AsyncIOMotorCollection, user_id: str) -> UserInDB:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


async def list_users(collection: AsyncIOMotorCollection, page: int, size: int) -> list:
    skip = (page - 1) * size
    users_cursor = collection.find().skip(skip).limit(size)
    users = await users_cursor.to_list(length=size)
    return users


async def update_user(
    collection: AsyncIOMotorCollection, user_id: str, user: UserUpdate
) -> UserInDB:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if update_data:
        result = await collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        if result.modified_count == 1:
            updated_user = await collection.find_one({"_id": ObjectId(user_id)})
            return updated_user
    existing_user = await collection.find_one({"_id": ObjectId(user_id)})
    if existing_user:
        return existing_user
    raise HTTPException(status_code=404, detail="User not found")


async def delete_user(collection: AsyncIOMotorCollection, user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail="User not found")

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorCollection

from app.database import user_collection
from app.models import UserCreate, UserInDB, UserUpdate
from app.services.user_service import create_user as service_create_user
from app.services.user_service import delete_user as service_delete_user
from app.services.user_service import get_user as service_get_user
from app.services.user_service import list_users as service_list_users
from app.services.user_service import update_user as service_update_user

router = APIRouter(prefix="/users", tags=["users"])


def get_user_collection() -> AsyncIOMotorCollection:
    return user_collection


@router.post("/", response_model=UserInDB, status_code=201)
async def create_user(
    user: UserCreate, collection: AsyncIOMotorCollection = Depends(get_user_collection)
):
    return await service_create_user(collection, user)


@router.get("/{user_id}", response_model=UserInDB)
async def get_user(
    user_id: str, collection: AsyncIOMotorCollection = Depends(get_user_collection)
):
    return await service_get_user(collection, user_id)


@router.get("/", response_model=list[UserInDB])
async def list_users(
    page: int = Query(1, gt=0),
    size: int = Query(10, gt=0, le=100),
    collection: AsyncIOMotorCollection = Depends(get_user_collection),
):
    return await service_list_users(collection, page, size)


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(
    user_id: str,
    user: UserUpdate,
    collection: AsyncIOMotorCollection = Depends(get_user_collection),
):
    return await service_update_user(collection, user_id, user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: str, collection: AsyncIOMotorCollection = Depends(get_user_collection)
):
    await service_delete_user(collection, user_id)
    return

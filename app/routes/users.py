from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=str)
async def hello_world():
    return "Hello, World!"

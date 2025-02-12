from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routes import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, title="User CRUD")
app.include_router(users.router)

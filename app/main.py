from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, title="User CRUD")
app.include_router(users.router)

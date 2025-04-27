from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.auth import router as auth_router
from api.config import router as config_router
from api.items import router as items_router
from api.users import router as users_router
from database.session import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Simple API",
    description="簡易 API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(items_router)
app.include_router(users_router)
app.include_router(config_router)

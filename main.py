from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.models import Base
from core.db.session import db_session

from user.views import router as user_router
from items_views import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_session.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(items_router)
app.include_router(user_router)

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from api_v1 import router as router_v1
from user.views import router as user_router
from items_views import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(user_router)

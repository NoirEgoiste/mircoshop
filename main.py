from fastapi import FastAPI

from user.views import router as user_router
from items_views import router as items_router

app = FastAPI()
app.include_router(items_router)
app.include_router(user_router)

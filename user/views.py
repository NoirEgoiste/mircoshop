from fastapi import APIRouter

from user.schemas import CreateUser
from user import crud

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/")
async def create_user(user: CreateUser):
    return crud.create_user(user_in=user)

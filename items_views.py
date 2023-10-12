from typing import Annotated

from fastapi import Path, APIRouter

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
async def list_items():
    return {
        "Item1",
        "Item2",
        "Item3",
    }


@router.get("/latest/")
async def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}


@router.get("/{item_id}/")
async def get_items_by_id(items_id: Annotated[int, Path(gt=1, lt=1_000_000)]):
    return {
        "item": {
            "id": items_id,
        },
    }

from fastapi import APIRouter, Depends, Response

from app.database import get_db as get_shops_db
from app.models.categories import CategoryCreate
from prisma import Prisma as ShopsClient

router = APIRouter(tags=["categories"])


@router.get("/categories", summary="Get all categories")
async def handle_get_categories(shop_db: ShopsClient = Depends(get_shops_db)):
    categories = await shop_db.categories.find_many()

    return categories


@router.post("/categories", summary="Create a new category")
async def handle_post_categories(
    data: CategoryCreate, shop_db: ShopsClient = Depends(get_shops_db)
):
    new_category = await shop_db.categories.create(data=data.model_dump())

    return new_category


@router.delete("/categories/{category_slug}", summary="Delete a category")
async def handle_delete_category(
    category_slug: str, shop_db: ShopsClient = Depends(get_shops_db)
):
    res = await shop_db.categories.delete(where={"slug": category_slug})

    if res is None:
        return Response(status_code=404)

    return Response(status_code=204)

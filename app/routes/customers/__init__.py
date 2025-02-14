from fastapi import APIRouter, Depends

from app.database import get_db as get_shops_db
from prisma import Prisma as ShopsClient

router = APIRouter(tags=["customers"])


@router.get("/", summary="Get all customers")
async def handle_get_customers(
    shop_db: ShopsClient = Depends(get_shops_db),
    limit: int = 20,
    offset: int = 0,
):
    data = await shop_db.customers.find_many(
        take=limit,
        skip=offset,
        order={"created_at": "desc"},
    )

    return data

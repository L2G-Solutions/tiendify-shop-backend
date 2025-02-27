from uuid import uuid4

from fastapi import APIRouter, Depends, Request, Response, UploadFile

from app.config import settings
from app.database import get_db as get_shops_db
from app.models.products import ProductCreate, ProductUpdateVisibility
from app.routes.products.utils import (
    parse_products_response_data,
    parse_single_product_response_data,
)
from app.services.storage import upload_file
from prisma import Prisma as ShopsClient

router = APIRouter(tags=["products"])


@router.get("/", summary="Get all products")
async def handle_get_products(
    shop_db: ShopsClient = Depends(get_shops_db),
    limit: int = 20,
    offset: int = 0,
    search: str = None,
):
    data = await shop_db.products.find_many(
        where={"name": {"contains": search}} if search else None,
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}, "take": 1},
        },
        take=limit,
        skip=offset if offset > 0 else 0,
    )
    count = await shop_db.products.count()

    return {
        "products": parse_products_response_data(data),
        "total": count,
    }


@router.get("/{product_id}", summary="Get a single product")
async def handle_get_product(
    product_id: int, shop_db: ShopsClient = Depends(get_shops_db)
):
    product = await shop_db.products.find_unique(
        where={"id": product_id},
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}},
        },
    )

    if not product:
        return Response(status_code=404)

    return parse_single_product_response_data(product)


@router.post("/", summary="Create a new product")
async def handle_create_product(
    data: ProductCreate, shop_db: ShopsClient = Depends(get_shops_db)
):
    new_product = await shop_db.products.create(
        data={
            "name": data.name,
            "description": data.description,
            "stock": data.stock,
            "price": int(data.price),
            "product_categories": {
                "create": [{"category_id": c} for c in data.categories]
            },
        },
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}},
        },
    )
    return parse_single_product_response_data(new_product)


@router.put("/{product_id}", summary="Update a product")
async def handle_update_product(
    product_id: int, data: ProductCreate, shop_db: ShopsClient = Depends(get_shops_db)
):
    await shop_db.product_categories.delete_many(
        where={"product_id": product_id, "category_id": {"not_in": data.categories}}
    )
    updated_product = await shop_db.products.update(
        where={"id": product_id},
        data={
            "name": data.name,
            "description": data.description,
            "stock": data.stock,
            "price": int(data.price),
            "product_categories": {
                "connect_or_create": [
                    {
                        "create": {"category_id": c},
                        "where": {
                            "product_id_category_id": {
                                "product_id": product_id,
                                "category_id": c,
                            }
                        },
                    }
                    for c in data.categories
                ]
            },
        },
        include={
            "product_categories": {"include": {"categories": True}},
            "products_mediafiles": {"include": {"mediafiles": True}},
        },
    )

    if updated_product is None:
        return Response(status_code=404)

    return parse_single_product_response_data(updated_product)


@router.delete("/{product_id}", summary="Delete a product")
async def handle_delete_product(
    product_id: int, shop_db: ShopsClient = Depends(get_shops_db)
):
    deleted_product = await shop_db.products.delete(where={"id": product_id})

    if deleted_product is None:
        return Response(status_code=404)

    return Response(status_code=204)


@router.post("/{product_id}/mediafile", summary="Add a mediafile to a product")
async def handle_create_product_mediafile(
    product_id: int,
    request: Request,
    file: UploadFile,
    shop_db: ShopsClient = Depends(get_shops_db),
):
    extension = file.filename.split(".")[-1]

    id_ = str(uuid4())

    upload_file(file.file, "products/" + id_ + "." + extension)

    new_mediafile = await shop_db.mediafiles.create(
        data={
            "url": f"{settings.AZURE_STORAGE}/{settings.AZURE_PUBLIC_CONTAINER}/products/{id_}.{extension}",
            "type": file.content_type,
        }
    )

    await shop_db.products_mediafiles.create(
        data={"product_id": product_id, "media_file_id": new_mediafile.id}
    )

    return new_mediafile


@router.patch("/{product_id}/visibility", summary="Change product visibility")
async def handle_change_product_visibility(
    data: ProductUpdateVisibility,
    product_id: int,
    shop_db: ShopsClient = Depends(get_shops_db),
):

    updated_product = await shop_db.products.update(
        where={"id": product_id}, data={"hidden": data.hidden}
    )

    if not updated_product:
        return Response(status_code=404)

    return parse_single_product_response_data(updated_product)

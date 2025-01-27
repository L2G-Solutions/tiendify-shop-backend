from prisma.models import products as Products


def parse_products_response_data(data: list[Products]) -> list[dict]:
    """Parse products response data to remove unwanted fields,
    and return the proper JSON schema.

    Args:
        data (list[products]): The data to be parsed (response from Prisma).

    Returns:
        list[dict]: The parsed data.
    """

    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "isHidden": p.hidden,
            "categories": [
                {
                    "id": c.categories.slug,
                    "name": c.categories.name,
                    "description": c.categories.description,
                }
                for c in p.product_categories
            ],
            "thumbnailImg": (
                p.products_mediafiles[0].mediafiles.url
                if len(p.products_mediafiles) > 0
                else None
            ),
            "stock": p.stock,
            "createdAt": p.created_at,
        }
        for p in data
    ]


def parse_single_product_response_data(data: Products) -> dict:
    """Parse single product response data to remove unwanted fields,
    and return the proper JSON schema.

    Args:
        data (products): The data to be parsed (products model response from Prisma).

    Returns:
        dict: The parsed data.
    """

    return {
        "id": data.id,
        "name": data.name,
        "price": data.price,
        "description": data.description,
        "categories": [
            {
                "id": c.categories.slug,
                "name": c.categories.name,
                "description": c.categories.description,
            }
            for c in (data.product_categories if data.product_categories else [])
        ],
        "mediafiles": [
            m.mediafiles.url
            for m in (data.products_mediafiles if data.products_mediafiles else [])
        ],
        "stock": data.stock,
        "createdAt": data.created_at,
        "isHidden": data.hidden,
    }

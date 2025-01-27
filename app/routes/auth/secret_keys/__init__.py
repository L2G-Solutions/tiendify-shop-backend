from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import has_admin_role
from app.core.security.utils import generate_secret_key
from app.database import get_db as get_shops_db
from app.models.secretKey import SecretKeyCreate, SecretKeyInfo
from prisma import Prisma

router = APIRouter(tags=["secret keys"], dependencies=[Depends(has_admin_role)])


@router.get(
    "/",
    summary="Get all secret keys",
)
async def get_secret_keys(
    client_db: Prisma = Depends(get_shops_db),
):
    secret_keys = await SecretKeyInfo.prisma(client_db).find_many()

    return secret_keys


@router.post(
    "/",
    summary="Create a new secret key",
)
async def create_secret_key(
    secret_key_info: SecretKeyCreate,
    client_db: Prisma = Depends(get_shops_db),
):
    total_secret_keys = await client_db.secret_keys.count()

    if total_secret_keys >= 10:
        raise HTTPException(
            status_code=400,
            detail="You can only have a maximum of 10 secret keys",
        )

    [secret_key, hashed_secret_key, secret_key_prefix] = generate_secret_key()
    secret_key_row = await client_db.secret_keys.create(
        {
            "name": secret_key_info.name,
            "prefix": secret_key_prefix,
            "scopes": "[admin.all]",
            "secret_key": hashed_secret_key,
        }
    )

    secret_key_row.secret_key = secret_key

    return secret_key_row


@router.delete(
    "/{secret_key_id}",
    summary="Delete a secret key",
)
async def delete_secret_key(
    secret_key_id: UUID,
    client_db: Prisma = Depends(get_shops_db),
):
    secret_key_id = str(secret_key_id)
    secret_key = await client_db.secret_keys.find_unique(where={"id": secret_key_id})

    if not secret_key:
        raise HTTPException(
            status_code=404,
            detail="Secret key not found",
        )

    await client_db.secret_keys.delete(where={"id": secret_key_id})

    return secret_key

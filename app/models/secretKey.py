from typing import Optional

from prisma.bases import Basesecret_keys as BaseSecretKey
from pydantic import BaseModel


class SecretKeyCreate(BaseModel):
    name: str
    scopes: Optional[str] = "[admin.all]"


class SecretKeyInfo(BaseSecretKey):
    id: str
    name: str
    scopes: str
    prefix: str
    enabled: bool
    created_at: str
    updated_at: str


class SecretKeyValue(BaseSecretKey):
    secret_key: str

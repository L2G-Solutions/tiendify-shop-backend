from typing import List, Optional

from prisma.bases import Basesecret_keys as BaseSecretKey
from pydantic import BaseModel


class SecretKeyCreate(BaseModel):
    name: str
    scopes: Optional[str] = "[admin.all]"


class SecretKeyInfo(BaseSecretKey):
    name: str
    scopes: List[str]
    prefix: str
    enabled: bool
    created_at: str
    updated_at: str


class SecretKeyValue(BaseSecretKey):
    secret_key: str

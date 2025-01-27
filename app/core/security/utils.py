import secrets
from typing import Tuple

from app.core.security import secret_key_context


def generate_secret_key() -> Tuple[str, str, str]:
    """
    Generate a new secret key, and return it, hashed value, and prefix.

    Returns:
        Tuple[str, str, str]: The secret key, hashed value, and prefix.
    """
    secret_key = secrets.token_urlsafe(32)
    hashed_secret_key = secret_key_context.hash(secret_key)
    prefix = secret_key[:3] + "..." + secret_key[-3:]

    return secret_key, hashed_secret_key, prefix

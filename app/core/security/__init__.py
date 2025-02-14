from typing import Annotated, Optional, Union
from urllib.parse import quote

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
from jwt import PyJWKClient, decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from keycloak import KeycloakOpenID
from passlib.context import CryptContext

from app.config import settings
from app.models.secretKey import SecretKeyValue
from app.models.user import UserTokenInfo

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)

cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)
refresh_cookie_scheme = APIKeyCookie(name="refresh_token", auto_error=False)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scheme_name="Secret key Adim Authentication",
    auto_error=False,
)

secret_key_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenAccessChecker:
    """Class to check the validity of the access token."""

    def __init__(self, auto_error: Optional[bool] = True):
        self.auto_error = auto_error

    def __call__(
        self,
        access_token: str = Depends(cookie_scheme),
        refresh_token: str = Depends(refresh_cookie_scheme),
    ):
        try:
            if not refresh_token:
                raise HTTPException(status_code=401, detail="Not authenticated")

            if refresh_token and not access_token:
                raise HTTPException(status_code=403, detail="Not authenticated")

            jwks_url = f"{settings.KEYCLOAK_URL}/realms/{quote(settings.KEYCLOAK_REALM)}/protocol/openid-connect/certs"
            jwks_client = PyJWKClient(jwks_url, timeout=10)

            try:
                signing_key = jwks_client.get_signing_key_from_jwt(access_token)

                decoded_token = decode(
                    access_token,
                    signing_key.key,
                    algorithms=["RS256"],
                    audience=["account"],
                    options={"verify_exp": True},
                )

                return decoded_token
            except ExpiredSignatureError:
                raise HTTPException(status_code=403, detail="Token expired")
            except InvalidTokenError:
                raise HTTPException(status_code=401, detail="Not authenticated")
        except HTTPException as e:
            if self.auto_error:
                raise e
            return False


class SecretKeyAccessChecker:
    def __init__(self, auto_error: Optional[bool] = True):
        self.auto_error = auto_error

    async def __call__(self, secret_key: str = Depends(oauth2_scheme)):
        try:
            if not secret_key:
                raise HTTPException(status_code=401, detail="Not authenticated")

            allowed_secret_keys = [settings.SECRET_KEY]
            client_assigned_secret_keys = await SecretKeyValue.prisma().find_many()

            if client_assigned_secret_keys:
                allowed_secret_keys += [
                    key.secret_key for key in client_assigned_secret_keys
                ]

            for key in allowed_secret_keys:
                if secret_key_context.verify(secret_key, key):
                    return True

            raise HTTPException(status_code=403, detail="Unauthorized access")
        except HTTPException as e:
            if self.auto_error:
                raise e
            return False


has_admin_role = SecretKeyAccessChecker()
valid_access_token = TokenAccessChecker()

has_admin_role_without_error = SecretKeyAccessChecker(auto_error=False)
valid_access_token_without_error = TokenAccessChecker(auto_error=False)


async def has_customer_session(
    token_data: Annotated[Union[dict, bool], Depends(valid_access_token_without_error)],
    admin: Annotated[bool, Depends(has_admin_role_without_error)],
):
    if not token_data and not admin:
        raise HTTPException(status_code=403, detail="Unauthorized access")


async def get_current_user(
    token_data: Annotated[dict, Depends(valid_access_token)]
) -> UserTokenInfo:
    try:
        user_info = {
            "username": token_data.get("preferred_username"),
            "email": token_data.get("email"),
            "firstName": token_data.get("given_name"),
            "lastName": token_data.get("family_name"),
        }
        return UserTokenInfo(**user_info)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid token structure")

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tiendify"
    SECRET_KEY: str
    DATABASE_URL: str
    AZURE_STORAGE: str
    AZURE_PUBLIC_CONTAINER: str
    KEYCLOAK_URL: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()

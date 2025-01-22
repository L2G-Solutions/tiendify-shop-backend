from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tiendify"
    DATABASE_URL: str
    AZURE_STORAGE: str
    AZURE_PUBLIC_CONTAINER: str

    class Config:
        env_file = ".env"


settings = Settings()

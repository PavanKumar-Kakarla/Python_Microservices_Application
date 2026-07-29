from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str

    AUTH_SERVICE_URL: str
    USER_SERVICE_URL: str
    PRODUCT_SERVICE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Payment Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str

    AUTH_SERVICE_URL: str
    USER_SERVICE_URL: str
    ORDER_SERVICE_URL: str

    PAYMENT_SERVICE_PORT: int = 8005

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
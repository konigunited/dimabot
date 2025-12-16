from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Telegram
    BOT_TOKEN: str

    # Database
    DATABASE_URL: str

    # YooKassa
    YOOKASSA_SHOP_ID: str
    YOOKASSA_SECRET_KEY: str

    # Optional
    MOCK_PAYMENTS: bool = False
    DEBUG: bool = False


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "Indonesia Stock API"
    APP_VERSION: str = "1.0.0"
    REQUEST_TIMEOUT: int = 10
    LOG_LEVEL: str = "INFO"
    PROVIDER: str = "yahoo"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
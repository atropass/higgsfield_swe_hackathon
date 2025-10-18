from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="higgsfield-api", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=False, alias="APP_DEBUG")
    app_api_key: str = Field(default="dev-key", alias="APP_API_KEY")

    hf_api_key: str = Field(..., alias="HF_API_KEY")
    hf_secret: str = Field(..., alias="HF_SECRET")
    hf_base_url: str = Field(
        default="https://platform.higgsfield.ai", alias="HF_BASE_URL"
    )

    request_timeout_connect: int = Field(default=10, alias="REQUEST_TIMEOUT_CONNECT")
    request_timeout_read: int = Field(default=60, alias="REQUEST_TIMEOUT_READ")
    max_retries: int = Field(default=3, alias="MAX_RETRIES")
    retry_backoff_factor: float = Field(default=2.0, alias="RETRY_BACKOFF_FACTOR")

    poll_max_attempts: int = Field(default=60, alias="POLL_MAX_ATTEMPTS")
    poll_interval_seconds: int = Field(default=5, alias="POLL_INTERVAL_SECONDS")

    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        alias="CORS_ORIGINS",
    )

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


settings = Settings()


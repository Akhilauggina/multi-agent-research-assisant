from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Determine path to .env file relative to this settings module
_BASE_DIR = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _BASE_DIR / ".env"


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_provider: str = Field(default="gemini")
    openai_api_key: str = Field(default="")
    openai_model: str = Field(default="gpt-4.1")
    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-3.5-flash-lite")
    log_level: str = Field(default="INFO")


settings = Settings()

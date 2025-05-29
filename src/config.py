from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NEBULA_BLOCK_API_URL: str = "https://api.nebulablock.com"
    NEBULA_BLOCK_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
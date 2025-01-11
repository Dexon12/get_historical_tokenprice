from typing import Annotated, Any, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", # Fix 
        env_ignore_empty=True,
        extra="ignore",
    )
    CHAINLIST_API_URL: str = "http://localhost:3000/api/price"


settings = Settings()  # type: ignore
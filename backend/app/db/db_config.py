from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = (Path(__file__).resolve().parents[3] / ".env")

load_dotenv(dotenv_path=env_path)

class DataBaseSettings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_path = (Path(__file__).resolve().parents[3] / ".env"),
        extra="ignore"
    )
    
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_sync_db_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" 

db_settings = DataBaseSettings()

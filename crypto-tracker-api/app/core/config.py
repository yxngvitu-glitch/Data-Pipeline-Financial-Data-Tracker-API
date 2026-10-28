from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Data Tracker API"
    DATABASE_URL: str = "sqlite:///./tracker.db"
    FETCH_INTERVAL_SECONDS: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
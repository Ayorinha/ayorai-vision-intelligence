from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AYORAI Vision Intelligence"
    environment: str = "production"
    confidence_review_threshold: float = 0.70
    confidence_auto_accept_threshold: float = 0.90
    model_path: str = "yolo11n.pt"
    database_url: str = "sqlite:///data/ayorai.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

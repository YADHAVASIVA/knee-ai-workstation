import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Knee AI Analysis"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Storage Settings
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    UPLOAD_DIR: str = os.path.join(DATA_DIR, "uploads")
    PROCESSED_DIR: str = os.path.join(DATA_DIR, "processed")
    PREVIEWS_DIR: str = os.path.join(DATA_DIR, "previews")
    MASKS_DIR: str = os.path.join(DATA_DIR, "masks")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024 # 10 MB

    def create_dirs(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(os.path.join(self.UPLOAD_DIR, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.UPLOAD_DIR, "dicom"), exist_ok=True)
        os.makedirs(self.PROCESSED_DIR, exist_ok=True)
        os.makedirs(self.PREVIEWS_DIR, exist_ok=True)
        os.makedirs(self.MASKS_DIR, exist_ok=True)

    class Config:
        case_sensitive = True

settings = Settings()

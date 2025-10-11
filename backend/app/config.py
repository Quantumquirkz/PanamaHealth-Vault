from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Configuración de la aplicación - Todo local"""
    
    # General
    APP_NAME: str = "PanamaHealth Vault"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "change-this-in-production-must-be-at-least-32-characters-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 horas
    
    # Database (SQLite local)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/panamahealth.db"
    
    # File Upload (almacenamiento local)
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "jpg", "jpeg", "png"]
    
    # OCR (opcional)
    TESSERACT_CMD: str = "tesseract"  # Debe estar en PATH
    OCR_ENABLED: bool = False  # Deshabilitado por defecto
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Crear directorio de uploads si no existe
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        (self.UPLOAD_DIR / "medical-records").mkdir(exist_ok=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


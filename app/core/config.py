from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    # Настройки самого приложения
    PROJECT_NAME: str = "Mini-Forum API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ALGORITHM: str = "HS256"
    
    # Инфраструктура
    DATABASE_URL: str
    
    secret_key: str = SecretStr
    access_token_expire_minutes: int = 30
    
    # Pydantic v2 конфиг: указываем, откуда читать переменные
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",extra="ignore",)

settings = Settings()
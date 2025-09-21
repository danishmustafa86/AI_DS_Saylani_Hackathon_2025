from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os 
import dotenv

dotenv.load_dotenv()

class Settings(BaseSettings):
    environment: str = "development"
    api_port: int = 8000
    secret_key: str = "change-me-please"
    
    # OpenAI
    openai_api_key: str = ""
    agent_model: str = "gpt-4o-mini"
    
    # ElevenLabs
    elevenlabs_api_key: str = ""
    
    # MongoDB (keeping both names for compatibility)
    mongodb_uri: str = "mongodb://localhost:27017"
    mongo_uri: str = "mongodb://localhost:27017"  # alias
    mongodb_db: str = "ai_campus"
    
    # SMTP
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    email_from: str = "notifications@example.com"
    
    # CORS
    allow_origins: str = "http://localhost:8080,http://localhost:8081,http://localhost:5173,http://localhost:3000,http://127.0.0.1:8080,http://127.0.0.1:8081,http://127.0.0.1:5173,http://127.0.0.1:3000"
    allow_methods: str = "*"
    allow_headers: str = "*"
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    
    @property
    def db_uri(self) -> str:
        """Use mongo_uri if set, otherwise mongodb_uri"""
        return self.mongo_uri if self.mongo_uri != "mongodb://localhost:27017" else self.mongodb_uri

    def get_cors_origins(self) -> List[str]:
        if self.allow_origins == "*":
            return ["*"]
        return [x.strip() for x in self.allow_origins.split(",")]

    def get_cors_methods(self) -> List[str]:
        if self.allow_methods == "*":
            return ["*"]
        return [x.strip() for x in self.allow_methods.split(",")]

    def get_cors_headers(self) -> List[str]:
        if self.allow_headers == "*":
            return ["*"]
        return [x.strip() for x in self.allow_headers.split(",")]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="")


@lru_cache
def get_settings() -> Settings:
    return Settings()



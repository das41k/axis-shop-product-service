from pydantic_settings import BaseSettings, SettingsConfigDict
import urllib.parse

class Settings(BaseSettings):
    APP_NAME: str
    APP_HOST: str
    APP_PORT: int
    
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    
    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://username:password@host:port/name_db
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
    @property
    def DATABASE_URL_psycopg(self):
        # postgresql+psycopg://username:password@host:port/name_db
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def REDIS_URL(self):
        # redis://username:password@host:port/db
        safe_password = urllib.parse.quote_plus(self.REDIS_PASSWORD)
        return f"redis://:{safe_password}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        
    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings()
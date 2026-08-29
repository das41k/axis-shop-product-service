from pydantic_settings import BaseSettings, SettingsConfigDict

class TestSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://username:password@host:port/name_db
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            
    @property
    def DATABASE_URL_psycopg(self):
        # postgresql+psycopg://username:password@host:port/name_db
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            
    model_config = SettingsConfigDict(env_file = ".env_test")

setting = TestSettings()
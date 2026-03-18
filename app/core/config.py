from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "llm-p"
    ENV: str = "local"
    
    JWT_SECRET: str = "change_me_super_secret"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    SQLITE_PATH: str = "./app.db"
    
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    OPENROUTER_SITE_URL: str = "https://example.com"
    OPENROUTER_APP_NAME: str = "llm-fastapi-openrouter"
    
    class Config:
        env_file = ".env"

settings = Settings()
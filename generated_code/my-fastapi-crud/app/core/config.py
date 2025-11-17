from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App settings
    PROJECT_NAME: str = "My FastAPI App"

    # Database
    DATABASE_URL: str = "sqlite:///./test.db"  # For SQL
    # For MongoDB: DATABASE_URL = "mongodb://localhost:27017"
    DATABASE_NAME: str = "myapp"  # For MongoDB
    DATABASE_TYPE: str = "sql"  # "sql" or "mongodb"

    # Security (required for authentication)
    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_an_env_file"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Load from .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Create a single, importable instance
settings = Settings()

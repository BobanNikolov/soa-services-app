import os
from dotenv import load_dotenv

from pathlib import Path

env_path = '../variables.env.local'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "soa-services-app"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER","services-app")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD","services-app")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "services-app")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()

import os

from dotenv import load_dotenv

env_path = '.././.env.local'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "soa-services-app"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URL = os.getenv("DB_CONNECTION")
    USER_ENDPOINT = os.getenv("USER_ENDPOINT")
    STORE_ENDPOINT = os.getenv("STORE_ENDPOINT")
    PAYMENT_ENDPOINT = os.getenv("PAYMENT_ENDPOINT")
    NOTIFICATION_ENDPOINT = os.getenv("NOTIFICATION_ENDPOINT")


settings = Settings()

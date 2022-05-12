import os

from dependency_injector import providers
from dotenv import load_dotenv

from integration.integrations import UserService, PaymentService, NotificationService, StoreService

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

    userService = providers.Factory(UserService, USER_ENDPOINT)
    paymentService = providers.Factory(PaymentService, PAYMENT_ENDPOINT)
    notificationService = providers.Factory(NotificationService, NOTIFICATION_ENDPOINT)
    storeService = providers.Factory(StoreService, STORE_ENDPOINT)


settings = Settings()

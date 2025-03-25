import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL")
    DB_NAME = os.getenv("DB_NAME")

    STORY_PROTOCOL_API_BASE_URL = os.getenv("STORY_PROTOCOL_API_BASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


config = Config()


class CeleryConfig:
    broker = os.getenv("CELERY_BROKER_URL")
    backend = os.getenv("CELERY_RESULT_BACKEND")
    include = ["task_queue.tasks"]
    enable_utc = True
    timezone = "UTC"
    broker_connection_retry_on_startup = True

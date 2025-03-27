import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL")
    DB_NAME = os.getenv("DB_NAME")
    STORY_PROTOCOL_API_BASE_URL = os.getenv("STORY_PROTOCOL_API_BASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SEARXNG_HOST = os.getenv("SEARXNG_HOST", "")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:6789/auth/callback/google")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    QDRANT_URI = os.getenv("QDRANT_URI")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    REDIS_URI = os.getenv("REDIS_URI")


config = Config()


class CeleryConfig:
    broker = os.getenv("CELERY_BROKER_URL")
    backend = os.getenv("CELERY_RESULT_BACKEND")
    include = ["task_queue.tasks"]
    enable_utc = True
    timezone = "UTC"
    broker_connection_retry_on_startup = True
    beat_schedule = {
        "prepare_reply_to_mentions": {
            "task": "tasks.x.prepare_reply_to_mentions",
            "schedule": 60,
            "options": {"queue": "celery"},
        },
        "get_mentions": {
            "task": "tasks.x.get_mentions",
            "schedule": 80,
            "options": {"queue": "celery"},
        },
    }

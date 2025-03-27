import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL")
    DB_NAME = os.getenv("DB_NAME")
    
    STORY_PROTOCOL_API_BASE_URL = os.getenv("STORY_PROTOCOL_API_BASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_HOST = os.getenv("RAPID_API_HOST", "twitter-api45.p.rapidapi.com")
    RAPID_BASE_URL = os.getenv("RAPID_BASE_URL", "https://twitter-api45.p.rapidapi.com")

    MONGO_URI = os.getenv("MONGO_URI")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
    TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    AGENT_NAME = os.getenv("AGENT_NAME", "clinkaiagent_")
    PORT = int(os.getenv("PORT", 6789))
    SEARXNG_HOST = os.getenv("SEARXNG_HOST", "")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    ONCHAIN_SERVICE_BASE_URL = os.getenv(
        "ONCHAIN_SERVICE_BASE_URL", "http://localhost:6001"
    )
    AGENT_SECRET = os.getenv("AGENT_SECRET")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    # Google OAuth credentials
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:6789/auth/callback/google"
    )

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Frontend URL for redirect after authentication
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # X (Twitter) OAuth credentials
    X_CLIENT_ID = os.getenv("X_CLIENT_ID")
    X_CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")
    X_REDIRECT_URI = os.getenv(
        "X_REDIRECT_URI", "http://localhost:6789/api/auth/callback/x"
    )
    QDRANT_URI = os.getenv("QDRANT_URI")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    ## Google Auth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

    ## JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

    ## Redis
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

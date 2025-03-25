import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_URL = os.getenv("DB_URL")
    DB_NAME = os.getenv("DB_NAME")

    STORY_PROTOCOL_API_BASE_URL = os.getenv("STORY_PROTOCOL_API_BASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


config = Config()

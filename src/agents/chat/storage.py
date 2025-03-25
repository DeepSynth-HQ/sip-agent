from agno.storage.agent.mongodb import MongoDbAgentStorage
from settings.config import config

storage = MongoDbAgentStorage(
    db_url=config.DB_URL,
    db_name=config.DB_NAME,
    collection_name="agent_chat",
)

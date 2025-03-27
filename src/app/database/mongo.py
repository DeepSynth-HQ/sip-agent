import pymongo
from settings import config


def get_collection(collection_name: str):
    client = pymongo.MongoClient(config.DB_URL)
    db = client[config.DB_NAME]
    return db[collection_name]

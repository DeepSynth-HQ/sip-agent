import pymongo
from settings import config

client = pymongo.MongoClient(config.DB_URL)
db = client[config.DB_NAME]


def get_collection(collection_name: str):
    return db[collection_name]

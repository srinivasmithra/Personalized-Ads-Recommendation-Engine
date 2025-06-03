from pymongo import MongoClient

from app.config.config import app_config


db_client = MongoClient(app_config.MONGO_DB_URI)
db = db_client[app_config.MONGO_DB_NAME]

from pymongo import MongoClient
import config

class MongoDatabase():
    def __init__(self):
        self.db = None

    def connect(self):
        # save data to database
        # uri_cloud = f"mongodb+srv://{config.mongo_user}:{config.mongo_pwd}@{config.mongo_host}/?retryWrites=true&w=majority"
        uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
        client = MongoClient(uri_local)
        
        self.db = client.sezame
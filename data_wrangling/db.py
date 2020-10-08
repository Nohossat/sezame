from pymongo import MongoClient

class MongoDatabase():
    def __init__():
        self.db = None

    def connect():
        # save data to database
        uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
        client = MongoClient(uri_local)
        
        self.db = client.sezame
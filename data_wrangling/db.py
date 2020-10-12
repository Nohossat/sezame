from pymongo import MongoClient

import sys
sys.path.append('../')

import data_wrangling.config as config

class MongoDatabase():
    def __init__(self):
        self.db = None

    def connect(self):
        uri_local = f"mongodb://{config.mongo_local_user}:{config.mongo_local_pwd}@{config.mongo_localhost}:{config.mongo_local_port}/?authSource=admin&readPreference=primary&ssl=false"
        client = MongoClient(uri_local)
        
        self.db = client.sezame
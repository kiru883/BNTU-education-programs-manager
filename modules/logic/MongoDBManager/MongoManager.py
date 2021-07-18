import pymongo
import configparser
import pandas as pd

from typing import Dict


class MongoManager():
    def __init__(self, dbconfig_path: str):
        # read config file
        config = configparser.ConfigParser()
        config.read(dbconfig_path)
        # read args
        host = config['MONGO']['host']
        port = config['MONGO']['port']
        self.db_name = config['DATABASE']['name']
        self.col_name = config['DATABASE']['collection_name']

        # create client
        self.__mongo_client = pymongo.MongoClient(f"mongodb://{host}:{port}/")

        # check existing of database with bd_name name
        self.db_is_exist = self.__db_in_mongo(self.db_name)
        self.col_is_exist = self.__collection_in_db(self.db_name, self.col_name)
        if self.db_is_exist and self.col_is_exist:
            self.create_database_and_collection()
        else:
            self.__mongo_col = None


    def add_document(self, doc: Dict):
        if self.__mongo_col is not None:
            self.__mongo_col.insert_one(doc)


    def find(self, query: Dict):
        if self.__mongo_col is not None:
            result = list(self.__mongo_col.find(query))
            if len(result) != 0:
                # form dataframe
                result = pd.DataFrame(result)
                result = result.drop('_id', axis=1)
            else:
                result = 'Not found'

        return result


    def create_database_and_collection(self):
        # create collection
        self.__mongo_col = self.__mongo_client[self.db_name][self.col_name]
        self.__mongo_col.insert_one({})


    def __db_in_mongo(self, db_name: str):
        return db_name in self.__mongo_client.list_database_names()


    def __collection_in_db(self, db_name: str, col_name: str):
        return col_name in self.__mongo_client[db_name].list_collection_names()












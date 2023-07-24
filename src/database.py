import pymongo
import json
from typing import List

class MongoConnection:

    with open('conf.json') as file:
        conf = json.load(file)

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://root:password@mongodb:27017/')
        self.db = self.client['smartmaple']
        self.collections = dict()
        for scrapper in MongoConnection.conf.get('scrappers'):
            self.collections[scrapper.get('name')] =  self.db[scrapper.get('name')]

    def add_books(self, books: List[dict], collection_name: str):
        for book in books:
            db_book = self.collections[collection_name].find_one(
                {
                    "name": book.get('name'),
                    "writers": book.get('writers'),
                    "publisher": book.get('publisher')
                })
            
            if db_book:
                self.collections[collection_name].update_one(
                    {"_id": db_book.get('_id')},
                    {"$set": {"price": db_book.get("price")}},
                    upsert=True
                )
            else:
                self.collections[collection_name].insert_one(book)


    def close_connection(self):
        self.client.close()
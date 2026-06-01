from datetime import datetime
from pymongo import MongoClient
from settings import (MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION)


class MongoDB:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DATABASE][MONGO_COLLECTION]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        return False

    def save_search(self, search_type, value):
        self.db.insert_one(
            {
                'search_type': search_type,
                'value': value,
                'created_at': datetime.now(),
            }
        )

    def get_recent_searches(self):
        return list(self.db.find().sort('created_at', -1).limit(10))

    def get_top_searches(self):
        pipeline = [{'$group': {'_id': {'search_type': '$search_type','value': '$value'},
                                'count': {'$sum': 1},}},
                    {'$sort': {'count': -1}}, {'$limit': 5}]
        return list(self.db.aggregate(pipeline))
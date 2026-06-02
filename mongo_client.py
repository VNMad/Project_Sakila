"""
MongoDB client.
Stores search history and provides
statistics for recent and popular searches.
"""

from datetime import datetime
from pymongo import MongoClient
from settings import (MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION)


class MongoDB:
    """
    MongoDB wrapper.
    Provides methods for:
    - saving search history
    - retrieving recent searches
    - retrieving top search requests
    Supports context manager protocol.
    """

    def __init__(self) -> None:
        """
        Initialize MongoDB connection.
        Creates MongoDB client and selects
        database and collection.
        """
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DATABASE][MONGO_COLLECTION]

    def __enter__(self) -> "MongoDB":
        """
        Enter context manager.
        Returns: Current MongoDB instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit context manager.
        Closes MongoDB connection.
        Args: exc_type: Exception type.
               exc_val: Exception value.
                exc_tb: Exception traceback.
        Returns: False to propagate exceptions.
        """
        self.client.close()
        return False

    def save_search(self, search_type: str, value: str | dict) -> None:
        """
            Save search request to MongoDB.
            Args: search_type: Search type.
                        value: Search value.
            Returns: None
            """
        self.db.insert_one(
            {
                'search_type': search_type,
                'value': value,
                'created_at': datetime.now(),
            }
        )

    def get_recent_searches(self) -> list[dict]:
        """
        Retrieve latest search requests.
        Returns: List of recent searches.
        """
        return list(self.db.find().sort('created_at', -1).limit(10))

    def get_top_searches(self) -> list[dict]:
        """
        Retrieve most popular search requests.
        Returns: List of top searches with usage count.
        """
        pipeline = [{'$group': {'_id': {'search_type': '$search_type','value': '$value'},
                                'count': {'$sum': 1},}},
                    {'$sort': {'count': -1}}, {'$limit': 5}]
        return list(self.db.aggregate(pipeline))
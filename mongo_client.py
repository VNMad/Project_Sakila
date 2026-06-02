"""MongoDB access layer for search history."""

from datetime import datetime
from pymongo import MongoClient
from settings import (MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION)


class MongoDB:
    """MongoDB client wrapper."""

    def __init__(self) -> None:
        """Initialize MongoDB connection and select database collection."""
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DATABASE][MONGO_COLLECTION]

    def __enter__(self) -> "MongoDB":
        """Enter the runtime context and return MongoDB instance.
        Returns: MongoDB: Current MongoDB object. """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Close MongoDB connection when leaving context manager.
        Args:
            exc_type: Exception type if raised.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.
        Returns:
            bool: False to propagate exceptions."""
        self.client.close()
        return False

    def save_search(self, search_type: str, value: str | dict) -> None:
        """Save user search request."""
        self.db.insert_one(
            {
                'search_type': search_type,
                'value': value,
                'created_at': datetime.now(),
            }
        )

    def get_recent_searches(self) -> list[dict]:
        """Return latest searches."""
        return list(self.db.find().sort('created_at', -1).limit(10))

    def get_top_searches(self) -> list[dict]:
        """Return top searched requests."""
        pipeline = [{'$group': {'_id': {'search_type': '$search_type','value': '$value'},
                                'count': {'$sum': 1},}},
                    {'$sort': {'count': -1}}, {'$limit': 5}]
        return list(self.db.aggregate(pipeline))
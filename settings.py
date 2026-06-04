"""
Project configuration module.
Loads environment variables from a .env file and
defines connection settings for MySQL and MongoDB.
"""

import os

from dotenv import load_dotenv


load_dotenv()


MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
}


MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

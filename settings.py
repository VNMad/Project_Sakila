import os

from dotenv import load_dotenv


load_dotenv()


MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
}


MONGO_URI = (
    'mongodb://ich_editor:verystrongpassword'
    '@mongo.itcareerhub.de/?readPreference=primary'
    '&ssl=false&authMechanism=DEFAULT'
    '&authSource=ich_edit'
)

MONGO_DATABASE = 'ich_edit'
MONGO_COLLECTION = 'final_project_121225ptm_vnmad'
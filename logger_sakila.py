import logging
from functools import wraps

from pymysql import MySQLError
from pymongo import errors as mongo_errors

from errors import (
    MoviesPublishedYearError,
    CategoryNotFoundError,
    InvalidMenuChoiceError,
    InvalidYearRangeError,
)


logging.basicConfig(
    filename='project.log',
    level=logging.ERROR,
    format=(
        '%(asctime)s '
        '%(levelname)s '
        '%(message)s'
    )
)

logger = logging.getLogger(__name__)

def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MoviesPublishedYearError as e:
            logger.error(e)
            print(e)
        except InvalidYearRangeError as e:
            logger.error(e)
            print(e)
        except CategoryNotFoundError as e:
            logger.error(e)
            print(e)
        except InvalidMenuChoiceError as e:
            logger.error(e)
            print(e)
        except MySQLError as e:
            logger.exception(e)
            print('Database MySQL error.')
        except mongo_errors.ConnectionFailure as e:
            logger.exception(e)
            print('MongoDB connection error.')
        except mongo_errors.OperationFailure as e:
            logger.exception(e)
            print('MongoDB authorization error.')
        except mongo_errors.PyMongoError as e:
            logger.exception(e)
            print('MongoDB error.')
        except Exception as e:
            logger.exception(e)
            print('Unexpected system error.')
    return wrapper
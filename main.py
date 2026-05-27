import pymysql
import os
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from settings import MYSQL_CONFIG
from sql_queries import *

load_dotenv('.env')

try:
    with pymysql.connect(**MYSQL_CONFIG, cursorclass=DictCursor) as conn_ich:
        print('Connection opened')
        try:
            with conn_ich.cursor() as cursor:
                #cursor.execute(GET_CATEGORIES)
                #cursor.execute(GET_YEAR_RANGE)
                #cursor.execute(SEARCH_FILMS_BY_KEYWORD, ("%academy%", 10, 0))
                cursor.execute(SEARCH_BY_CATEGORY_AND_YEAR, (15, 2000, 2026, 10, 0))
                for num, row in enumerate(cursor.fetchall(), 1):
                    fields = ", ".join([f"{key}: {val}" for key, val in row.items()])
                    print(f"{num}. {fields}")
        except pymysql.MySQLError as e:
            print("Query error:", e)

except pymysql.MySQLError as e:
    print("Connection error:", e)







# if __name__ == '__main__':
#     main()

# import pymysql
# import os
# from pymysql.cursors import DictCursor
# from dotenv import load_dotenv
# from settings import MYSQL_CONFIG
# from sql_queries import *
#
#
# load_dotenv('.env')
#
# try:
#     with pymysql.connect(**MYSQL_CONFIG, cursorclass=DictCursor) as conn_ich:
#         print('Connection opened')
#         try:
#             with conn_ich.cursor() as cursor:
#                 #cursor.execute(GET_CATEGORIES)
#                 #cursor.execute(GET_YEAR_RANGE)
#                 #cursor.execute(SEARCH_FILMS_BY_KEYWORD, ("%academy%", 10, 0))
#                 cursor.execute(SEARCH_BY_CATEGORY_AND_YEAR, (15, 2000, 2026, 10, 0))
#                 for num, row in enumerate(cursor.fetchall(), 1):
#                     fields = ", ".join([f"{key}: {val}" for key, val in row.items()])
#                     print(f"{num}. {fields}")
#         except pymysql.MySQLError as e:
#             print("Query error:", e)
#
# except pymysql.MySQLError as e:
#     print("Connection error:", e)
#
#
#



# Олег стайл
import ui_test

def main():
    ui_test.run_menu(ui_test.menu_config)

if __name__ == '__main__':
    main()

#################### CHATGPT 1st Various#################################
from pymysql import MySQLError
from pymongo import errors
from mysql_client import DB
from mongo_client import MongoDB
from ui import Menu
from logger import logger


def print_films(films):
    if len(films) == 0:
        print('Films not found.')

    for film in films:
        print(
            film['film_id'],
            film['title'],
            film['release_year'],
            film.get('categories')
            or film.get('name')
        )


def main():
    try:
        with DB() as db, MongoDB() as mongo:

            menu = Menu(
                [
                    'Search by keyword',
                    'Search by category and year',
                    'Show recent searches',
                    'Exit',
                ]
            )

            while True:

                match menu.show():

                    case 1:
                        keyword = input('Enter keyword: ').strip()
                        limit = 10
                        offset = 0

                        while True:
                            films = db.search_by_keyword(keyword, limit, offset,)
                            print_films(films)
                            mongo.save_search('keyword', keyword,)
                            answer = input('Show next page? y/n: ').lower()
                            if answer != 'y':
                                break
                            offset += limit

                    case 2:
                        categories = db.get_categories()
                        for category in categories:
                            print(
                                category['category_id'],
                                category['name']
                            )
                        year_range = db.get_year_range()
                        print(
                            f'Years: '
                            f'{year_range["MIN(release_year)"]}'
                            f' - '
                            f'{year_range["MAX(release_year)"]}'
                        )

                        category_id = int(input('Category id: '))
                        start_year = int(input('Start year: '))
                        end_year = int(input('End year: '))

                        films = (
                            db.search_by_category_and_year(
                                category_id,
                                start_year,
                                end_year,
                                10,
                                0,
                            )
                        )

                        print_films(films)

                        mongo.save_search(
                            'category_year',
                            {
                                'category_id': category_id,
                                'start_year': start_year,
                                'end_year': end_year,
                            }
                        )

                    case 3:
                        searches = (mongo.get_recent_searches())
                        for search in searches:
                            print(search)

                    case 4:
                        break

    except MySQLError as error:
        logger.error(error)

        print(f'MySQL error: {error}')

    except errors.PyMongoError as error:
        logger.error(error)

        print(f'MongoDB error: {error}')

    except Exception as error:
        logger.error(error)

        print(f'Unexpected error: {error}')


if __name__ == '__main__':
    main()
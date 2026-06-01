#файл работы с базой данных
import pymysql
from pymysql.cursors import DictCursor
from settings import MYSQL_CONFIG
import sql_queries


class DB:

    def __enter__(self):
        self.conn = pymysql.connect(**MYSQL_CONFIG, cursorclass=DictCursor)
        self.cursor = self.conn.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
        return False

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def search_by_keyword(self, keyword, limit, offset):
        return self.execute(sql_queries.SEARCH_FILMS_BY_KEYWORD,(f'%{keyword}%', limit, offset))

    def get_categories(self):
        return self.execute(sql_queries.GET_CATEGORIES)

    def get_year_range(self):
        year_range, = self.execute(sql_queries.GET_YEAR_RANGE)
        return year_range

    def search_by_year(self, start_year, end_year, limit, offset):
        return self.execute(sql_queries.SEARCH_BY_YEAR,(start_year, end_year, limit, offset))

    def search_by_category_and_year(self, category_id, start_year, end_year, limit, offset):
        return self.execute(
            sql_queries.SEARCH_BY_CATEGORY_AND_YEAR,(category_id, start_year, end_year, limit, offset))

    def search_by_category(self, category_id, limit, offset):
        return self.execute(sql_queries.SEARCH_BY_CATEGORY,(category_id, limit, offset))
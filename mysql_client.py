"""
MySQL database client.
Provides methods for working with the Sakila database,
executing SQL queries and retrieving movie information.
"""

import pymysql
from pymysql.cursors import DictCursor
from settings import MYSQL_CONFIG
import sql_queries


class DB:
    """
    MySQL database wrapper.
    Provides methods for:
    - movie search by keyword
    - movie search by category
    - movie search by year
    - movie search by category and year
    - retrieving categories
    - retrieving available year range
    Supports context manager protocol.
    """

    def __init__(self) -> None:
        """Initialize database attributes."""
        self.conn = None
        self.cursor = None

    def __enter__(self) -> "DB":
        """
        Open database connection.
        Creates MySQL connection and cursor.
        Returns: Current DB instance.
        """
        self.conn = pymysql.connect(**MYSQL_CONFIG, cursorclass=DictCursor)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Close database connection.
        Automatically closes cursor and connection
        when leaving context manager.
        Args: exc_type: Exception type.
              exc_val: Exception value.
              exc_tb: Exception traceback.
        Returns: False to propagate exceptions.
        """
        self.cursor.close()
        self.conn.close()
        return False

    def execute(self, query: str, params: tuple | None = None) -> list[dict]:
        """
        Execute SQL query.
        Args: query: SQL query string.
             params: Query parameters.
        Returns: List of rows returned by database.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def search_by_keyword(self, keyword: str, limit: int, offset: int) -> list[dict]:
        """
            Search movies by title keyword.
            Args: keyword: Search phrase.
                    limit: Number of records per page.
                   offset: Pagination offset.
            Returns: List of movies.
            """
        return self.execute(sql_queries.SEARCH_FILMS_BY_KEYWORD,(f'%{keyword}%', limit, offset))

    def get_categories(self) -> list[dict]:
        """
        Retrieve all movie categories.
        Returns: List of categories.
        """
        return self.execute(sql_queries.GET_CATEGORIES)

    def get_year_range(self) -> dict:
        """
        Retrieve minimum and maximum release years.
        Returns: Dictionary containing min_year and max_year.
        """
        year_range, = self.execute(sql_queries.GET_YEAR_RANGE)
        return year_range

    def search_by_year(self, start_year: int, end_year: int, limit: int, offset: int) -> list[dict]:
        """
            Search movies by year range.
            Args: start_year: Beginning of range.
                    end_year: End of range.
                       limit: Number of records.
                      offset: Pagination offset.
            Returns: List of movies.
            """
        return self.execute(sql_queries.SEARCH_BY_YEAR,(start_year, end_year, limit, offset))

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def search_by_category_and_year(self, category_id: int, start_year: int, end_year: int,
                                                limit: int, offset: int) -> list[dict]:
        """
            Search movies by category and year range.
            Args: category_id: Category identifier.
                   start_year: Beginning of range.
                     end_year: End of range.
                        limit: Number of records.
                       offset: Pagination offset.
            Returns: List of movies.
            """
        return self.execute(
            sql_queries.SEARCH_BY_CATEGORY_AND_YEAR,(category_id, start_year, end_year,
                                                                   limit, offset))

    def search_by_category(self, category_id: int, limit: int, offset: int) -> list[dict]:
        """
         Search movies by category.
         Args: category_id: Category identifier.
                     limit: Number of records.
                    offset: Pagination offset.
         Returns: List of movies.
         """
        return self.execute(sql_queries.SEARCH_BY_CATEGORY,(category_id, limit, offset))

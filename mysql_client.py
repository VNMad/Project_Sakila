"""MySQL database access layer."""

import pymysql
from pymysql.cursors import DictCursor
from settings import MYSQL_CONFIG
import sql_queries


class DB:
    """MySQL database client.
    Supports context manager protocol for automatic
    connection opening and closing."""
    def __enter__(self) -> "DB":
        """Open MySQL connection and create cursor.
        Returns: DB: Current database object."""
        self.conn = pymysql.connect(**MYSQL_CONFIG, cursorclass=DictCursor)
        self.cursor = self.conn.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Close cursor and database connection.
        Args:
            exc_type: Exception type if raised.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.
        Returns: bool: False to propagate exceptions."""
        self.cursor.close()
        self.conn.close()
        return False

    def execute(self, query: str, params: tuple | None = None) -> list[dict]:
        """Execute SQL query and return result.
           Args: query: SQL query string.
                params: Query parameters.
           Returns: list[dict]: Query result as list of dictionaries."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def search_by_keyword(self, keyword: str, limit: int, offset: int) -> list[dict]:
        """Search films by keyword."""
        return self.execute(sql_queries.SEARCH_FILMS_BY_KEYWORD,(f'%{keyword}%', limit, offset))

    def get_categories(self) -> list[dict]:
        """Return all movie categories."""
        return self.execute(sql_queries.GET_CATEGORIES)

    def get_year_range(self) -> dict:
        """Return min and max movie year."""
        year_range, = self.execute(sql_queries.GET_YEAR_RANGE)
        return year_range

    def search_by_year(self, start_year: int, end_year: int, limit: int, offset: int) -> list[dict]:
        """Search films by year range."""
        return self.execute(sql_queries.SEARCH_BY_YEAR,(start_year, end_year, limit, offset))

    def search_by_category_and_year(self, category_id: int, start_year: int, end_year: int, limit: int,
                                    offset: int) -> list[dict]:
        """Search films by category and year range."""
        return self.execute(
            sql_queries.SEARCH_BY_CATEGORY_AND_YEAR,(category_id, start_year, end_year, limit, offset))

    def search_by_category(self, category_id: int, limit: int, offset: int) -> list[dict]:
        """Search films by category."""
        return self.execute(sql_queries.SEARCH_BY_CATEGORY,(category_id, limit, offset))
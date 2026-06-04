"""
Custom exceptions and validation utilities.
Contains project-specific exceptions and
input validation functions.
"""

class MoviesPublishedYearError(Exception):
    """Raised when movie year is invalid."""


class CategoryNotFoundError(Exception):
    """Raised when category does not exist."""


class InvalidMenuChoiceError(Exception):
    """Raised when menu item is invalid."""


class InvalidYearRangeError(Exception):
    """Raised when start year is greater than end year."""


def validate_category(category_id: int, categories: list[dict]) -> None:
    """
    Validate category identifier.
    Args:  category_id: User selected category.
            categories: Available categories.
    Raises: CategoryNotFoundError
    """
    if not any(category['category_id'] == category_id for category in categories):
        raise CategoryNotFoundError('Category does not exist.')


def validate_year_range(start_year: int, end_year: int) -> None:
    """
        Validate year range boundaries.
        Checks that the start year is not greater
        than the end year.
        Args: start_year: Beginning of the selected year range.
                end_year: End of the selected year range.
        Raises: InvalidYearRangeError: If start year is greater than end year.
        """
    if start_year > end_year:
        raise InvalidYearRangeError('Start year cannot be greater than end year.')


def validate_year(year: int, min_year: int, max_year: int) -> None:
    """
        Validate a single year value.
        Checks whether the specified year is within
        the available movie release year range.
        Args:   year: Year entered by the user.
            min_year: Minimum available movie release year.
            max_year: Maximum available movie release year.
        Raises: MoviesPublishedYearError: If year is outside the allowed range.
        """
    if year < min_year or year > max_year:
        raise MoviesPublishedYearError(f'Year must be between {min_year} and {max_year}.')

def validate_years(start_year: int, end_year: int, min_year: int, max_year: int) -> None:
    """
        Validate year range.
        Checks:
        - year boundaries
        - start year <= end year
        Args: start_year: Beginning of range.
                end_year: End of range.
                min_year: Minimum available year.
                max_year: Maximum available year.
        """
    validate_year(start_year, min_year, max_year)
    validate_year(end_year, min_year, max_year)
    validate_year_range(start_year, end_year)


def validate_years_input(start_year_input: str, end_year_input: str,
                        min_year: int, max_year: int) -> tuple[int, int]:
    """
        Convert and validate user year input.
        Converts user input values to integers and
        validates the year range.

        Args: start_year_input: Start year entered by user.
                end_year_input: End year entered by user.
                      min_year: Minimum available movie release year.
                      max_year: Maximum available movie release year.
        Returns: Tuple containing validated start and end years.
        Raises: MoviesPublishedYearError:
                                        If input values are not numbers or
                                        years are outside the allowed range.
                   InvalidYearRangeError:
                                         If start year is greater than end year.
        """
    try:
        start_year = int(start_year_input)
        end_year = int(end_year_input)
    except ValueError as e:
        raise MoviesPublishedYearError('Year must be a number.') from e
    validate_years(start_year, end_year, min_year, max_year)
    return start_year, end_year

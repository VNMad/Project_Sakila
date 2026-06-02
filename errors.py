"""Custom exceptions and validation functions."""

class MoviesPublishedYearError(Exception):
    """Raised when movie year is invalid."""
    pass


class CategoryNotFoundError(Exception):
    """Raised when category does not exist."""
    pass


class InvalidMenuChoiceError(Exception):
    """Raised when menu item is invalid."""
    pass


class InvalidYearRangeError(Exception):
    """Raised when start year is greater than end year."""
    pass


def validate_category(category_id: int, categories: list[dict]) -> None:
    """Validate category existence."""
    if category_id not in [category['category_id'] for category in categories]:
        raise CategoryNotFoundError('Category does not exist.')


def validate_year_range(start_year: int, end_year: int) -> None:
    """Validate year range."""
    if start_year > end_year:
        raise InvalidYearRangeError('Start year cannot be greater than end year.')


def validate_year(year: int, min_year: int, max_year: int) -> None:
    """Validate single year."""
    if year < min_year or year > max_year:
        raise MoviesPublishedYearError(f'Year must be between {min_year} and {max_year}.')

def validate_years(start_year: int, end_year: int, min_year: int, max_year: int) -> None:
    """Validate year range and boundaries."""
    validate_year(start_year, min_year, max_year)
    validate_year(end_year, min_year, max_year)
    validate_year_range(start_year, end_year)


def validate_years_input(start_year_input: str, end_year_input: str, min_year: int, max_year: int) -> tuple[int, int]:
    """Convert and validate user year input."""
    try:
        start_year = int(start_year_input)
        end_year = int(end_year_input)
    except ValueError:
        raise MoviesPublishedYearError('Year must be a number.')
    validate_years(start_year, end_year, min_year, max_year)
    return start_year, end_year
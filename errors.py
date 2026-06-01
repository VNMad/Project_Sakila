class MoviesPublishedYearError(Exception):
    pass


class CategoryNotFoundError(Exception):
    pass


class InvalidMenuChoiceError(Exception):
    pass


class InvalidYearRangeError(Exception):
    pass


def validate_category(category_id, categories):
    if category_id not in [category['category_id'] for category in categories]:
        raise CategoryNotFoundError('Category does not exist.')


def validate_year_range(start_year, end_year):
    if start_year > end_year:
        raise InvalidYearRangeError('Start year cannot be greater than end year.')


def validate_year(year, min_year, max_year):
    if year < min_year or year > max_year:
        raise MoviesPublishedYearError(f'Year must be between {min_year} and {max_year}.')

def validate_years(start_year, end_year, min_year, max_year):
    validate_year(start_year, min_year, max_year)
    validate_year(end_year, min_year, max_year)
    validate_year_range(start_year, end_year)


def validate_years_input(start_year_input, end_year_input, min_year, max_year):
    try:
        start_year = int(start_year_input)
        end_year = int(end_year_input)
    except ValueError:
        raise MoviesPublishedYearError('Year must be a number.')
    validate_years(start_year, end_year, min_year, max_year)
    return start_year, end_year
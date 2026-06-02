"""Application user interface and menu handling."""

import sys

from mysql_client import DB
from mongo_client import MongoDB
from logger_sakila import logger_decorator
import errors


def print_films(films: list[dict]) -> None:
    """Print movie information."""
    if not films:
        print('No movies found for your request.')
        return
    for film in films:
        print(
            ('=' * 130) + '\n'
            + f"ID          : {film['film_id']}\n"
            + f"Title       : {film['title']}\n"
            + f"Year        : {film['release_year']}\n"
            + f"Category    : {film['categories']}\n"
            + f"Language    : {film['language_name']}\n"
            + f"Description : {film['description']}\n"
            + ('=' * 130)
        )

def paginate_movies(search_function, limit: int = 10, offset: int = 0) -> None:
    """Display movies page by page."""
    while True:
        films = search_function(limit, offset)
        if not films:
            if offset == 0:
                print('No movies found for your request..')
            break
        print_films(films)
        answer = input('Show next page? y/n: ').lower()
        if answer != 'y':
            break
        offset += limit

def print_popular_searches(searches: list[dict]) -> None:
    """Print search statistics."""
    if not searches:
        print('Search history is empty.')
        return
    separator = '-' * 100
    for search in searches:
        if 'count' in search:
            search_type = search['_id']['search_type']
            value = search['_id']['value']
            count = search['count']
            extra_info = f'Count: {count}'

        else:
            search_type = search['search_type']
            value = search['value']
            date = search['created_at'].strftime('%Y-%m-%d %H:%M')
            extra_info = f'Date: {date}'
        if search_type == 'keyword':
            formatted_value = value
        elif search_type == 'genre':
            formatted_value = value
        elif search_type == 'year':
            formatted_value = (
                f"{value['start_year']} - "
                f"{value['end_year']}"
            )
        elif search_type == 'genre_year':
            formatted_value = (
                f"{value['category']} | "
                f"{value['start_year']} - "
                f"{value['end_year']}"
            )
        else:
            formatted_value = value

        print(
            f"{separator}\n"
            f"Type  : {search_type}\n"
            f"Value : {formatted_value}\n"
            f"{extra_info}\n"
            f"{separator}"
        )

@logger_decorator
def handle_search_keyword_movies() -> None:
    """Search movies by keyword."""
    keyword = input('Enter keyword: ').strip()
    with DB() as db, MongoDB() as mongo:
        mongo.save_search('keyword', keyword,)
        paginate_movies(lambda limit, offset:
                db.search_by_keyword(keyword, limit, offset))


@logger_decorator
def handle_search_genre_movies() -> None:
    """Search movies by genre."""
    with DB() as db, MongoDB() as mongo:
        categories = db.get_categories()
        for category in categories:
            print(category['category_id'], category['name'])
        category_id = int(input('Enter category id: '))
        errors.validate_category(category_id, categories)
        selected_category = next(category['name'] for category in categories if category['category_id'] == category_id)
        mongo.save_search('genre', selected_category)
        paginate_movies(lambda limit, offset:
                db.search_by_category(category_id, limit, offset))


@logger_decorator
def handle_search_year_movies() -> None:
    """Search movies by year range."""
    with DB() as db, MongoDB() as mongo:
        year_range = db.get_year_range()
        print('Available years:', year_range['min_year'],'-', year_range['max_year'])
        start_year, end_year = errors.validate_years_input(
            input('Enter start year: '),
            input('Enter end year: '),
            year_range['min_year'],
            year_range['max_year']
        )
        mongo.save_search('year',{'start_year': start_year, 'end_year': end_year})
        paginate_movies(lambda limit, offset: db.search_by_year(start_year, end_year, limit, offset))


@logger_decorator
def handle_search_movies() -> None:
    """Search movies by genre and year."""
    with DB() as db, MongoDB() as mongo:
        categories = db.get_categories()
        for category in categories:
            print(category['category_id'], category['name'])
        category_id = int(input('Enter category id: '))
        errors.validate_category(category_id, categories)
        year_range = db.get_year_range()
        print('Available years:', year_range['min_year'],'-', year_range['max_year'])
        start_year, end_year = errors.validate_years_input(
            input('Enter start year: '),
            input('Enter end year: '),
            year_range['min_year'],
            year_range['max_year']
        )
        selected_category = next(category['name'] for category in categories if category['category_id'] == category_id)
        mongo.save_search('genre_year',{
                'category': selected_category,
                'start_year': start_year,
                'end_year': end_year,
            }
        )
        paginate_movies(lambda limit, offset:
                db.search_by_category_and_year(category_id, start_year, end_year, limit, offset))


@logger_decorator
def handle_popular_top_queries() -> None:
    """Show top searched requests."""
    with MongoDB() as mongo:
        searches = mongo.get_top_searches()
        print_popular_searches(searches)


@logger_decorator
def handle_popular_last_queries() -> None:
    """Show latest search requests."""
    with MongoDB() as mongo:
        searches = mongo.get_recent_searches()
        print_popular_searches(searches)


menu_config = {
    'title': 'Main menu',
    'items': {
        '1': {'text': 'Search movies',
            'submenu': {'title': 'Movies search menu',
                'items': {
                    '1': {'text': 'Search by keyword in title', 'action': handle_search_keyword_movies},
                    '2': {'text': 'Search by genre', 'action': handle_search_genre_movies},
                    '3': {'text': 'Search by year', 'action': handle_search_year_movies},
                    '4': {'text': 'Search by genre and year', 'action': handle_search_movies},
                    '0': {'text': 'Back', 'action': 'back'},
                         }
                       }
             },
        '2': {'text': 'Popular searches',
            'submenu': {'title': 'Popular searches menu',
                'items': {
                    '1': {'text': 'Last 10 searches', 'action': handle_popular_last_queries},
                    '2': {'text': 'Top 5 searches', 'action': handle_popular_top_queries},
                    '0': {'text': 'Back', 'action': 'back'},
                         }
                       }
             },
        '0': {'text': 'Exit', 'action': lambda: sys.exit(0)}
    }
}


def run_menu(config: dict) -> None:
    """Run interactive application menu."""
    stack = [config]
    while stack:
        current_menu = stack[-1]
        print(f'\n{current_menu["title"]}')
        for key, value in (current_menu['items'].items()):
            print(f'{key}. {value["text"]}')
        choice = input('Choose menu item: ')
        if choice in current_menu['items']:
            menu_item = (current_menu['items'][choice])
            if menu_item.get('action') == 'back':
                stack.pop()
            elif 'submenu' in menu_item:
                stack.append(menu_item['submenu'])
            elif 'action' in menu_item:
                menu_item['action']()
        else:
            print('Invalid menu option. Please choose from the options above.')
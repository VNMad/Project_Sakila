import sys

def handle_search_genre_movies():
    print('Hello')
    # выполняем нужные действия по поиску фильмов

def handle_search_year_movies():
    print('Hello')
    # выполняем нужные действия по поиску фильмов

def handle_search_keyword_movies():
    print('Hello')
    # выполняем нужные действия по поиску фильмов

def handle_search_movies():
    print('Hello')
    # выполняем нужные действия по поиску фильмов

def handle_popular_top_queries():
    print('Hello')
    # выполняем нужные действия по показу популярных запросов

def handle_popular_last_queries():
    print('Hello')
    # выполняем нужные действия по показу популярных запросов


menu_config = {
    'title': 'Главное меню',
    'items': {
        '1':
            {
                'text': 'Поиск фильмов',
                'submenu':{
                    'title': 'Меню поиска фильмов',
                    'items':{
                        '1': {'text': 'Поиск по слову', 'action': handle_search_keyword_movies, },
                        '2': {'text': 'Поиск по жанру', 'action': handle_search_genre_movies, },
                        '3': {'text': 'Поиск по году',   'action': handle_search_year_movies, },
                        '4': {'text': 'Поиск по жанру и году',   'action': handle_search_movies, },
                        '0': {'text':'Назад', 'action': 'back'},
                            }
                           }
            },
        '2': {
                'text': 'Поиск популярных запросов',
                'submenu':{
                    'title': 'Меню поиска популярных запросов',
                    'items':{
                        '1': {'text': 'Последние 5 запросов', 'action': handle_popular_top_queries, },
                        '2': {'text': 'ТОП 5 запросов',   'action': handle_popular_last_queries, },
                        '0': {'text':'Назад', 'action': 'back'},
                            }
                           }
            },
        '0': {'text': 'Выход', 'action': lambda: sys.exit(0)}
    }
}

def run_menu(config):
    stack = [config]
    while stack:
        current_menu = stack[-1]

        for key, value in current_menu['items'].items():
            print(f'{key}: {value["text"]}')

        choice = input('Выберите пункт меню: ')

        if choice in current_menu['items']:
            menu_item = current_menu['items'][choice]
            if menu_item.get('action') == 'back':
                stack.pop()
            elif 'submenu' in menu_item:
                stack.append(menu_item['submenu'])
            elif 'action' in menu_item:
                menu_item['action']()
        else:
            print('Неверный пункт меню. Выберите из предложенных выше.')
        # match choice:
        #     case '1':
        #         menu_config['1']['action']()
        #     case '2':
        #         menu_config['2']['action']()
        #     case '0':
        #         menu_config['0']['action']()
        # action = menu_config.get(choice)
        # if action:
        #     action['action']()

###############CHATGPT 1st VARIOUS########################
class Menu:

    def __init__(self, items):
        self.items = items

    def show(self):
        for index, item in enumerate(self.items, start=1,):
            print(f'{index}. {item}')

        while True:
            try:
                choice = int(input('Choose action: '))
                if 1 <= choice <= len(self.items):
                    return choice
                raise ValueError
            except ValueError:
                print('Invalid menu number.')
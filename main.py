"""
Application entry point.
Starts the movie search system and launches
the main user interface menu.
"""

import ui


def main():
    """
    Start application.
    Runs the main menu interface.
    Returns: None
    """
    ui.run_menu(ui.menu_config)


if __name__ == '__main__':
    main()

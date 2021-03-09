import arcade

from views.main_view import MainView
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    window = arcade.Window(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE)
    menu_view = MainView(window)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

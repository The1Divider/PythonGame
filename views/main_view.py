import arcade

from sprites import Button
from mechanics import Vector
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


from views.game_view import GameView

MAIN_MENU_SPACER = SCREEN_WIDTH / 25

MAIN_MENU_BUTTON_WIDTH = (SCREEN_WIDTH - MAIN_MENU_SPACER * 4) / 3
MAIN_MENU_BUTTON_HEIGHT = SCREEN_HEIGHT / 10


class MainView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
        self.game_view = GameView(window)

        arcade.set_background_color(arcade.color.GREEN)

        self.b1 = Button(x=MAIN_MENU_SPACER + MAIN_MENU_BUTTON_WIDTH / 2,
                         y=MAIN_MENU_BUTTON_HEIGHT * 2.5,
                         width=MAIN_MENU_BUTTON_WIDTH,
                         height=MAIN_MENU_BUTTON_HEIGHT,
                         colour=arcade.color.BLUE,
                         text="New Game",
                         text_size=25,
                         text_colour=arcade.color.BLACK)

        self.b2 = Button(x=MAIN_MENU_SPACER * 2 + MAIN_MENU_BUTTON_WIDTH * 1.5,
                         y=MAIN_MENU_BUTTON_HEIGHT * 2.5,
                         width=MAIN_MENU_BUTTON_WIDTH,
                         height=MAIN_MENU_BUTTON_HEIGHT,
                         colour=arcade.color.BLUE,
                         text="Load Game",
                         text_size=25,
                         text_colour=arcade.color.BLACK)

        self.b3 = Button(x=MAIN_MENU_SPACER * 3 + MAIN_MENU_BUTTON_WIDTH * 2.5,
                         y=MAIN_MENU_BUTTON_HEIGHT * 2.5,
                         width=MAIN_MENU_BUTTON_WIDTH,
                         height=MAIN_MENU_BUTTON_HEIGHT,
                         colour=arcade.color.BLUE,
                         text="Quit",
                         text_size=25,
                         text_colour=arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(text="SEA SHANTIES!!!",
                         start_x=SCREEN_WIDTH / 2,
                         start_y=SCREEN_WIDTH * 2 / 3,
                         color=arcade.color.WHITE,
                         font_size=45,
                         anchor_x='center')

        [b.draw() for b in (self.b1, self.b2, self.b3)]

    def on_mouse_press(self, x, y, button, key_modifier):
        coords = Vector(x, y)
        if coords in self.b1:
            self.window.show_view(self.game_view)
        if coords in self.b2:
            self.window.show_view(self.game_view)
        if coords in self.b3:
            print("B3")

    def on_key_press(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.ESCAPE:
            arcade.close_window()

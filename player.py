import arcade

from mechanics import Vector, BoolVector
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Controller:
    def __init__(self, bus, map_locks: BoolVector):
        self.map_locks = map_locks
        self.bus = bus
        self.pos = Vector(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        self.bus.listen("move", self.move)
        self.bus.listen("draw_player", self.draw)
        self.bus.listen("player_position", self.get_player_pos)

    def set_sprite(self, direction): pass

    def get_player_pos(self):
        return self.pos.copy()

    def draw(self):
        arcade.draw_rectangle_filled(self.pos.x, self.pos.y, 20, 20, arcade.color.BLACK)

    def move(self, displacement: Vector):
        """
        if not self.map_locks.x_locked:
            self.pos.x = SCREEN_WIDTH // 2
            displacement.x = 0

        if not self.map_locks.y_locked:
            self.pos.y = SCREEN_HEIGHT // 2
            displacement.y = 0"""

        if self.map_locks.x_locked:
            if self.pos.x > SCREEN_WIDTH // 2 and self.map_locks.xl:
                self.map_locks.unlock('xl')
            elif self.pos.x < SCREEN_WIDTH // 2 and self.map_locks.xr:
                self.map_locks.unlock('xr')
        else:
            displacement.x = 0

        if self.map_locks.y_locked:
            if self.pos.y > SCREEN_HEIGHT // 2 and self.map_locks.yl:
                self.map_locks.unlock('yl')
            elif self.pos.y < SCREEN_HEIGHT // 2 and self.map_locks.yr:
                self.map_locks.unlock('yr')
        else:
            displacement.y = 0

        self.pos += displacement


class Player:
    def __init__(self, bus, map_locks):
        self.controller = Controller(bus, map_locks)







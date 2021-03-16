from typing import Any

import arcade
import arcade.color as c

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, TILE_OFFSET, MAP_SIZE_X, MAP_SIZE_Y
from mechanics import Vector, BoolVector, Dimension


class Render:
    def __init__(self, world_map, bus, map_locks: BoolVector):
        self.bus = bus
        self.tile_map = Map(world_map)
        starting_pos = Vector(self.tile_map.dim.length//2, self.tile_map.dim.height//2)
        self.cam = Camera(self.tile_map, starting_pos, self.bus, map_locks)

        self.first_render = True

        self.bus.listen("move", self.update)
        self.bus.listen("draw", self.cam.draw)

    def update(self, move: Vector):  # keep player centered with this method
        if self.first_render:
            self.first_render = False
        else:
            move = move

        self.cam.update(move=move)


class Map:
    def __init__(self, tile_map: list[list]):
        self.tile_map = tile_map
        self.dim = Dimension(len(self.tile_map[0]), len(self.tile_map))
        print(self.dim)
        self.tile_values = {-1: c.WHITE, 0: c.GRAY, 1: c.BLACK, 2: c.RED, 3: c.ORANGE, 4: c.YELLOW,
                            5: c.GREEN, 6: c.BLUE, 7: c.PURPLE}


class Camera:
    """TODO
    Movement is still very janky but it's a step in the right direction:
        studdering/bad rendering being caused by y direction
        it does fix itself tho which is nice

        studdering/bad rendering when x + y are moving?

        test_map_word: flickering on last H line (horizontally) -> figure that out

        bounds are fucky in both directions (x.left seems to work?)"""
    def __init__(self, tile_map: Map, initial_pos: Vector, bus, map_locks: BoolVector):
        self.bus = bus
        self.pos = initial_pos
        self.tile_map = tile_map
        self.offset = Vector(0, 0)
        self._start = Vector(0, 0)
        self._stop = Vector(0, 0)
        self.locks = map_locks
        self.last_pos = Vector(0, 0)

    @property
    def on_left_edge_of_map_x(self):
        return self.start.x + TILE_OFFSET == 0 and self.offset.x == 0

    @property
    def on_right_edge_of_map_x(self):
        return self.stop.x == self.tile_map.dim.length - 1 and self.offset.x == 0

    @property
    def on_left_edge_of_map_y(self) -> bool:
        return self.start.y == 0 and self.offset.y == 0

    @property
    def on_right_edge_of_map_y(self) -> bool:
        return self.stop.y == self.tile_map.dim.height - 1 and self.offset.y == 0

    def update_pos(self):  # updating screen pos not player
        if self.pos.x <= SCREEN_WIDTH // 2:
            self.pos.x = SCREEN_WIDTH // 2
        if self.pos.x > self.tile_map.dim.length * TILE_SIZE - SCREEN_WIDTH:
            self.pos.x = self.tile_map.dim.length * TILE_SIZE - SCREEN_WIDTH
        if self.pos.y < SCREEN_HEIGHT // 2:
            self.pos.y = SCREEN_HEIGHT // 2
        if self.pos.y > self.tile_map.dim.height * TILE_SIZE - SCREEN_HEIGHT:
            self.pos.y = self.tile_map.dim.height * TILE_SIZE - SCREEN_HEIGHT

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, new_start: Vector):
        """Clamp x & y start pointers"""
        if new_start.x < 0:
            self._start.x = 0
        else:
            self._start.x = new_start.x

        if new_start.y < 0:
            self._start.y = 0
        else:
            self._start.y = new_start.y

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, new_stop: Vector):
        """Clamp x & y stop pointers"""
        if new_stop.x > self.tile_map.dim.length - 1:
            self._stop.x = self.tile_map.dim.length - 1
        else:
            self._stop.x = new_stop.x

        if new_stop.y > self.tile_map.dim.height - 1:
            self._stop.y = self.tile_map.dim.height - 1
        else:
            self._stop.y = new_stop.y

    def update(self, move: Vector):
        if self.locks.x_locked:
            move.x = 0
        if self.locks.y_locked:
            move.y = 0

        self.pos += move
        self.update_pos()
        locks = self.locks

        if not locks.x_locked:
            start_x, stop_x, offset_x = self._update_x()
        else:
            start_x, stop_x, offset_x = self.start.x, self.stop.x, self.offset.x

        if not locks.y_locked:
            start_y, stop_y, offset_y = self._update_y()
        else:
            start_y, stop_y, offset_y = self.start.y, self.stop.y, self.offset.y

        self.start = Vector(start_x, start_y)
        self.stop = Vector(stop_x, stop_y)
        self.offset = Vector(offset_x, offset_y)

        self.locks.x_locked = self.on_left_edge_of_map_x, self.on_right_edge_of_map_x
        self.locks.y_locked = self.on_left_edge_of_map_y, self.on_right_edge_of_map_y
        print(self.on_left_edge_of_map_x, self.on_right_edge_of_map_x)
        print(self.on_left_edge_of_map_y, self.on_right_edge_of_map_y)

    def _update_x(self) -> tuple[int, int, int]:
        left_x_of_screen = (self.pos.x - (SCREEN_WIDTH // 2))
        right_x_of_screen = left_x_of_screen + SCREEN_WIDTH

        start = left_x_of_screen // TILE_SIZE - TILE_OFFSET
        stop = right_x_of_screen // TILE_SIZE + TILE_OFFSET

        # player offset
        offset = self.pos.x % TILE_SIZE

        return start, stop, offset

    def _update_y(self) -> tuple[int, int, int]:
        top_y_of_screen = (self.pos.y - (SCREEN_HEIGHT // 2))
        bottom_y_of_screen = top_y_of_screen + SCREEN_HEIGHT

        start = top_y_of_screen // TILE_SIZE - TILE_OFFSET
        stop = bottom_y_of_screen // TILE_SIZE + TILE_OFFSET

        # player  offset
        offset = self.pos.y % TILE_SIZE

        return start, stop, offset

    def draw(self):
        start, stop = self.start, self.stop
        pos = self.bus.get("player_position")

        print(start.x, stop.x, start.y, stop.y)
        print(self.pos)
        for y in range(start.y, stop.y):  # might be 1 off
            for x in range(start.x, stop.x):
                texture = self.tile_map.tile_values[self.tile_map.tile_map[y][x]]
                arcade.draw_rectangle_filled(center_x=((pos.x - self.offset.x - SCREEN_WIDTH // 2) + TILE_SIZE // 2) + TILE_SIZE * (x-start.x),
                                             center_y=((pos.y - self.offset.y - SCREEN_HEIGHT // 2) + TILE_SIZE // 2) + TILE_SIZE * (y-start.y),
                                             width=TILE_SIZE,
                                             height=TILE_SIZE,
                                             color=texture)
        else:
            self.bus.command("draw_player")


class RenderBus:
    def __init__(self):
        self.listeners = {}

    def listen(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def emit(self, event_type, payload):
        for listener in self.listeners.get(event_type, []):
            if isinstance(payload, Vector):
                _payload = payload.copy()
            else:
                _payload = payload
            listener(_payload)

    def command(self, event_type):
        for listener in self.listeners.get(event_type, []):
            listener()

    def get(self, event_type) -> Any:
        for listener in self.listeners.get(event_type, []):
            return listener()

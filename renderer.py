import arcade
import arcade.color as c

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, TILE_OFFSET
from mechanics import Vector


class Render:
    def __init__(self, world_map, bus):
        self.bus = bus
        self.camera_lock_x, self.camera_lock_y = False, False
        self.x_offset, self.y_offset = None, None

        self.x_start = (self.map_dimensions.x // 2 - SCREEN_WIDTH // 2) * TILE_SIZE - TILE_OFFSET
        self.x_stop = (dx + SCREEN_WIDTH // 2) * TILE_SIZE + TILE_OFFSET
        self.y_start = (dy - SCREEN_HEIGHT // 2) * TILE_SIZE - TILE_OFFSET
        self.y_stop = (dy + SCREEN_HEIGHT // 2) * TILE_SIZE + TILE_OFFSET

        self.map = world_map
        self.map_dimensions = Vector(len(self.map[0]), len(self.map))
        self.tile_values = {-1: c.WHITE, 0: c.GRAY, 1: c.BLACK, 2: c.RED, 3: c.ORANGE, 4: c.YELLOW,
                            5: c.GREEN, 6: c.BLUE, 7: c.PURPLE}

        self.bus.listen("moved", self.update)
        self.bus.listen("draw", self.draw)

    def update(self, move: Vector):  # keep player centered with this method
        move = -move
        if not self.camera_lock_x:
            self._update_x(int(move.x))

        if not self.camera_lock_y:
            self._update_y(int(move.y))

        _clx = self.camera_lock_x
        _cly = self.camera_lock_y
        # check if camera needs to be locked
        self.camera_lock_x = self.on_edge_of_map_x()
        self.camera_lock_y = self.on_edge_of_map_y()

        if (_clx, _cly) != (self.camera_lock_x, self.camera_lock_y):
            self.bus.emit("update_locks", (self.camera_lock_x, self.camera_lock_y))

    # noinspection DuplicatedCode
    def _update_x(self, dx: int):
        print("Update x is called")
        self.x_offset = dx % 10
        self.x_start = (dx - SCREEN_WIDTH // 2) * TILE_SIZE - TILE_OFFSET
        self.x_stop = (dx + SCREEN_WIDTH // 2) * TILE_SIZE + TILE_OFFSET

        if self.x_start < 0:
            self.x_start = 0

        if self.x_stop > self.map_dimensions.x - 1:
            self.x_stop = self.map_dimensions.x - 1

    # noinspection DuplicatedCode
    def _update_y(self, dy: int):
        print("Update y is called")
        self.y_offset = dy % 10
        self.y_start = (dy - SCREEN_HEIGHT // 2) * TILE_SIZE - TILE_OFFSET
        self.y_stop = (dy + SCREEN_HEIGHT // 2) * TILE_SIZE + TILE_OFFSET

        if self.y_start < 0:
            self.y_start = 0

        if self.y_stop > self.map_dimensions.y - 1:
            self.y_stop = self.map_dimensions.y - 1

    def on_edge_of_map_x(self) -> bool:
        return True if self.x_start == 0 or self.x_stop == self.map_dimensions.x - 1 else False

    def on_edge_of_map_y(self) -> bool:
        return True if self.y_start == 0 or self.y_stop == self.map_dimensions.y - 1 else False

    def draw(self):
        for y in range(self.y_start, self.y_stop):  # might be 1 off
            for x in range(self.x_start, self.x_stop):
                texture = self.tile_values[self.map[x][y]]
                arcade.draw_rectangle_filled(center_x=TILE_SIZE // 2 * (x - self.x_start) - self.x_offset,
                                             center_y=TILE_SIZE // 2 * (y - self.y_start) - self.y_offset,
                                             width=TILE_SIZE,
                                             height=TILE_SIZE,
                                             color=texture)


class RenderBus:
    def __init__(self):
        self.listeners = {}

    def listen(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def emit(self, event_type, payload):
        if event_type == "update_locks": print('Update Locks')
        for listener in self.listeners.get(event_type, []):
            listener(payload)

    def command(self, event_type):
        for listener in self.listeners.get(event_type, []):
            listener()

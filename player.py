import arcade

from mechanics import Vector


class Controller:
    def __init__(self, bus):
        self.bus = bus
        self.player_lock_x, self.player_lock_y = True, True
        self.bus.listen("update_locks", self.update_locks)

    def set_sprite(self, direction): pass

    def update_locks(self, locks: tuple[bool, bool]):
        self.player_lock_x, self.player_lock_y = not locks[0], not locks[1]


class Player:
    def __init__(self, bus):
        self.controller = Controller(bus)
        self.pos = Vector(500, 500)
        self.bus = bus

        self.bus.listen("moved", self.move)
        self.bus.listen("draw", self.draw)

    def move(self, displacement: Vector):
        if self.controller.player_lock_x:
            displacement.x = 0
        if self.controller.player_lock_y:
            displacement.y = 0
        self.pos += displacement

    def draw(self):
        arcade.draw_rectangle_filled(self.pos.x, self.pos.y, 20, 20, arcade.color.BLACK)

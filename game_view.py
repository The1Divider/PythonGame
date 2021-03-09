import queue
import arcade

from main_map import main_map
from mechanics import Signal, Vector
from player import Player
from renderer import Render, RenderBus
from constants import (SPRINT_VALUE, CROUCH_VALUE, SPRINT_BINDING, CROUCH_BINDING, SPRINT_MOD_BINDING,
                       CROUCH_MOD_BINDING, UP_BINDING, DOWN_BINDING, LEFT_BINDING, RIGHT_BINDING)


class GameView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
        self.bus = RenderBus()
        self.camera = Render(main_map, self.bus)
        self.player = Player(self.bus)
        self.camera.update(self.player.pos)
        self.signal_processor = SignalProcessing(self.bus)

        # signal lookup
        self.key_dict = {UP_BINDING: "up",
                         DOWN_BINDING: "down",
                         LEFT_BINDING: "left",
                         RIGHT_BINDING: "right",
                         SPRINT_BINDING: "sprint",
                         CROUCH_BINDING: "crouch"}

        # mod signal lookup
        self.mod_dict = {SPRINT_MOD_BINDING: "sprint",
                         CROUCH_MOD_BINDING: "crouch",}

    def on_draw(self):
        arcade.start_render()
        self.camera.draw()
        self.player.draw()

    def on_update(self, dt: float):
        self.signal_processor.update()

    def on_key_press(self, _symbol: int, _modifiers: int):
        if _symbol == arcade.key.ESCAPE:
            arcade.close_window()

        if _symbol in self.key_dict:  # change dict lookup to .get()?
            _signal = Signal(name=self.key_dict[_symbol],
                             value=True,
                             modifier=self.mod_dict.get(_modifiers - 256))
            self.bus.emit("key_press", _signal)
            self.signal_processor.signal_queue.put(_signal)

    def on_key_release(self, _symbol: int, _modifiers: int):
        if _symbol in self.key_dict:
            _signal = Signal(self.key_dict[_symbol], False)
            self.signal_processor.signal_queue.put(_signal)


class SignalProcessing:
    def __init__(self, bus):
        self.bus = bus
        self.up, self.down, self.left, self.right = False, False, False, False
        self.sprint, self.crouch = False, False
        self.signal_queue = queue.Queue()

        # signal switches
        self.directions = {"up": self.up,
                           "down": self.down,
                           "left": self.left,
                           "right": self.right}

        # mod switches
        self.mods = {"sprint": self.sprint,
                     "crouch": self.crouch}

        # values of movement
        self.move_dict = {"up": Vector(0, 5),
                          "down": Vector(0, -5),
                          "left": Vector(-5, 0),
                          "right": Vector(5, 0)}

        # values of mods
        self.move_mod_dict = {"sprint": SPRINT_VALUE,
                              "crouch": CROUCH_VALUE}

    def process_key_signal(self) -> Vector:
        displacement = Vector(0, 0)
        _mod = 1

        # check signal queue
        while not self.signal_queue.empty():
            signal: Signal = self.signal_queue.get()
            name = signal.name
            value = signal.value
            mod = signal.modifier

            if signal.name in ("sprint", "crouch"):
                self.mods[name] = value

            elif name in ("up", "down", "left", "right"):
                self.directions[name] = value

                if mod is not None:
                    self.mods[mod] = True

        # update pos based on signal & mod switches
        for direction, move in self.directions.items():
            if move:
                displacement += self.move_dict[direction]
        else:
            for mod, used in self.mods.items():
                if used:
                    print(self.move_mod_dict.get(mod, 1))

                    _mod *= self.move_mod_dict.get(mod, 1)

        return displacement * _mod

    def update(self):
        signal = self.process_key_signal()
        if signal is not None:
            self.bus.emit("moved", signal)

        self.bus.command("draw")

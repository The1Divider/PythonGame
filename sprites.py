from typing import Optional, Tuple

import arcade

from mechanics import Vector, Dimension


class Button:
    def __init__(self, x: float, y: float, width: float, height: float,
                 colour: arcade.color, text: Optional[str] = "",
                 text_colour: tuple[int, int, int] = arcade.color.BLACK,
                 text_size: int = 45):
        self._l1, self._l2, self._r1, self._r2 = None, None, None, None
        self.text = text
        self.text_colour = text_colour
        self.text_size = text_size
        self.center = Vector(x, y), Dimension(width, height)
        self.colour = colour

    def __contains__(self, pos: Vector) -> bool:
        """Check if vector is in range of button"""
        if self._l1.x < pos.x < self._r1.x and self._l1.y < pos.y < self._l2.y:
            return True
        else:
            return False

    @property
    def center(self):
        pass

    @center.setter
    def center(self, _in: Tuple[Vector, Dimension]):
        _center, _dim = _in

        cx = _center.x
        cy = _center.y

        dx = _dim.length / 2
        dy = _dim.height / 2

        left = cx - dx
        right = cx + dx

        top = cy - dy
        bottom = cy + dy

        self._l1 = Vector(left, top)
        self._l2 = Vector(left, bottom)
        self._r1 = Vector(right, top)
        self._r2 = Vector(right, bottom)

    @center.getter
    def center(self):
        return Vector((self._l1.x + self._r1.x) / 2, (self._l1.y + self._l2.y) / 2)

    @property
    def dim(self) -> Dimension:
        return Dimension(self._r1.x - self._l1.x, self._l2.y - self._l1.y)

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.dim.length, self.dim.height, self.colour)
        self.set_text()

    def set_text(self):
        arcade.draw_text(text=self.text,
                         start_x=self.center.x,
                         start_y=self.center.y,
                         color=self.text_colour,
                         font_size=self.text_size,
                         anchor_x='center',
                         anchor_y='center')


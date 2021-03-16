from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, Union, Optional


# rename to internals?


class Dimension(NamedTuple):
    length: float
    height: float

    def __str__(self):
        return f"object is ({self.length} * {self.height})"


@dataclass
class Vector:
    x: Union[int, float]
    y: Union[int, float]

    def __str__(self):
        return f"(x={self.x}px, y={self.y}px)"

    def __add__(self, other: Vector) -> Vector:
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other: Union[Vector, int, float]) -> Vector:
        if isinstance(other, Vector):
            raise NotImplemented

        elif isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            return self

    def __neg__(self):
        self.x = -self.x
        self.y = -self.y
        return self

    def vint(self) -> Vector:
        self.x = int(self.x)
        self.y = int(self.y)
        return self

    def copy(self):
        return Vector(self.x, self.y)


@dataclass
class BoolVector:
    xl: bool
    xr: bool
    yl: bool
    yr: bool
    _x: tuple[bool, bool] = ()
    _y: tuple[bool, bool] = ()

    @property
    def x_locked(self):
        return self.xl or self.xr

    @x_locked.setter
    def x_locked(self, values: tuple[bool, bool]):
        self._x = values

    @property
    def y_locked(self):
        return self.yl or self.yr

    @y_locked.setter
    def y_locked(self, values: tuple[bool, bool]):
        self._y = values

    def __ne__(self, other):
        self.x = not self.x[0], not self.x[1]
        self.y = not self.y[0], not self.y[1]
        return self

    def __str__(self):
        return f"(lock_x={self.x}, lock_y={self.y})"

    def lock(self, lock: str):
        if lock == 'x':
            self.x_locked = False, False
        if lock == 'y':
            self.y_locked = False, False
        elif lock in ('xl', 'xr', 'yl', 'yr'):
            setattr(self, lock, False)
        else:
            raise KeyError

    def unlock(self, lock: str):
        if lock == 'x':
            self.x_locked = True, True
        if lock == 'y':
            self.y_locked = True, True
        elif lock in ('xl', 'xr', 'yl', 'yr'):
            setattr(self, lock, True)
        else:
            raise KeyError


@dataclass
class Signal:
    name: str
    value: Union[int, float, str, bool]
    modifier: Optional[str] = None

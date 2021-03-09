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
    x: float
    y: float

    def __str__(self):
        return f"x = {self.x}px |//|\\\\| y = {self.y}px"

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

@dataclass
class Signal:
    name: str
    value: Union[int, float, str, bool]
    modifier: Optional[str] = None

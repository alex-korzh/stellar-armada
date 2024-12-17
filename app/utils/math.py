from dataclasses import dataclass

from pygame import Vector2, Rect


def rect_from_center(center: Vector2, size: Vector2) -> Rect:
    return Rect(
        center.x - size.x // 2,
        center.y - size.y // 2,
        size.x,
        size.y,
    )


@dataclass
class V2:
    x: int
    y: int

    def get_neighbors(self) -> list["V2"]:
        return [
            V2(self.x + 1, self.y),
            V2(self.x - 1, self.y),
            V2(self.x, self.y + 1),
            V2(self.x, self.y - 1),
        ]

    def as_vector2(self) -> Vector2:
        return Vector2(self.x, self.y)

    def __add__(self, other: "V2") -> "V2":
        return V2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "V2") -> "V2":
        return V2(self.x - other.x, self.y - other.y)
    
    def __floordiv__(self, other: int) -> "V2":
        return V2(self.x // other, self.y // other)

    def in_range(self, min: "V2", max: "V2") -> bool:
        return min.x <= self.x < max.x and min.y <= self.y < max.y

    def distance(self, other: "V2") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other: "V2") -> bool:
        return self.x == other.x and self.y == other.y
    
    def __mul__(self, other):
        if type(other) == int:
            return V2(self.x*other, self.y*other)
        elif type(other) == V2:
            V2(self.x * other.x, self.y * other.y)
        else:
            return self

    def as_tuple(self) -> tuple[int, int]:
        return self.x, self.y
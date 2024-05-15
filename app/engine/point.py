from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def get_neighbors(self) -> list["Point"]:
        return [
            Point(self.x + 1, self.y),
            Point(self.x - 1, self.y),
            Point(self.x, self.y + 1),
            Point(self.x, self.y - 1),
        ]

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def in_range(self, min: "Point", max: "Point") -> bool:
        return min.x <= self.x < max.x and min.y <= self.y < max.y

    def distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

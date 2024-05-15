from dataclasses import dataclass

from app.engine.point import Point


@dataclass
class Ship:
    position: Point
    hp: int = 100
    current_hp: int = 100
    damage: int = 10
    range: int = 4
    speed: int = 3
    active_moves: int = 3

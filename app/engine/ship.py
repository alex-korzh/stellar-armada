from dataclasses import dataclass

from app.engine.point import Point


@dataclass
class Ship:
    position: Point
    hp: int = 100
    current_hp: int = 100
    damage: int = 10
    range: int = 4
    speed: int = 8
    active_moves: int = speed
    attacks: int = 1
    attacks_left: int = attacks

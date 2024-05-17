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

    def infodump(self):
        return (
            f"HP: {self.current_hp} ({self.hp})"
            f"\nAttacks: {self.attacks_left} ({self.attacks})"
            f"\nMoves: {self.active_moves} ({self.speed})"
            f"\nDamage: {self.damage}"
        )

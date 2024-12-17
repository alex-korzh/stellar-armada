from dataclasses import dataclass

from app.utils.math import V2
from app.engine.weapons import Weapon


@dataclass
class Ship:
    position: V2
    weapons: list[Weapon]
    hp: int = 100
    current_hp: int = 100
    speed: int = 8
    active_moves: int = speed
    selected_weapon: Weapon | None = None

    def __post_init__(self):
        self.selected_weapon = self.weapons[0]

    @property
    def attacks(self) -> int:
        return sum(weapon.attacks for weapon in self.weapons)

    @property
    def attacks_left(self) -> int:
        return sum(weapon.attacks_left for weapon in self.weapons)

    def __weapons_repr(self):
        for weapon in self.weapons:
            if weapon == self.selected_weapon:
                yield f">>{weapon}"
            else:
                yield str(weapon)

    def infodump(self):
        weapons = "\n".join(self.__weapons_repr())
        return (
            f"HP: {self.current_hp} ({self.hp})"
            f"\nAttacks: {self.attacks_left} ({self.attacks})"
            f"\nMoves: {self.active_moves} ({self.speed})"
            f"\nWeapons:\n{weapons}"
        )

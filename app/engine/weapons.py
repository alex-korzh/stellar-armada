from dataclasses import dataclass

from app.utils.constants import (
    LASER_DAMAGE,
    LASER_RANGE,
    MISSILE_AMMO,
    MISSILE_DAMAGE,
    MISSILE_RANGE,
)


# TODO: implement non-circle range for weapons
@dataclass
class Weapon:
    damage: int
    range: int
    attacks: int  # attacks per turn
    attacks_left: int
    ammo: int | None  # None means unlimited ammo
    ammo_left: int | None

    def __str__(self):
        ammo_str = f" ({self.ammo_left}/{self.ammo})" if self.ammo else "Unlimited"
        return (
            f"{self.__class__.__name__}"
            f"\nDamage: {self.damage}"
            f"\nRange: {self.range}"
            f"\nAttacks: {self.attacks_left} ({self.attacks})"
            f"\nAmmo: {ammo_str}"
        )


class Laser(Weapon):
    def __init__(self, damage=LASER_DAMAGE, range=LASER_RANGE):
        super().__init__(
            damage=damage,
            range=range,
            attacks=1,
            attacks_left=1,
            ammo=None,
            ammo_left=None,
        )


class MissileLauncher(Weapon):
    def __init__(self, damage=MISSILE_DAMAGE, range=MISSILE_RANGE, ammo=MISSILE_AMMO):
        super().__init__(
            damage=damage,
            range=range,
            attacks=1,
            attacks_left=1,
            ammo=ammo,
            ammo_left=ammo,
        )

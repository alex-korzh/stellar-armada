from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Player:
    name: str
    color: tuple[int, int, int]
    is_ai: bool = False

    def __str__(self) -> str:
        return self.name

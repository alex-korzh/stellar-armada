from dataclasses import asdict, dataclass
from enum import Enum
import json
from pathlib import Path
# TODO: support TileD format


class TileType(str, Enum):
    SPACE = "S"


@dataclass
class Level:
    tile_size: int
    height: int
    width: int
    starting_zones: list[
        list[tuple[int, int]]
    ]  # example: [[(0, 0), (2, 2)], [(3, 3), (5, 5)]] (topleft, bottomright)

    data: list[list[TileType]]


def generate_simple_level() -> None:
    level = Level(
        tile_size=50,
        height=28,
        width=28,
        starting_zones=[[(0, 0), (27, 2)], [(0, 25), (27, 27)]],
        data=[[TileType.SPACE for _ in range(28)] for _ in range(28)],
    )
    file_path = Path("app", "assets", "levels", "level1.json")
    with open(file_path, "w") as file:
        json.dump(asdict(level), file)


def load_levels() -> list[Level]:
    levels: list[Level] = []
    path = Path("app", "assets", "levels").glob("*.json")
    for file_path in path:
        with open(file_path, "r") as file:
            data = json.load(file)
            lvl = Level(**data)
            levels.append(lvl)
    return levels

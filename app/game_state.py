import logging
from enum import Enum

from app.engine.engine import GameEngine
from app.utils.math import V2
from app.engine.ship import Ship
from app.utils.point_converter import PointConverter


logger = logging.getLogger(__name__)


# temporary, in the future there will be a
# possibility to select a weapon
class SelectionMode(Enum):
    MOVE = "move"
    ATTACK = "attack"


class GameState:
    def __init__(self, engine: GameEngine, point_converter: PointConverter):
        self.engine = engine
        self.point_converter = point_converter
        self.selected_ship: Ship | None = None
        self.selected_ship_destinations: list[V2] | None = None
        self.selected_ship_attack_range: list[V2] | None = None
        self.selection_mode: SelectionMode | None = None

    def switch_selection_mode(self):
        if self.selection_mode == SelectionMode.MOVE:
            self.selection_mode = SelectionMode.ATTACK
        else:
            self.selection_mode = SelectionMode.MOVE

    def try_select_ship(self, point: V2) -> bool:
        ship: Ship | None = self.engine.find_current_player_ship_by_pos(point)
        if ship:
            self.selected_ship = ship
            self.selection_mode = SelectionMode.MOVE
            logger.debug(f"Ship selected: {self.selected_ship}")
            return True

        self.reset_ship_selection()
        return False

    def is_ship_selected(self):
        return self.selected_ship is not None

    def reset_ship_selection(self):
        self.selected_ship = None
        self.selected_ship_destinations = None
        self.selected_ship_attack_range = None
        self.selection_mode = None
        logger.debug("Ship deselected")

    def get_selected_ship_position(self) -> V2:
        return self.selected_ship.position

    def reset_selected_ship_destinations(self, *args) -> None:
        destinations = self.engine.find_all_destinations_by_ship(self.selected_ship)
        self.selected_ship_destinations = [
            d for d in destinations if d != self.selected_ship.position
        ]

    def reset_selected_ship_attack_range(self, *args) -> None:
        attack_range = self.engine.find_attack_range_by_ship(self.selected_ship)
        self.selected_ship_attack_range = [
            d for d in attack_range if d != self.selected_ship.position
        ]

    def get_selected_ship_destinations(self) -> list[V2]:
        if self.selected_ship_destinations is None:
            destinations = self.engine.find_all_destinations_by_ship(self.selected_ship)
            self.selected_ship_destinations = [
                d for d in destinations if d != self.selected_ship.position
            ]
        return self.selected_ship_destinations

    def get_selected_ship_attack_range(self) -> list[V2]:
        if self.selected_ship_attack_range is None:
            attack_range = self.engine.find_attack_range_by_ship(self.selected_ship)
            self.selected_ship_attack_range = [
                d for d in attack_range if d != self.selected_ship.position
            ]
        return self.selected_ship_attack_range

    def get_all_allied_positions(self) -> list[V2]:
        ships = self.engine.get_all_allied_ships()
        return [s.position for s in ships]

    def get_all_enemy_positions(self) -> list[V2]:
        ships = self.engine.get_all_enemy_ships()
        return [s.position for s in ships]

    def get_game_info(self) -> str:
        return f"Turn: {self.engine.turn}\nPlayer: {self.engine.current_player}"

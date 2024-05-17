import logging
from app.engine.engine import GameEngine
from app.engine.point import Point
from app.engine.ship import Ship
from app.utils.point_converter import PointConverter
from app.utils.screen_point import ScreenPoint


logger = logging.getLogger(__name__)


class GameState:
    def __init__(self, engine: GameEngine, point_converter: PointConverter):
        self.engine = engine
        self.point_converter = point_converter
        self.selected_ship: Ship | None = None
        self.selected_ship_destinations: list[ScreenPoint] | None = None
        self.selected_ship_attack_range: list[ScreenPoint] | None = None

    def try_select_ship(self, point: Point) -> bool:
        ship: Ship | None = self.engine.find_current_player_ship_by_pos(point)
        if ship:
            self.selected_ship = ship
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
        logger.debug("Ship deselected")

    def get_selected_ship_position(self) -> ScreenPoint:
        return self.point_converter.from_game_to_screen(
            self.selected_ship.position, center=False
        )

    def reset_selected_ship_destinations(self, *args) -> None:
        destinations = self.engine.find_all_destinations_by_ship(self.selected_ship)
        self.selected_ship_destinations = [
            self.point_converter.from_game_to_screen(d, center=False)
            for d in destinations
            if d != self.selected_ship.position
        ]

    def reset_selected_ship_attack_range(self, *args) -> None:
        attack_range = self.engine.find_attack_range_by_ship(self.selected_ship)
        self.selected_ship_attack_range = [
            self.point_converter.from_game_to_screen(d, center=False)
            for d in attack_range
            if d != self.selected_ship.position
        ]

    def get_selected_ship_destinations(self) -> list[ScreenPoint]:
        if self.selected_ship_destinations is None:
            destinations = self.engine.find_all_destinations_by_ship(self.selected_ship)
            self.selected_ship_destinations = [
                self.point_converter.from_game_to_screen(d, center=False)
                for d in destinations
                if d != self.selected_ship.position
            ]
        return self.selected_ship_destinations

    def get_selected_ship_attack_range(self) -> list[ScreenPoint]:
        if self.selected_ship_attack_range is None:
            attack_range = self.engine.find_attack_range_by_ship(self.selected_ship)
            self.selected_ship_attack_range = [
                self.point_converter.from_game_to_screen(d, center=False)
                for d in attack_range
                if d != self.selected_ship.position
            ]
        return self.selected_ship_attack_range

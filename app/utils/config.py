import logging

from app.utils.constants import CELL_SIZE
from app.utils.screen_point import ScreenPoint

logger = logging.getLogger(__name__)


class ScreenConfig:
    def __init__(self, screen_height: int):
        self.window_width: int = screen_height
        self.window_height: int = int(7 / 8 * screen_height)
        self.game_area_width: int = self.window_height
        self.game_area_height: int = self.window_height
        self.game_area_width_normalized: int = self.game_area_width // CELL_SIZE
        self.game_area_height_normalized: int = self.game_area_height // CELL_SIZE
        self.game_area_x: int = (self.window_width - self.window_height) // 2
        self.game_area_y: int = 0
        self.game_area_x_normalized: int = self.game_area_x // CELL_SIZE
        self.game_area_y_normalized: int = self.game_area_y // CELL_SIZE

        logger.debug(f"Window size: {self.window_width}x{self.window_height}")
        logger.debug(f"Game area size: {self.game_area_width}x{self.game_area_height}")
        logger.debug(f"Game area position: ({self.game_area_x},{self.game_area_y})")
        logger.debug(
            f"Game area normalized position: ({self.game_area_x_normalized},{self.game_area_y_normalized})"
        )
        logger.debug(
            f"Game area normalized size: {self.game_area_width_normalized}x{self.game_area_height_normalized}"
        )

        @property
        def game_area(self) -> ScreenPoint:
            return ScreenPoint(self.game_area_x, self.game_area_y)

        @property
        def game_area_normalized(self) -> ScreenPoint:
            return ScreenPoint(self.game_area_x_normalized, self.game_area_y_normalized)

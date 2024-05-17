import logging

from app.engine.point import Point
from app.utils.config import ScreenConfig
from app.utils.screen_point import ScreenPoint

logger = logging.getLogger(__name__)


class PointConverter:
    def __init__(self, config: ScreenConfig, cell_size: int) -> None:
        self.config = config
        self.cell_size = cell_size

    def from_screen_to_game(self, screen_point: ScreenPoint) -> Point:
        rx = screen_point.x - self.config.game_area_x
        ry = screen_point.y - self.config.game_area_y
        rx = rx // self.cell_size
        ry = ry // self.cell_size
        return Point(rx, ry)

    def from_game_to_screen(
        self, game_point: Point, center: bool = True
    ) -> ScreenPoint:
        x = self.cell_size * game_point.x + self.config.game_area_x
        y = self.cell_size * game_point.y + self.config.game_area_y
        if center:
            x += self.cell_size // 2
            y += self.cell_size // 2

        return ScreenPoint(x, y)

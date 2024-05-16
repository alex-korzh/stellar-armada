from app.engine.point import Point
from app.utils.config import ScreenConfig
from app.utils.constants import CELL_SIZE
from app.utils.screen_point import ScreenPoint


class PointConverter:
    def __init__(
        self, config: ScreenConfig, x_normalized: int, y_normalized: int
    ) -> None:
        self.config = config
        self.x_normalized = x_normalized
        self.y_normalized = y_normalized

    def from_screen_to_game(self, screen_point: ScreenPoint) -> Point:
        # first step: from pixels to tiles
        result = Point(screen_point.x // CELL_SIZE, screen_point.y // CELL_SIZE)
        # second step: adjust for game area
        result.x -= self.x_normalized
        result.y -= self.y_normalized
        return result

    def from_game_to_screen(
        self, game_point: Point, center: bool = True
    ) -> ScreenPoint:
        x = CELL_SIZE * game_point.x + self.config.game_area_x
        y = CELL_SIZE * game_point.y + self.config.game_area_y
        if center:
            x += CELL_SIZE // 2
            y += CELL_SIZE // 2
        return ScreenPoint(x, y)

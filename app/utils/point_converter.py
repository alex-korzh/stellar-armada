import logging

from app.utils.math import V2
from app.utils.config import ScreenConfig

logger = logging.getLogger(__name__)


class PointConverter:
    def __init__(self, config: ScreenConfig, cell_size: int) -> None:
        self.config = config
        self.cell_size = cell_size

    def from_screen_to_game(self, screen_point: V2) -> V2:
        r = screen_point - V2(*self.config.game_area.topleft)
        r //= self.cell_size
        return V2(r.x, r.y)

    def from_game_to_screen(
        self, game_point: V2, center: bool = True
    ) -> V2:
        v = game_point * self.cell_size + V2(*self.config.game_area.topleft)
        if center:
            v.x += self.cell_size // 2
            v.y += self.cell_size // 2

        return v

    @staticmethod
    def from_game_to_minimap(
        x: int, y: int, cell_size: int, game_point: V2
    ) -> V2:
        s_x = cell_size * game_point.x + x + cell_size // 2
        s_y = cell_size * game_point.y + y + cell_size // 2
        return V2(s_x, s_y)

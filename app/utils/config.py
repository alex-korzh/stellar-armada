import logging

from app.utils.constants import SCREEN_RESOLUTIONS


logger = logging.getLogger(__name__)


class ScreenConfig:
    def __init__(self, screen_height: int, screen_width: int):
        for res in reversed(SCREEN_RESOLUTIONS):
            if res[0] <= screen_width and res[1] <= screen_height:
                self.window_width = res[0]
                self.window_height = res[1]
                break

        self.game_area_width: int = self.window_height
        self.game_area_height: int = self.window_height
        self.game_area_x: int = (self.window_width - self.window_height) // 2
        self.game_area_y: int = 0

        logger.debug(f"Screen size: {screen_width}x{screen_height}")
        logger.debug(f"Window size: {self.window_width}x{self.window_height}")
        logger.debug(f"Game area size: {self.game_area_width}x{self.game_area_height}")
        logger.debug(f"Game area position: ({self.game_area_x},{self.game_area_y})")

    def is_in_game_area(self, x: int, y: int) -> bool:
        min_x = self.game_area_x
        min_y = self.game_area_y
        max_x = min_x + self.game_area_width
        max_y = min_y + self.game_area_height
        return min_x <= x <= max_x and min_y <= y <= max_y

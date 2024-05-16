import logging


logger = logging.getLogger(__name__)


class ScreenConfig:
    def __init__(self, screen_height: int):
        self.window_width: int = screen_height
        self.window_height: int = int(7 / 8 * screen_height)
        self.game_area_width: int = self.window_height
        self.game_area_height: int = self.window_height
        self.game_area_x: int = (self.window_width - self.window_height) // 2
        self.game_area_y: int = 0

        logger.debug(f"Window size: {self.window_width}x{self.window_height}")
        logger.debug(f"Game area size: {self.game_area_width}x{self.game_area_height}")
        logger.debug(f"Game area position: ({self.game_area_x},{self.game_area_y})")

import logging

from pygame import Rect, Vector2

from app.utils.constants import SCREEN_RESOLUTIONS


logger = logging.getLogger(__name__)


class ScreenConfig:
    def __init__(self, screen_width: int, screen_height: int):
        for res in reversed(SCREEN_RESOLUTIONS):
            if res[0] <= screen_width and res[1] <= screen_height:
                self.window_size = Vector2(res[0], res[1])
                break
        else:
            raise Exception("Incorrect screen resolution")


        # FIXME doesn't work for vertical display
        self.game_area = Rect(
            (self.window_size.x - self.window_size.y) // 2,
            0,
            self.window_size.y,
            self.window_size.y,
        )

        logger.debug(f"Screen size: {screen_width}x{screen_height}")
        logger.debug(f"Window size: {self.window_size.x}x{self.window_size.y}")
        logger.debug(f"Game area size: {self.game_area.w}x{self.game_area.h}")
        logger.debug(f"Game area position: ({self.game_area.x},{self.game_area.y})")

    def is_in_game_area(self, x: int, y: int) -> bool:
        return self.game_area.collidepoint(x, y)

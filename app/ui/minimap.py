import logging

import pygame
from app.ui.base import UIElement
from app.utils.config import ScreenConfig
from app.utils.constants import WHITE, BLUE
from app.utils.screen_point import ScreenPoint

logger = logging.getLogger(__name__)


class Minimap(UIElement):
    def __init__(
        self,
        offset_x: int,  # in pixels
        offset_y: int,  # in pixels
        screen_config: ScreenConfig,
        level_height: int,  # in pixels
        level_width: int,  # in pixels
        allies: list[ScreenPoint],
        enemies: list[ScreenPoint],
    ):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.allies = allies
        self.enemies = enemies
        self.screen_config = screen_config
        self.level_height = level_height
        self.level_width = level_width
        logger.debug(f"""
        Minimap initialized.
        Offset: ({self.offset_x}, {self.offset_y})
        Level size: {self.level_width}x{self.level_height}""")

    def build(self, rect: pygame.Rect, **kwargs) -> None:
        self.rect = rect
        self.height = rect.height
        self._build_level_rect()
        self._build_camera_rect()
        if self.offset_x is not None:
            self.update(
                offset_x=self.offset_x,
                offset_y=self.offset_y,
                allies=self.allies,
                enemies=self.enemies,
            )

        logger.debug(f"""
        Minimap UI built.
        Rect: {self.rect}
        Level rect: {self.level_rect}
        Camera rect: {self.camera_rect}""")

    def _build_level_rect(self):
        self.width_q = self.level_width / (self.rect.width * 0.9)
        self.height_q = self.level_height / (self.rect.height * 0.9)
        self.level_rect = pygame.Rect(
            0,
            0,
            (self.level_width // self.width_q) + 2,
            (self.level_height // self.height_q) + 2,
        )
        self.level_rect.center = self.rect.center

    def _build_camera_rect(self):
        self.camera_rect = pygame.Rect(
            0,
            0,
            self.screen_config.game_area_width // self.width_q,
            self.screen_config.game_area_height // self.height_q,
        )
        # todo change when starting position will change
        self.camera_rect.topleft = self.level_rect.topleft

    def _update_camera_rect(self):
        self.camera_rect_adjusted = pygame.Rect(self.camera_rect)
        self.camera_rect_adjusted.centerx += self.offset_x // self.width_q
        self.camera_rect_adjusted.centery += self.offset_y // self.height_q
        logger.debug(f"Camera rect updated: {self.camera_rect_adjusted}")

    def update(
        self,
        offset_x: int,
        offset_y: int,
        allies: list[ScreenPoint],
        enemies: list[ScreenPoint],
    ):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.allies = allies
        self.enemies = enemies
        self._update_camera_rect()

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, BLUE, self.camera_rect_adjusted, width=2)
        pygame.draw.rect(screen, WHITE, self.level_rect, width=2)

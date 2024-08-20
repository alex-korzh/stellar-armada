from pathlib import Path
import pygame

from app.engine.point import Point
from app.utils.screen_point import ScreenPoint


class ShipSprite(pygame.sprite.Sprite):
    def __init__(self, point: Point, position: ScreenPoint, direction: str):
        super().__init__()
        img_path = Path("app", "assets", "img", f"fighter_{direction}.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=position.as_tuple)
        self._point = point

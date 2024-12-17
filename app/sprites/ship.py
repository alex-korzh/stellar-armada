from pathlib import Path
import pygame

from app.utils.math import V2


class ShipSprite(pygame.sprite.Sprite):
    def __init__(self, point: V2, position: V2, direction: str):
        super().__init__()
        img_path = Path("app", "assets", "img", f"fighter_{direction}.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=position.as_tuple())
        self._point = point

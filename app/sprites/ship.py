import pygame

from app.utils.screen_point import ScreenPoint


class ShipSprite(pygame.sprite.Sprite):
    def __init__(self, position: ScreenPoint, direction: str):
        super().__init__()
        self.image = pygame.image.load(
            f"app/assets/fighter_{direction}.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=position.as_tuple)

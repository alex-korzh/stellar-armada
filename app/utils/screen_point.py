from dataclasses import dataclass

import pygame


@dataclass
class ScreenPoint:
    x: int
    y: int

    @property
    def as_tuple(self):
        return (self.x, self.y)

    @staticmethod
    def from_screen() -> "ScreenPoint":
        x, y = pygame.mouse.get_pos()
        return ScreenPoint(x, y)

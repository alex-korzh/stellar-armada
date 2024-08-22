from abc import ABC

import pygame


class UIElement(ABC):
    rect: pygame.Rect
    font: pygame.font.Font | None
    height: int

    def draw(self, screen: pygame.Surface):
        raise NotImplementedError

    def build(self, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

from abc import ABC

import pygame


class UIElement(ABC):
    """
    Base class for all UI elements
    use build() to initialize the placement of the element
    """

    rect: pygame.Rect
    font: pygame.font.Font | None
    height: int

    def draw(self, screen: pygame.Surface):
        raise NotImplementedError

    def build(self, **kwargs):
        raise NotImplementedError

    def update(self, **kwargs):
        raise NotImplementedError

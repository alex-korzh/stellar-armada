import pygame
from app.ui.base import UIElement
from app.utils.constants import WHITE


class Label(UIElement):
    def __init__(self, text: str):
        self.text = text

    def build(self, font: pygame.font.Font, rect: pygame.Rect) -> None:
        self.font = font
        self.rect = rect
        self.height = self.font.get_linesize()
        # FIXME: this is the wrong way to do it; height should be passed as part of rect
        self.rect.height = self.height
        if self.text:
            self.update(text=self.text)

    def update(self, **kwargs) -> None:
        """
        kwargs:
            text: str
        """
        self.text = kwargs.get("text", self.text)
        if not self.text:
            return
        self.rendered_text = self.font.render(self.text, True, WHITE)
        self.rendered_text_rect = self.rendered_text.get_rect(topleft=self.rect.topleft)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.rendered_text, self.rendered_text_rect)

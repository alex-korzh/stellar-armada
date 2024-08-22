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
        self.rendered_text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.rendered_text, self.rendered_text_rect)


class VPanel(UIElement):
    def __init__(
        self,
        data: list[UIElement],
    ) -> None:
        self.padding = 2
        self.data = data

    def build(self, font: pygame.font.Font, rect: pygame.Rect) -> None:
        self.rect = rect
        self.font = font
        self.update(data=self.data)

    def update(self, **kwargs) -> None:
        """
        kwargs:
            data: list[UIElement]
        """
        self.data: list[UIElement] = kwargs.get("data", self.data)
        if self.data is None:
            return
        if len(self.data) == 0:
            return
        item_height = self.rect.height // len(self.data)
        while (self.font.get_linesize() > item_height) and (self.font.size > 1):
            self.font = pygame.font.SysFont(
                "jetbrainsmononl", self.base_font_size - 1, bold=True
            )
        shift = 0
        for item in self.data:
            item.build(
                self.font,
                pygame.Rect(
                    self.rect.left + self.padding,
                    self.rect.top + shift,
                    self.rect.width,
                    0,
                ),
            )
            shift += item.height

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, WHITE, self.rect, width=2)
        for item in self.data:
            item.draw(screen)

    def handle_event(self, event: pygame.Event):
        pass

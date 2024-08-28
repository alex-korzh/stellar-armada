import pygame

from app.ui.base import UIElement
from app.utils.constants import WHITE


class VPanel(UIElement):
    def __init__(
        self,
        data: dict[str, UIElement],
    ) -> None:
        self.padding = 2
        self.data = data

    def __getitem__(self, key: str) -> UIElement | None:
        return self.data.get(key)

    def build(self, font: pygame.font.Font, rect: pygame.Rect) -> None:
        self.rect = rect
        self.font = font
        self.update(data=self.data)

    def update(self, data: dict[str, UIElement], **kwargs) -> None:
        """
        kwargs:
            data: dict[str, UIElement]
        """
        self.data.update(data)
        if len(self.data) == 0:
            return
        item_height = self.rect.height // len(self.data)
        while (self.font.get_linesize() > item_height) and (self.font.size > 1):
            self.font = pygame.font.SysFont(
                "jetbrainsmononl", self.base_font_size - 1, bold=True
            )
        shift = 0
        for k, item in self.data.items():
            item.build(
                font=self.font,
                rect=pygame.Rect(
                    self.rect.left + self.padding,
                    self.rect.top + shift,
                    self.rect.width,
                    self.rect.width,
                ),
            )
            shift += item.height

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, WHITE, self.rect, width=2)
        for k, item in self.data.items():
            item.draw(screen)

    def handle_event(self, event: pygame.Event):
        pass

from typing import Callable

import pygame
from app.utils.constants import BLACK, BORDER_WIDTH, WHITE
from pygame import Event, Surface


class Button:
    def __init__(
        self,
        rect: tuple[int, int, int, int],
        callback: Callable,
        text: str,
        id: int,
        font: pygame.Font | None = None,
    ) -> None:
        self.id = id
        self.font = font or pygame.font.SysFont("jetbrainsmononl", 32, bold=True)
        self.rect = pygame.Rect(rect)
        self.callback = callback
        self._text = text
        self.text = self.font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen: Surface):
        hovered = self.is_hovered()
        width = 0 if hovered else BORDER_WIDTH
        self._update_font(hovered)
        pygame.draw.rect(screen, WHITE, self.rect, width=width)
        screen.blit(self.text, self.text_rect)

    def _update_font(self, hovered: bool):
        color = BLACK if hovered else WHITE
        self.text = self.font.render(self._text, True, color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def on_click(self, event: Event):
        if self.is_hovered():
            self.callback()

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

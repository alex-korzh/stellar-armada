from typing import Callable
import pygame
from app.utils.constants import BORDER_WIDTH, WHITE
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
        self.text = self.font.render(text, True, WHITE)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, WHITE, self.rect, width=BORDER_WIDTH)
        screen.blit(self.text, self.text_rect)

    def on_click(self, event: Event):
        if self.rect.collidepoint(event.pos):
            self.callback()

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

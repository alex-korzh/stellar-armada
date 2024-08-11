import pygame
from app.utils.menu_item import MenuItem
from app.ui.button import Button
from app.utils.constants import BORDER_WIDTH, WHITE


class Menu:
    def __init__(self, rect: pygame.Rect, buttons: list[MenuItem]):
        self.padding = 5
        button_height = rect[3] // len(buttons)
        self.rect = pygame.Rect(rect)
        self.buttons: list[Button] = []
        

        button_shift = rect[1] + int(self.padding * 1.5)
        for button in buttons:
            button_rect = (rect[0] + self.padding, button_shift, rect[2] - self.padding * 2, int(button_height - self.padding * 1.5))
            self.buttons.append(
                Button(
                    button_rect,
                    text=button.title,
                    id=button.id,
                    callback=button.callback,
                )
            )
            button_shift += button_rect[3] + int(self.padding)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, WHITE, self.rect, width=BORDER_WIDTH)
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event: pygame.Event):
        for button in self.buttons:
            button.handle_event(event)



import pygame
from pygame.freetype import SysFont

from app.engine import Player
from app.scenes.base import Scene
from app.utils.config import ScreenConfig
from app.utils.constants import BLACK


class GameOver(Scene):
    def __init__(self, screen_config: ScreenConfig, winner: Player):
        super().__init__()
        self.screen_config = screen_config
        self.screen = pygame.display.set_mode(
            (self.screen_config.window_width, self.screen_config.window_height)
        )
        self.font = SysFont("jetbrainsmononl", size=120, bold=True)
        self.winner = winner

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        r = self.font.render_to(
            self.screen,
            (
                self.screen_config.game_area_width // 3,
                self.screen_config.window_height // 4,
            ),
            "Game Over",
            (255, 255, 255),
        )
        self.font.render_to(
            self.screen,
            (
                self.screen_config.game_area_width // 3,
                self.screen_config.window_height // 4 + r.h * 2,
            ),
            f"{self.winner.name} wins!",
            (255, 255, 255),
        )
        self.font.render_to(
            self.screen,
            (
                self.screen_config.game_area_width // 3,
                self.screen_config.window_height // 4 + 4 * r.h,
            ),
            "Press Enter to exit.",
            (255, 255, 255),
        )

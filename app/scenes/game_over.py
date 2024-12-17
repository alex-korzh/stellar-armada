import pygame
from pygame.freetype import SysFont

from app.engine import Player
from app.scenes.base import Scene
from app.utils.config import ScreenConfig
from app.utils.constants import BLACK


class GameOver(Scene):
    def __init__(self, screen_config: ScreenConfig, winner: Player, turns: int):
        super().__init__()
        self.screen_config = screen_config
        self.screen = pygame.display.get_surface()
        self.font = SysFont("jetbrainsmononl", size=120, bold=True)
        self.winner = winner
        self.turns = turns

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        text = f"Game Over!\n{self.winner.name} wins!\nTurns: {self.turns}\nPress Enter to exit."
        x = self.screen_config.game_area.w // 3
        y = self.screen_config.window_size.y // 4
        shift = 0
        for line in text.split("\n"):
            r = self.font.render_to(self.screen, (x, y + shift), line, (255, 255, 255))
            shift += r.h

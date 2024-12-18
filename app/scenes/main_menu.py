import pygame
from app.engine.engine import GameEngine
from app.level.level import Level, load_levels
from app.scenes.base import Scene
from app.scenes.game import GameScene
from app.ui.menu import Menu, MenuItem
from app.utils.config import ScreenConfig
from app.utils.constants import BLACK
from app.utils.math import rect_from_center


class MainMenu(Scene):
    def __init__(self, screen_config: ScreenConfig):
        super().__init__()
        self.screen_config = screen_config
        self.screen = pygame.display.get_surface()
        menu_rect = rect_from_center(
            self.screen_config.window_size // 2,
            pygame.Vector2(300, 400),
        )
        self.menu_items = [
            MenuItem(
                title="New game",
                id=0,
                callback=self.new_game_pressed,
            ),
            MenuItem(
                title="About",
                id=1,
                callback=self.about_pressed,
            ),
            MenuItem(
                title="Quit",
                id=2,
                callback=self.quit_pressed,
            ),
        ]
        self.menu = Menu(menu_rect, self.menu_items)

    def handle_event(self, event: pygame.Event):
        self.menu.handle_event(event)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.menu.draw(self.screen)

    def new_game_pressed(self):
        level: Level = load_levels()[0]
        game = GameEngine(level.width, level.height, level.starting_zones)
        self.next_scene = GameScene(game, self.screen_config, level)

    def about_pressed(self):
        print("About")

    def quit_pressed(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

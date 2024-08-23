import logging

import pygame

from app.scenes.base import Scene

from app.scenes.main_menu import MainMenu
from app.utils.config import ScreenConfig
from app.utils.constants import GAME_NAME

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)


class GameRunner:
    def __init__(self, scene: Scene):
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        self.scene = scene
        self.running = True

        logger.debug("Pygame runner initialized")

    def run(self):
        while self.running:
            # TODO https://stackoverflow.com/questions/60406647/pygame-how-to-write-event-loop-polymorphically # noqa: 501
            # https://github.com/Mekire/pygame-mutiscene-template-with-movie/blob/master/data/tools.py
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.scene.handle_event(event)
            self.scene.update()
            self.scene.draw()
            if self.scene.next_scene:
                self.scene = self.scene.next_scene
            pygame.display.update()
            self.clock.tick(60)


def run_game(debug: bool = True):
    if debug:
        logger.root.setLevel(logging.DEBUG)
    else:
        logger.root.setLevel(logging.INFO)
    pygame.init()

    config: ScreenConfig = ScreenConfig(
        pygame.display.Info().current_h, pygame.display.Info().current_w
    )
    pygame.display.set_mode((config.window_width, config.window_height))
    scene = MainMenu(config)
    runner = GameRunner(scene)
    runner.run()

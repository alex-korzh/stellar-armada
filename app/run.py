import logging

import pygame

from app.level.level import Level, load_levels
from app.scenes.base import Scene
from app.scenes.game import GameScene
from app.utils.config import ScreenConfig
from app.utils.constants import GAME_NAME

from app.engine import GameEngine


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
logger.root.setLevel(logging.DEBUG)


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


def run_game():
    pygame.init()
    level: Level = load_levels()[0]
    config: ScreenConfig = ScreenConfig(pygame.display.Info().current_h)
    game = GameEngine(level.width, level.height, level.starting_zones)
    scene = GameScene(game, config, level)
    runner = GameRunner(scene)
    runner.run()

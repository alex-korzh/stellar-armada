import logging
import sys

import pygame
from app.game_state import GameState

from app.level.level import Level, load_levels
from app.scenes.base import Scene
from app.scenes.game import GameScene
from app.utils.config import ScreenConfig
from app.utils.constants import (
    GREY,
    BLACK,
    LIGHT_GREEN,
    GAME_NAME,
    LIGHT_BLUE,
)
from app.engine import GameEngine, Point, Event
from app.utils.point_converter import PointConverter
from app.sprites.ship import ShipSprite
from app.utils.screen_point import ScreenPoint

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

        logger.debug("Pygame runner initialized")

    def run(self):
        while True:
            # TODO https://stackoverflow.com/questions/60406647/pygame-how-to-write-event-loop-polymorphically # noqa: 501
            # https://github.com/Mekire/pygame-mutiscene-template-with-movie/blob/master/data/tools.py
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.scene.handle_event(
                    event
                )  # possible to make it return a scene to be able to change scenes
            self.scene.update()  # possible to make it return a scene to be able to change scenes
            self.scene.draw()
            pygame.display.update()
            self.clock.tick(60)


def run_game():
    pygame.init()
    level: Level = load_levels()[0]
    config: ScreenConfig = ScreenConfig(pygame.display.Info().current_h)
    screen = pygame.display.set_mode((config.window_width, config.window_height))
    game = GameEngine(level.width, level.height, level.starting_zones)
    scene = GameScene(game, config, level, screen)
    runner = GameRunner(scene)
    runner.run()


if __name__ == "__main__":
    run_game()

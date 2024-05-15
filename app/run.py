import logging
import sys
from dataclasses import dataclass

import pygame
from app.game_state import GameState

from app.utils.config import ScreenConfig
from app.utils.constants import (
    GREY,
    CELL_SIZE,
    BLACK,
    GREEN,
    LIGHT_GREEN,
    GAME_NAME,
    LIGHT_BLUE,
)
from app.engine import GameEngine, Ship, Point, Event
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
    def __init__(self, game: GameEngine, screen_config: ScreenConfig):
        self.screen_config = screen_config
        self.point_converter = PointConverter(screen_config)

        self.screen = pygame.display.set_mode(
            (self.screen_config.window_width, self.screen_config.window_height)
        )
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()

        self.game_engine = game
        self.game_state = GameState(game, self.screen_config)

        self.ship_group = pygame.sprite.Group()
        all_ships = self.game_engine.get_all_ships()
        for ship in all_ships:
            direction = (
                "up"
                if ship.position.y > self.screen_config.game_area_height_normalized / 2
                else "down"
            )
            position = self.point_converter.from_game_to_screen(ship.position)
            self.ship_group.add(ShipSprite(position, direction))

        self.game_engine.subscribe(Event.SHIP_MOVED, self.move_ship_sprite)
        self.game_engine.subscribe(
            Event.SHIP_MOVED, self.game_state.reset_selected_ship_destinations
        )
        self.game_engine.subscribe(
            Event.NEXT_TURN, self.game_state.reset_ship_selection
        )

        logger.debug("Pygame runner initialized")

    def move_ship_sprite(self, from_point: Point, to_point: Point) -> None:
        from_pos = self.point_converter.from_game_to_screen(from_point)
        to_pos = self.point_converter.from_game_to_screen(to_point)
        for sprite in self.ship_group.sprites():
            if sprite.rect.center == from_pos.as_tuple:
                sprite.rect.center = to_pos.as_tuple
                logger.debug("Ship sprite moved successfully")
                return

    def run(self):
        while True:
            # TODO https://stackoverflow.com/questions/60406647/pygame-how-to-write-event-loop-polymorphically # noqa: 501
            # https://github.com/Mekire/pygame-mutiscene-template-with-movie/blob/master/data/tools.py
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_engine.next_turn()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = ScreenPoint.from_screen()

                    if self.game_state.is_ship_selected():
                        mouse_pos_point = self.point_converter.from_screen_to_game(
                            mouse_pos
                        )
                        logger.debug("Trying to move ship")
                        self.game_engine.move_ship(
                            self.game_state.selected_ship, mouse_pos_point
                        )
                    else:
                        self.game_state.try_select_ship(mouse_pos)

            self.screen.fill(BLACK)
            self.draw_grid()
            if self.game_state.is_ship_selected():
                self.draw_selected_cell()
                self.draw_destinations()
                self.draw_hp_bar()
            self.ship_group.draw(self.screen)
            self.ship_group.update()

            pygame.display.update()
            self.clock.tick(60)

    def draw_selected_cell(self):
        selected_cell_pos = self.game_state.get_selected_ship_position()
        pygame.draw.rect(
            self.screen,
            LIGHT_BLUE,
            (
                selected_cell_pos.x,
                selected_cell_pos.y,
                CELL_SIZE,
                CELL_SIZE,
            ),
        )

    def draw_destinations(self):
        destinations = self.game_state.get_selected_ship_destinations()
        for destination in destinations:
            pygame.draw.rect(
                self.screen,
                LIGHT_GREEN,
                (
                    destination.x + 1,
                    destination.y + 1,
                    CELL_SIZE - 1,
                    CELL_SIZE - 1,
                ),
            )

    def draw_hp_bar(self):
        # TODO finish this
        selected_cell_pos = self.game_state.get_selected_ship_position()
        pygame.draw.line(
            self.screen,
            GREEN,
            (selected_cell_pos.x, selected_cell_pos.y),
            (selected_cell_pos.x + CELL_SIZE, selected_cell_pos.y),
            3,
        )

    def draw_grid(self):
        for x in range(
            self.screen_config.game_area_x_normalized,
            self.screen_config.game_area_width_normalized
            + self.screen_config.game_area_x_normalized
            + 1,
        ):
            pygame.draw.line(
                self.screen,
                GREY,
                (x * CELL_SIZE, self.screen_config.game_area_y),
                (
                    x * CELL_SIZE,
                    self.screen_config.game_area_y
                    + self.screen_config.game_area_height,
                ),
            )
        for y in range(
            self.screen_config.game_area_y_normalized,
            self.screen_config.game_area_height_normalized
            + self.screen_config.game_area_y_normalized,
        ):
            pygame.draw.line(
                self.screen,
                GREY,
                (self.screen_config.game_area_x, y * CELL_SIZE),
                (
                    self.screen_config.game_area_x + self.screen_config.game_area_width,
                    y * CELL_SIZE,
                ),
            )


def run_game():
    pygame.init()
    config: ScreenConfig = ScreenConfig(pygame.display.Info().current_h)
    game = GameEngine(
        config.game_area_width_normalized, config.game_area_height_normalized
    )
    runner = GameRunner(game, config)
    runner.run()


if __name__ == "__main__":
    run_game()

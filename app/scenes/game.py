import logging

import pygame
from pygame.freetype import SysFont

from app.engine import Player
from app.engine.engine import Event, GameEngine
from app.engine.point import Point
from app.game_state import GameState, SelectionMode
from app.level.level import Level
from app.scenes.base import Scene
from app.scenes.game_over import GameOver
from app.sprites.ship import ShipSprite
from app.utils.config import ScreenConfig
from app.utils.constants import BLACK, GREY, LIGHT_BLUE, LIGHT_GREEN, LIGHT_RED
from app.utils.point_converter import PointConverter
from app.utils.screen_point import ScreenPoint

logger = logging.getLogger(__name__)


class GameScene(Scene):
    def __init__(
        self,
        game: GameEngine,
        screen_config: ScreenConfig,
        level: Level,
    ):
        super().__init__()
        self.screen_config = screen_config

        self.point_converter = PointConverter(screen_config, level.tile_size)
        self.level = level
        self.screen = pygame.display.set_mode(
            (self.screen_config.window_width, self.screen_config.window_height)
        )
        self.game_engine = game
        self.game_state = GameState(game, self.point_converter)

        self.ship_group = pygame.sprite.Group()
        all_ships = self.game_engine.get_all_ships()
        for ship in all_ships:
            direction = "up" if ship.position.y > self.level.height / 2 else "down"
            position = self.point_converter.from_game_to_screen(ship.position)
            self.ship_group.add(ShipSprite(position, direction))

        self.game_engine.subscribe(Event.SHIP_MOVED, self._move_ship_sprite)
        self.game_engine.subscribe(
            Event.SHIP_MOVED, self.game_state.reset_selected_ship_destinations
        )
        self.game_engine.subscribe(
            Event.SHIP_MOVED, self.game_state.reset_selected_ship_attack_range
        )
        self.game_engine.subscribe(
            Event.NEXT_TURN, self.game_state.reset_ship_selection
        )
        self.game_engine.subscribe(Event.SHIP_DESTROYED, self._remove_ship_sprite)
        self.game_engine.subscribe(Event.GAME_OVER, self.game_over)

        self.font = SysFont("jetbrainsmononl", size=24, bold=True)
        logger.debug("Game scene initialized")

    def game_over(self, player_won: Player):  # temporary
        self.next_scene = GameOver(self.screen_config, player_won)

    def _remove_ship_sprite(self, position: Point) -> None:
        screen_pos = self.point_converter.from_game_to_screen(position)
        for sprite in self.ship_group.sprites():
            if sprite.rect.center == screen_pos.as_tuple:
                self.ship_group.remove(sprite)
                logger.debug("Ship sprite removed successfully")
                return

    def _move_ship_sprite(self, from_point: Point, to_point: Point) -> None:
        from_pos = self.point_converter.from_game_to_screen(from_point)
        to_pos = self.point_converter.from_game_to_screen(to_point)
        for sprite in self.ship_group.sprites():
            if sprite.rect.center == from_pos.as_tuple:
                sprite.rect.center = to_pos.as_tuple
                logger.debug("Ship sprite moved successfully")
                return

    def draw(self):
        self.screen.fill(BLACK)  # instead, draw by tile
        self.draw_grid()

        if self.game_state.is_ship_selected():
            self.draw_text()
            self.draw_selected_cell()
            if self.game_state.selection_mode == SelectionMode.MOVE:
                self.draw_destinations()
            elif self.game_state.selection_mode == SelectionMode.ATTACK:
                self.draw_attack_range()
        self.ship_group.draw(self.screen)
        self.ship_group.update()

    def draw_text(self):
        if not self.game_state.is_ship_selected():
            return
        data = self.game_state.selected_ship.infodump()
        shift = 0
        for i in data.split("\n"):
            text_rect = self.font.render_to(
                self.screen,
                (0, 0 + shift),
                i,
                (255, 255, 255),
            )
            shift += text_rect.h * 1.5
        self.font.render_to(
            self.screen,
            (0, 0 + shift),
            f"Mode: {self.game_state.selection_mode.value}",
            (255, 255, 255),
        )

    def draw_selected_cell(self):
        selected_cell_pos = self.game_state.get_selected_ship_position()
        pygame.draw.rect(
            self.screen,
            LIGHT_BLUE,
            (
                selected_cell_pos.x,
                selected_cell_pos.y,
                self.level.tile_size,
                self.level.tile_size,
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
                    self.level.tile_size - 1,
                    self.level.tile_size - 1,
                ),
            )

    def draw_attack_range(self):
        range_cells: list[ScreenPoint] = (
            self.game_state.get_selected_ship_attack_range()
        )
        for cell in range_cells:
            pygame.draw.rect(
                self.screen,
                LIGHT_RED,
                (
                    cell.x + 1,
                    cell.y + 1,
                    self.level.tile_size - 1,
                    self.level.tile_size - 1,
                ),
            )

    def draw_grid(self):
        for x in range(
            self.screen_config.game_area_x,
            self.screen_config.game_area_x + self.screen_config.game_area_width + 1,
            self.level.tile_size,
        ):
            pygame.draw.line(
                self.screen,
                GREY,
                (x, self.screen_config.game_area_y),
                (
                    x,
                    self.screen_config.game_area_y
                    + self.screen_config.game_area_height,
                ),
            )
        for y in range(
            self.screen_config.game_area_y,
            self.screen_config.game_area_y + self.screen_config.game_area_height,
            self.level.tile_size,
        ):
            pygame.draw.line(
                self.screen,
                GREY,
                (self.screen_config.game_area_x, y),
                (
                    self.screen_config.game_area_x + self.screen_config.game_area_width,
                    y,
                ),
            )

    def update(self):
        pass

    def handle_event(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_SPACE:
                    self.game_engine.next_turn()
                case pygame.K_ESCAPE:
                    self.next_scene = GameOver(
                        self.screen_config, self.game_engine.current_player
                    )
                case pygame.K_a:
                    self.game_state.switch_selection_mode()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = ScreenPoint.from_screen()
            mouse_pos_point = self.point_converter.from_screen_to_game(mouse_pos)

            if (
                mouse_pos_point.x < 0
                or mouse_pos_point.y < 0
                or mouse_pos_point.x > self.level.width
                or mouse_pos_point.y > self.level.height
            ):
                logger.debug(f"Clicked outside of the game area: {mouse_pos_point}")
                return

            if self.game_state.is_ship_selected():
                logger.debug("Ship is selected")
                if self.game_state.selection_mode == SelectionMode.ATTACK:
                    self.game_engine.try_attack_ship(
                        self.game_state.selected_ship, mouse_pos_point
                    )
                elif self.game_state.selection_mode == SelectionMode.MOVE:
                    self.game_engine.move_ship(
                        self.game_state.selected_ship, mouse_pos_point
                    )
            else:
                self.game_state.try_select_ship(mouse_pos_point)

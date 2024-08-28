import logging

import pygame
from pygame.font import SysFont

from app.engine import Player
from app.engine.engine import Event, GameEngine
from app.engine.point import Point
from app.game_state import GameState, SelectionMode
from app.level.level import Level
from app.scenes.base import Scene
from app.scenes.game_over import GameOver
from app.sprites.groups import CameraGroup
from app.sprites.ship import ShipSprite
from app.ui.label import Label
from app.ui.minimap import Minimap
from app.ui.panel import VPanel
from app.utils.config import ScreenConfig
from app.utils.constants import (
    BLACK,
    GREY,
    LIGHT_BLUE,
    LIGHT_GREEN,
    LIGHT_RED,
    CELL_SIZE,
    MINIMAP_ID,
    PLAYER_LABEL_ID,
    TURN_LABEL_ID,
    HP_LABEL_ID,
    MODE_LABEL_ID,
)
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
        self.screen = pygame.display.get_surface()
        self.game_engine = game
        self.game_state = GameState(game, self.point_converter)

        self.ship_group = CameraGroup(screen_config=screen_config)
        all_ships = self.game_engine.get_all_ships()
        for ship in all_ships:
            direction = "up" if ship.position.y > self.level.height / 2 else "down"
            position = self.point_converter.from_game_to_screen(ship.position)
            self.ship_group.add(ShipSprite(ship.position, position, direction))

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
        self.game_engine.subscribe(Event.NEXT_TURN, self.update_left_panel)

        self.game_engine.subscribe(Event.SHIP_DESTROYED, self._remove_ship_sprite)
        self.game_engine.subscribe(Event.GAME_OVER, self.game_over)

        self.font = SysFont("jetbrainsmononl", size=24, bold=True)

        self.offset = Point(0, 0)

        self.left_panel = VPanel(
            {
                MINIMAP_ID: Minimap(
                    self.offset.x,
                    self.offset.y,
                    screen_config,
                    self.level.height * CELL_SIZE,
                    self.level.width * CELL_SIZE,
                    [],
                    [],
                ),
                PLAYER_LABEL_ID: Label(
                    f"Player: {self.game_engine.current_player.name}"
                ),
                TURN_LABEL_ID: Label(f"Turn: {self.game_engine.turn}"),
            },
        )
        self.left_panel.build(
            self.font,
            pygame.Rect(
                0, 0, screen_config.game_area_x - 1, screen_config.window_height
            ),
        )
        self.right_panel = VPanel({})
        self.right_panel.build(
            self.font,
            pygame.Rect(
                screen_config.game_area_x + screen_config.game_area_width,
                0,
                screen_config.game_area_x - 1,
                screen_config.window_height,
            ),
        )

        logger.debug("Game scene initialized")

    def update_left_panel(self):
        self.left_panel.update(
            data={
                PLAYER_LABEL_ID: Label(
                    f"Player: {self.game_engine.current_player.name}"
                ),
                TURN_LABEL_ID: Label(f"Turn: {self.game_engine.turn}"),
            }
        )

    def update_right_panel(self):
        if self.game_state.is_ship_selected():
            ship = self.game_state.selected_ship
            self.right_panel.update(
                data={
                    HP_LABEL_ID: Label(f"HP: {ship.current_hp}/{ship.hp}"),
                    MODE_LABEL_ID: Label(
                        f"Mode: {self.game_state.selection_mode.value}"
                    ),
                }
            )
        else:
            self.right_panel.update(data={})

    def update_minimap(self):
        self.left_panel[MINIMAP_ID].update(
            offset_x=self.offset.x * CELL_SIZE,
            offset_y=self.offset.y * CELL_SIZE,
            allies=[],
            enemies=[],
        )

    def game_over(self, player_won: Player):  # temporary
        self.next_scene = GameOver(
            self.screen_config, player_won, self.game_engine.turn
        )

    def _remove_ship_sprite(self, position: Point) -> None:
        screen_pos = self.point_converter.from_game_to_screen(position)
        for sprite in self.ship_group.sprites():
            if sprite.rect.center == screen_pos.as_tuple:
                self.ship_group.remove(sprite)
                logger.debug("Ship sprite removed successfully")
                return

    def _move_ship_sprite(self, from_point: Point, to_point: Point) -> None:
        from_pos = self.point_converter.from_game_to_screen(from_point - self.offset)
        to_pos = self.point_converter.from_game_to_screen(to_point - self.offset)
        for sprite in self.ship_group.sprites():
            if sprite.rect.center == from_pos.as_tuple:
                sprite.rect.center = to_pos.as_tuple
                sprite._point = to_point
                logger.debug("Ship sprite moved successfully")
                return

    def adjust_ships_for_offset(self):
        for sprite in self.ship_group.sprites():
            new_point: Point = sprite._point - self.offset
            new_pos = self.point_converter.from_game_to_screen(new_point)

            sprite.rect.center = new_pos.as_tuple

    def draw(self):
        self.screen.fill(BLACK)  # instead, draw by tile
        self.draw_grid()  # todo draw on surface on load, then paint to screen every frame

        if self.game_state.is_ship_selected():
            self.draw_selected_cell()
            if self.game_state.selection_mode == SelectionMode.MOVE:
                self.draw_destinations()
            elif self.game_state.selection_mode == SelectionMode.ATTACK:
                self.draw_attack_range()
        self.ship_group.draw(self.screen)
        self.ship_group.update()

        self.left_panel.draw(self.screen)
        self.right_panel.draw(self.screen)

    def draw_cell(
        self,
        color: tuple[int, int, int],
        x: int,
        y: int,
        width_scale: int = 0,
        fill: bool = True,
    ):
        if not self.screen_config.is_in_game_area(x, y):
            return

        width = self.level.tile_size + width_scale
        pygame.draw.rect(
            self.screen, color, (x, y, width, width), width=0 if fill else 1
        )

    def convert_adjust_point_for_offset(self, point: Point) -> ScreenPoint:
        return self.point_converter.from_game_to_screen(
            point - self.offset, center=False
        )

    def draw_selected_cell(self):
        selected_cell_pos = self.convert_adjust_point_for_offset(
            self.game_state.get_selected_ship_position()
        )
        self.draw_cell(LIGHT_BLUE, selected_cell_pos.x, selected_cell_pos.y)

    def draw_destinations(self):
        point_destinations = self.game_state.get_selected_ship_destinations()
        destinations = [
            self.convert_adjust_point_for_offset(p) for p in point_destinations
        ]
        for destination in destinations:
            self.draw_cell(LIGHT_GREEN, destination.x + 1, destination.y + 1, -1)

    def draw_attack_range(self):
        point_range_cells: list[Point] = (
            self.game_state.get_selected_ship_attack_range()
        )
        range_cells = [
            self.convert_adjust_point_for_offset(p) for p in point_range_cells
        ]
        for cell in range_cells:
            self.draw_cell(LIGHT_RED, cell.x + 1, cell.y + 1, -1)

    def draw_grid(self):
        tiles_width = (self.screen_config.game_area_width + 1) // self.level.tile_size
        tiles_height = self.screen_config.game_area_height // self.level.tile_size
        effective_width = min(tiles_width, self.level.width)
        effective_height = min(tiles_height, self.level.height)
        for x in range(effective_width):
            for y in range(effective_height):
                point = self.point_converter.from_game_to_screen(Point(x, y), False)
                self.draw_cell(GREY, point.x, point.y, fill=False)

    def update(self):
        self.update_right_panel()

    def update_offset(self, x: int, y: int):
        if self.offset.x + x < 0 or self.offset.y + y < 0:
            return

        tiles_width = self.screen_config.game_area_width // self.level.tile_size
        tiles_height = self.screen_config.game_area_height // self.level.tile_size
        max_offset_x = self.level.width - tiles_width
        max_offset_y = self.level.height - tiles_height

        if max_offset_x <= 0 or max_offset_y <= 0:
            return

        if self.offset.x + x > max_offset_x or self.offset.y + y > max_offset_y:
            return

        self.offset.x += x
        self.offset.y += y

        self.adjust_ships_for_offset()
        self.update_minimap()
        self.draw()

    def handle_event(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_SPACE:
                    self.game_engine.next_turn()
                case pygame.K_ESCAPE:
                    self.next_scene = GameOver(
                        self.screen_config,
                        self.game_engine.current_player,
                        self.game_engine.turn,
                    )
                case pygame.K_a:
                    self.game_state.switch_selection_mode()
                    self.update_right_panel()
                case pygame.K_LEFT:
                    self.update_offset(-1, 0)

                case pygame.K_RIGHT:
                    self.update_offset(1, 0)
                case pygame.K_UP:
                    self.update_offset(0, -1)
                case pygame.K_DOWN:
                    self.update_offset(0, 1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = ScreenPoint.from_screen()
            mouse_pos_point = (
                self.point_converter.from_screen_to_game(mouse_pos) + self.offset
            )

            if not self.screen_config.is_in_game_area(mouse_pos.x, mouse_pos.y):
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

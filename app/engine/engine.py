import itertools
import logging
import random
from enum import Enum

from app.utils.constants import RED, BLUE
from app.engine.point import Point
from app.engine.player import Player
from app.engine.ship import Ship

logger = logging.getLogger(__name__)


class Event(Enum):
    SHIP_MOVED = 1
    NEXT_TURN = 2


def generate_random_ships(topleft: Point, bottomright: Point) -> list[Ship]:
    ships = []
    limit = 1  # can be randomized later
    for _ in range(limit):
        ships.append(
            Ship(
                position=Point(
                    random.randint(topleft.x, bottomright.x),
                    random.randint(topleft.y, bottomright.y),
                )
            )
        )
    return ships


class GameEngine:
    def __init__(self, width_tiles: int, height_tiles: int):
        self.min_point = Point(0, 0)
        self.max_point = Point(width_tiles, height_tiles)

        self.width = width_tiles
        self.height = height_tiles

        # Specific implementation: randomized ships, 2 players.
        # Will be generalized later.
        self.players = [
            Player("Player 1", RED),
            Player("Player 2", BLUE),
        ]
        # there should be map-specific places to put ships for each player
        starting_zones = self.define_starting_zones()
        logger.debug(f"Starting zones defined: {starting_zones}")
        self.ships = {
            p: generate_random_ships(
                topleft=starting_zones[p][0],
                bottomright=starting_zones[p][1],
            )
            for p in self.players
        }
        logger.debug(f"Ships generated: {self.ships}")

        self.players_cycle = itertools.cycle(self.players)
        self.current_player = next(self.players_cycle)

        self.callbacks = {
            Event.SHIP_MOVED: [],
            Event.NEXT_TURN: [],
        }
        logger.debug("Game engine initialized")

    def next_turn(self) -> None:
        self.current_player = next(self.players_cycle)
        self.reset_ships_by_player(self.current_player)
        for callback in self.callbacks[Event.NEXT_TURN]:
            callback()
        logger.debug(f"It is now {self.current_player.name}'s turn")

    def define_starting_zones(self) -> dict[Player, list[Point]]:
        # only works for 2 players for now
        return {
            self.players[0]: [self.min_point, Point(self.width - 1, 2)],
            self.players[1]: [
                Point(self.min_point.x, self.height - 3),
                Point(self.width - 1, self.height - 1),
            ],
        }

    def get_all_ships(self) -> list[Ship]:
        return [x for v in self.ships.values() for x in v]

    # TODO think: just save ships in dict, keys=coords?
    def find_current_player_ship_by_pos(self, position: Point) -> Ship | None:
        for s in self.ships[self.current_player]:
            if s.position == position:
                logger.debug(f"Found ship at {s.position}")
                return s
        logger.debug(f"No ship found at {position}")
        return None

    def find_all_destinations_by_ship(self, ship: Ship) -> list[Point]:
        if ship not in self.get_all_ships():
            return []
        destinations = [ship.position]
        queue = [ship.position]

        while queue:
            current = queue.pop(0)
            for neighbor in current.get_neighbors():
                if (
                    neighbor not in destinations
                    and neighbor.in_range(self.min_point, self.max_point)
                    and neighbor.distance(ship.position) <= ship.active_moves
                ):
                    destinations.append(neighbor)
                    queue.append(neighbor)
        logger.debug("BFS successful")
        return destinations

    def is_ship_move_possible(self, ship: Ship, destination: Point) -> bool:
        destinations = self.find_all_destinations_by_ship(ship)
        if (
            destination in destinations
            and ship.position.distance(destination) <= ship.active_moves
        ):
            return True
        return False

    def move_ship(self, ship: Ship, destination: Point) -> None:
        from_point = ship.position
        if not self.is_ship_move_possible(ship, destination):
            return
        ship.position = destination
        ship.active_moves -= from_point.distance(destination)
        for callback in self.callbacks[Event.SHIP_MOVED]:
            callback(from_point, destination)
        logger.debug(
            f"Ship moved from {from_point} to {destination}, active moves reduced to {ship.active_moves}, callbacks called"
        )

    def reset_ships_by_player(self, player: Player) -> None:
        for s in self.ships[player]:
            s.active_moves = s.speed

    def subscribe(self, event: Event, callback: callable) -> None:
        self.callbacks[event].append(callback)
        logger.debug(f"Subscribed to {event}: {callback.__name__}")

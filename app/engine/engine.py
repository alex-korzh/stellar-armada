import itertools
import logging
import random
from enum import Enum

from app.engine.weapons import Laser
from app.utils.constants import RED, BLUE
from app.utils.math import V2
from app.engine.player import Player
from app.engine.ship import Ship

logger = logging.getLogger(__name__)


class Event(Enum):
    SHIP_MOVED = 1
    NEXT_TURN = 2
    SHIP_DESTROYED = 3
    GAME_OVER = 4


# TODO proper ship types
def generate_random_ships(
    topleft: V2,
    bottomright: V2,
    limit: int = 1,
) -> list[Ship]:
    ships = []
    for _ in range(limit):
        ships.append(
            Ship(
                position=V2(
                    random.randint(topleft.x, bottomright.x),
                    random.randint(topleft.y, bottomright.y),
                ),
                weapons=[Laser()],
            )
        )
    return ships


class GameEngine:
    def __init__(
        self,
        width_tiles: int,
        height_tiles: int,
        starting_zones: list[list[tuple[int, int]]],
    ):
        self.min_point = V2(0, 0)
        self.max_point = V2(width_tiles, height_tiles)

        self.width = width_tiles
        self.height = height_tiles

        # Specific implementation: randomized ships, 2 players.
        # Will be generalized later.
        self.players = [
            Player("Player 1", RED),
            Player("Player 2", BLUE),
        ]
        # there should be map-specific places to put ships for each player
        prepared_starting_zones = self.prepare_starting_zones(starting_zones)
        logger.debug(f"Starting zones defined: {prepared_starting_zones}")
        self.ships = {
            p: generate_random_ships(
                topleft=prepared_starting_zones[p][0],
                bottomright=prepared_starting_zones[p][1],
            )
            for p in self.players
        }
        logger.debug(f"Ships generated: {self.ships}")

        self.players_cycle = itertools.cycle(self.players)
        self.current_player = next(self.players_cycle)

        self.callbacks = {
            Event.SHIP_MOVED: [],
            Event.NEXT_TURN: [],
            Event.SHIP_DESTROYED: [],
            Event.GAME_OVER: [],
        }
        self.turn = 1
        logger.debug("Game engine initialized")

    def next_turn(self) -> None:
        self.turn += 1
        self.current_player = next(self.players_cycle)
        self.reset_ships_by_player(self.current_player)
        for callback in self.callbacks[Event.NEXT_TURN]:
            callback()
        logger.debug(f"It is now {self.current_player.name}'s turn")

    def prepare_starting_zones(
        self, starting_zones: list[list[tuple[int, int]]]
    ) -> dict[Player, list[V2]]:
        # only works for 2 players for now
        return {
            self.players[i]: [
                V2(starting_zones[i][0][0], starting_zones[i][0][1]),
                V2(starting_zones[i][1][0], starting_zones[i][1][1]),
            ]
            for i in range(2)
        }

    def get_all_ships(self) -> list[Ship]:
        return [x for v in self.ships.values() for x in v]

    def get_all_allied_ships(self) -> list[Ship]:
        # there might be more than one player in an alliance in the future
        return self.ships[self.current_player]

    def get_all_enemy_ships(self) -> list[Ship]:
        return [i for p, s in self.ships.items() for i in s if p != self.current_player]

    def get_player_by_ship(self, ship: Ship) -> Player | None:
        for player, ships in self.ships.items():
            if ship in ships:
                return player
        return None

    def find_current_player_ship_by_pos(self, position: V2) -> Ship | None:
        for s in self.ships[self.current_player]:
            if s.position == position:
                logger.debug(f"Found ship at {s.position}")
                return s
        logger.debug(f"No ship found at {position}")
        return None

    def find_enemy_ship_by_pos(self, position: V2) -> tuple[Ship, Player] | None:
        for player in self.players:
            if player == self.current_player:
                continue
            for s in self.ships[player]:
                if s.position == position:
                    logger.debug(f"Found enemy ship at {s.position}")
                    return s, player
        logger.debug(f"No enemy ship found at {position}")
        return None

    def is_enemy_ship(self, position: V2) -> bool:
        return self.find_enemy_ship_by_pos(position) is not None

    def __bfs(self, position: V2, depth: int) -> list[V2]:
        destinations = [position]
        queue = [position]

        while queue:
            current = queue.pop(0)
            for neighbor in current.get_neighbors():
                if (
                    neighbor not in destinations
                    and neighbor.in_range(self.min_point, self.max_point)
                    and neighbor.distance(position) <= depth
                ):
                    destinations.append(neighbor)
                    queue.append(neighbor)
        logger.debug("BFS successful")
        return destinations

    def find_all_destinations_by_ship(self, ship: Ship) -> list[V2]:
        if ship not in self.get_all_ships():
            return []
        all_dest = self.__bfs(ship.position, ship.active_moves)
        players_to_exclude = [
            p for p in self.ships.keys() if p != self.get_player_by_ship(ship)
        ]
        for player in players_to_exclude:
            for s in self.ships[player]:
                if s.position in all_dest:
                    all_dest.remove(s.position)

        return all_dest

    def find_attack_range_by_ship(self, ship: Ship) -> list[V2]:
        if ship not in self.get_all_ships():
            return []
        return self.__bfs(ship.position, ship.selected_weapon.range)

    def is_ship_move_possible(self, ship: Ship, destination: V2) -> bool:
        destinations = self.find_all_destinations_by_ship(ship)
        if (
            destination in destinations
            and ship.position.distance(destination) <= ship.active_moves
        ):
            return True
        return False

    def move_ship(self, ship: Ship, destination: V2) -> None:
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
            s.selected_weapon.attacks_left = s.selected_weapon.attacks

    def subscribe(self, event: Event, callback: callable) -> None:
        self.callbacks[event].append(callback)
        logger.debug(f"Subscribed to {event}: {callback.__name__}")

    def try_attack_ship(self, attacker: Ship, position: V2) -> None:
        ship_player = self.find_enemy_ship_by_pos(position)
        if not ship_player:
            return
        ship, player = ship_player
        if attacker.attacks_left == 0:
            logger.debug("No attacks left")
            return
        if position.distance(attacker.position) > attacker.selected_weapon.range:
            logger.debug("Attack range exceeded")
            return
        ship.current_hp -= attacker.selected_weapon.damage
        attacker.selected_weapon.attacks_left -= 1
        logger.debug(
            f"Ship attacked at {position}, damage dealt: {attacker.selected_weapon.damage}, current hp: {ship.current_hp}"
        )
        logger.debug(f"Attacks left for attacker ship: {attacker.attacks_left}")
        if ship.current_hp <= 0:
            self.ships[player].remove(ship)
            if self.is_game_over():
                return
            for callback in self.callbacks[Event.SHIP_DESTROYED]:
                callback(position)
            logger.debug(f"Ship destroyed at {position}")

    def is_game_over(self) -> bool:
        all_ships_count = 0
        for p, ships in self.ships.items():
            if p != self.current_player:
                all_ships_count += len(ships)
        if all_ships_count == 0 and len(self.ships[self.current_player]) > 0:
            for callback in self.callbacks[Event.GAME_OVER]:
                callback(self.current_player)
            logger.debug(f"Game over, {self.current_player.name} wins")
            return True
        return False

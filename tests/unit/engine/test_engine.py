import pytest
from app.engine.engine import GameEngine, generate_random_ships
from app.utils.math import V2
from app.engine.ship import Ship


def test_generate_random_ships():
    ships_num = 5
    topleft = V2(0, 0)
    bottomright = V2(7, 7)
    bottomright_limit = V2(8, 8)

    ships = generate_random_ships(topleft, bottomright, ships_num)

    assert len(ships) == ships_num
    assert all([type(ship) == Ship for ship in ships])
    for ship in ships:
        assert ship.position.in_range(topleft, bottomright_limit)


def test_generate_random_ships_wrong_boundaries():
    """
    Topleft should be <= than bottomright
    """

    ships_num = 1
    topleft = V2(5, 5)
    bottomright = V2(3, 3)

    with pytest.raises(ValueError):
        generate_random_ships(topleft, bottomright, ships_num)


def test_gameengine_create():
    w = 3
    h = 3
    starting_zones = [
        [(0, 0), (2, 0)],
        [(0, 2), (2, 2)],
    ]

    engine = GameEngine(w, h, starting_zones)

    assert engine.turn == 1
    assert engine.min_point == V2(*(starting_zones[0][0]))
    assert engine.max_point == V2(w, h)  # ????
    assert len(engine.players) > 1
    assert len(engine.players) == len(engine.ships.keys())

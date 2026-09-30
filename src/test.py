import pytest

import game

gomoku_games = {
    (
        (4, 7), (5, 8),
        (5, 7), (6, 7),
        (6, 8), (7, 6),
        (4, 8), (7, 8),
        (7, 7), (4, 6),
        (6, 9), (5, 6),
        (6, 6), (4, 5),
        (3, 8), (6, 7)
    ): 2
}

def test_board():
    for moves, expected in gomoku_games.items():
        g = game.Game(15, 15, 5)
        actual = g.places(moves)
        if not actual == expected:
            print(moves)
            print(g)
        
        assert actual == expected
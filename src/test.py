import pytest

import game, player

gomoku_games = {
    (
        (4, 7), (5, 8),
        (5, 7), (6, 7),
        (6, 8), (7, 6),
        (4, 8), (7, 8),
        (7, 7), (4, 6),
        (6, 9), (5, 6),
        (6, 6), (4, 5),
        (3, 8), (8, 9)
    ): 2
}

tictacto = {
    (
        (1, 1), (1, 0),
        (0, 0), (2, 2),
        (0, 2), (2, 0),
        (2, 1), (0, 1),
        (1, 2)
    ): 3
}

def test_board():
    for moves, expected in gomoku_games.items():
        g = game.Board(15, 15, 5)
        actual = g.places(moves)
        if not actual == expected:
            print(moves)
            print(g)
        
        assert actual == expected
    
    for moves, expected in tictacto.items():
        g = game.Board(3, 3, 3)
        actual = g.places(moves)
        if not actual == expected:
            print(moves)
            print(g)

        assert actual == expected


def test_lines():
    for moves, expected in gomoku_games.items():
        g = game.Board(15, 15, 5)
        g.places(moves)

        print(f"Lines: {g.placed_lines}")
        player2_lines = g.placed_lines[2]
        player1_lines = g.placed_lines[1]
        assert ((((5, 8), (7, 6)), 3)) in player2_lines
        assert ((((4, 5), (4, 6)), 2)) in player2_lines
        assert ((((4, 7), (5, 7)), 2)) in player1_lines

        g2 = game.Board(15, 15, 5)
        g2.places(((4, 7), (4, 6), (5, 7), (5,6), (7, 7)))
        player2_lines = g2.placed_lines[2]
        player1_lines = g2.placed_lines[1]
        assert ((((4, 7), (5, 7)), 2)) in player1_lines
        assert ((((7, 7), (7, 7)), 1)) in player1_lines
        assert ((((4, 6), (5, 6)), 2)) in player2_lines
        g2.places(((3, 6), (6, 6)))
        assert ((((4, 7), (5, 7)), 2)) in player1_lines
        assert ((((5, 7), (6, 6)), 2)) in player1_lines
        assert ((((6, 6), (7, 7)), 2)) in player1_lines 

def test_cardinality():
    p = player.MonkeyThrowingDarts(1)

    assert p._cardinality((1, 0), (1, 3), 4) == (0, 1)
    assert p._cardinality((1, 0), (1, 1), 2) == (0, 1)
    assert p._cardinality((4, 5), (9, 5), 6) == (1, 0)
    assert p._cardinality((2, 3), (4, 5), 3) == (1, 1)
    assert p._cardinality((3, 2), (2, 3), 2) == (-1, 1)



def test_greedy():
    b = game.Board(15, 15, 5)
    player1 = player.GreedyBot(1)
    player2 = player.GreedyBot(2)
    g = game.Game(b, player1, player2)
    g.run()

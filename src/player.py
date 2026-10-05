from abc import ABC, abstractmethod
from typing import Any
from random import choice

class Player(ABC):
    def __init__(self, player_id : int, strategy_params: dict[str, Any]):
        if player_id not in {1, 2}:
            raise Exception(f"Player id {player_id} invalid! Must be 1 or 2.")
        self.player_id = player_id
        self.strategy_params = strategy_params

    def __str__(self) -> str:
        return self.name
    
    def _cardinality(self, start: tuple[int, int], end: tuple[int, int], line_length: int) -> tuple[int, int]:
        sx, sy = start
        ex, ey = end

        return (ex - sx) // line_length, (ey - sy) // line_length

    @abstractmethod
    def make_move(self, board : list[list[int]]) -> tuple[int, int]:
        pass

class MonkeyThrowingDarts(Player):
    def make_move(self, board: list[list[int]]) -> tuple[int, int]:
        x, y = 0, 0
        while board[x][y] != 0:
            x, y = choice(range(len(board))), choice(range(len(board[0])))
        
        return x, y

class GreedyBot(Player):
    def make_move(self, board: list[list[int]], lines: set[tuple[tuple[tuple[int, int], tuple[int, int]]], int]) -> tuple[int, int]:
        # Example: lines = {(((3, 2), (3, 5)), 3), ...}
        best_lines = list(lines).sort(key = lambda l: l[1], reverse = True)
        
        for (start, end), length in best_lines:
            card_x, card_y = self._cardinality(start, end, length)

            s_x, s_y = start
            e_x, e_y = end

            start_ext_x, start_ext_y = s_x - card_x, s_y - card_y
            end_ext_x, end_ext_y = e_x + card_x, e_y + card_y

            if not board[start_ext_x][start_ext_y]:
                return start_ext_x, start_ext_y
            elif not board[end_ext_x][end_ext_y]:
                return end_ext_x, end_ext_y
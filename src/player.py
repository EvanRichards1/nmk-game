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

    @abstractmethod
    def make_move(self, board : list[list[int]]) -> tuple[int, int]:
        pass

class MonkeyThrowingDarts(Player):
    def make_move(self, board: list[list[int]]) -> tuple[int, int]:
        x, y = 0, 0
        while board[x][y] != 0:
            x, y = choice(range(len(board))), choice(range(len(board[0])))
        
        return x, y
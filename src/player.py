from abc import ABC, abstractmethod
from typing import Any
from random import choice, sample

class Player(ABC):
    def __init__(self, player_id : int, strategy_params: dict[str, Any] = {}):
        if player_id not in {1, 2}:
            raise Exception(f"Player id {player_id} invalid! Must be 1 or 2.")
        self.player_id = player_id
        self.strategy_params = strategy_params

    def __str__(self) -> str:
        return self.name
    
    def _cardinality(self, start: tuple[int, int], end: tuple[int, int], line_length: int) -> tuple[int, int]:
        sx, sy = start
        ex, ey = end
        # (0, 1) (1, 1) -> (1 - 0 / 1, 1 - 1 / 1)

        return (ex - sx) // (line_length - 1), (ey - sy) // (line_length - 1)

    @abstractmethod
    def make_move(self, board : list[list[int]], lines: dict[int, set[tuple[tuple[tuple[int, int], tuple[int, int]]], int]]) -> tuple[int, int]:
        pass

class CommandLinePlayer(Player):
    def make_move(self, board: list[list[int]], lines) -> tuple[int, int]:
        board_pretty = "  "
        board_pretty += " ".join(str(n) for n in range(len(board)))

        for y in range(len(board[0])):
            board_pretty += f"\n{y} " + " ".join([str(board[x][y]) for x in range(len(board))])
        
        print(board_pretty)

        move = tuple(int(n) for n in input("Move (format: x, y): ").split(','))

        return move

class MonkeyThrowingDarts(Player):
    def make_move(self, board: list[list[int]], lines) -> tuple[int, int]:
        x, y = 0, 0
        while board[x][y] != 0:
            x, y = choice(range(len(board))), choice(range(len(board[0])))
        
        return x, y

class GreedyBot(Player):
    def make_move(self, board: list[list[int]], lines: dict[int, set[tuple[tuple[tuple[int, int], tuple[int, int]]], int]]) -> tuple[int, int]:
        board_x = len(board)
        board_y = len(board[0])

        my_lines = lines[self.player_id]

        if not my_lines:
            len_x = len(board) // 2
            len_y = len(board[0]) // 2
            return (len_x, len_y) if not board[len_x][len_y] else (len_x + 1, len_y)
        
        # Example: lines = {(((3, 2), (3, 5)), 3), ...}
        best_lines = sorted(list(my_lines), key = lambda l: l[1], reverse = True)
        
        for (start, end), length in best_lines:
            cards = [self._cardinality(start, end, length)] if length > 1 else sample([(0, 1), (1, 0), (1, 1), (-1, 1)], 4)
            for card_x, card_y in cards:
                s_x, s_y = start
                e_x, e_y = end

                start_ext_x, start_ext_y = s_x - card_x, s_y - card_y
                end_ext_x, end_ext_y = e_x + card_x, e_y + card_y

                if start_ext_x in range(board_x) and start_ext_y in range(board_y) and not board[start_ext_x][start_ext_y]:
                    return start_ext_x, start_ext_y
                elif end_ext_x in range(board_x) and end_ext_y in range(board_y) and not board[end_ext_x][end_ext_y]:
                    return end_ext_x, end_ext_y
        
        return choice(range(board_x)), choice(range(board_y))
from itertools import cycle, product
from collections.abc import Iterable

class Game:
    def __init__(self, board_x: int, board_y: int) -> None:
        self.board_x = board_x
        self.board_y = board_y
        self.board: list[list[int]] = [[0] * board_y for _ in range(board_x)]
        self.players: int = cycle([2, 1])
        self.player: int = 1

    def __str__(self) -> str:
        return '\n'.join(str(row) for row in self.board)

    def __repr__(self) -> str:
        return f"Game({self.board_x}, {self.board_y})"
    
    def _in_bounds(self, x: int, y: int) -> bool:
        return not (
            (x < 0 or x >= self.board_x) or
            (y < 0 or y >= self.board_y)
        )

    def _check_win(self, x: int, y: int, p: int) -> int:
        h_line = [(x + i, y) for i in range(-4, 4 + 1) if self._in_bounds(x + i, y)]
        v_line = [(x, y + i) for i in range(-4, 4 + 1) if self._in_bounds(x, y + i)]
        d1_line = [(x + i, y + i) for i in range(-4, 4 + 1) if self._in_bounds(x + i, y + i)]
        d2_line = [(x - i, y + i) for i in range(-4, 4 + 1) if self._in_bounds(x - i, y + i)]

        for line in (h_line, v_line, d1_line, d2_line):
            accum_stones = 0
            for cx, cy in line:
                if self.board[cx][cy] == p:
                    accum_stones += 1
                else:
                    accum_stones = 0
                
                if accum_stones == 5:
                    print(f"{line=}")
                    return p

    def place(self, x: int, y: int) -> int:
        if self.board[x][y]:
            raise Exception("Cannot place on occupied cell!")
        elif not self._in_bounds(x, y):
            raise Exception(f"{x, y} out of bounds!")
        
        self.board[x][y] = self.player
        win = self._check_win(x, y, self.player)
        self.player = next(self.players)

        return win
    
    def places(self, places: Iterable[tuple[int, int]]) -> int:
        for x, y in places:
            win = self.place(x, y)
            if win:
                return win
        
        return 0
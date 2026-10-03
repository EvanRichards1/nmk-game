from itertools import cycle, product
from collections.abc import Iterable

class Board:
    """
    Represents the state of any "m,n,k-game" where Game(m, n, k) should be equivalent to an "m,n,k-game"
    """
    def __init__(self, board_x: int, board_y: int, winning_length: int, board: list[list[int]] = []) -> None:
        self.winning_length = winning_length
        self.board_x = board_x
        self.board_y = board_y
        self.board: list[list[int]] = [[0] * board_y for _ in range(board_x)] if board else board
        self.players: int = cycle([2, 1])
        self.player: int = 1

    def __str__(self) -> str:
        return '\n'.join(str(row) for row in self.board)

    def __repr__(self) -> str:
        return f"Game({self.board_x}, {self.board_y}, {self.winning_length})"
    
    def _in_bounds(self, x: int, y: int) -> bool:
        return not (
            (x < 0 or x >= self.board_x) or
            (y < 0 or y >= self.board_y)
        )

    def _check_win(self, x: int, y: int, p: int) -> int:
        """
        Check for the win condition by scanning for lines around (x, y) made by player p.
        Returns the player id or 0 for no win.
        e.g. self._check_win(4, 3, 2) -> 2
        """
        lines = [
            [shift(x, y, i) for i in range(-(self.winning_length - 1), self.winning_length) if self._in_bounds(*shift(x, y, i))]
            for shift in (
                lambda x, y, i: (x + i, y),
                lambda x, y, i: (x, y + i),
                lambda x, y, i: (x + i, y + i),
                lambda x, y, i: (x - i, y + i)
            )
        ]

        for line in lines:
            accum_stones = 0
            for cx, cy in line:
                if self.board[cx][cy] == p:
                    accum_stones += 1
                else:
                    accum_stones = 0
                
                if accum_stones == self.winning_length:
                    print(f"{line=}")
                    return p

    def place(self, x: int, y: int) -> int:
        """
        Place a piece for the current player at position (x, y) on the board.
        e.g. self.place(3, 5)
        """
        if self.board[x][y]:
            raise Exception("Cannot place on occupied cell!")
        elif not self._in_bounds(x, y):
            raise Exception(f"{x, y} out of bounds!")
        
        self.board[x][y] = self.player
        win = self._check_win(x, y, self.player)
        self.player = next(self.players)

        return win
    
    def places(self, places: Iterable[tuple[int, int]]) -> int:
        """
        Make multiple placements on the board.
        e.g. self.places(
            (3, 4), (4, 3),
            (5, 6)
        )
        """
        for x, y in places:
            win = self.place(x, y)
            if win:
                return win
        
        return 0

class Player:
    pass

class Game:
    def __init__(self, board: Board, player1: Player, player2: Player) -> None:
        self.board = board
        self.player1 = player1
        self.player2 = player2
    
    def move(self) -> int:
        """
        Request a move from the current player then make it.
        Returns the winner.
        """
        player = self.player1 if self.board.player == 1 else self.player2

        move = player.make_move(self.board.board)
        
        return self.board.place(move)
    
    def run(self) -> int:
        """
        Make moves until a player wins.
        Return the winner.
        """
        winner = 0
        while not winner:
            winner = self.move()

        return winner
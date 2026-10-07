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
        self.board: list[list[int]] = board if board else [[0] * board_y for _ in range(board_x)]
        self.players: int = cycle([2, 1])
        self.player: int = 1
        self.placed_lines: dict[int, set[tuple[tuple[tuple[int, int], tuple[int, int]], int]]] = { 1: set(), 2: set()}

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
                    return p

    def _find_line(self, x: int, y: int, direction: tuple[int, int]) -> tuple[tuple[tuple[int, int], tuple[int, int]], int]:
        player_lines = self.placed_lines[self.player]
        for (start,end), length in player_lines:
            if (x, y) in (start, end) and (x + (length-1)*direction[0], y + (length-1)*direction[1]) in (start,end):
                if direction[0] == -1 or direction[1] == -1:
                    return (((x + (length-1)*direction[0], y+(length-1)*direction[1]), (x, y)), length)
                return (((x, y), (x + (length-1)*direction[0], y+(length-1)*direction[1])), length)

        return None
            


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
        print(f"Player {self.player} placed a move at {(x, y)}")

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        player_lines = self.placed_lines[self.player]
        print(f"Player lines for {self.player}: {player_lines}")
        has_neighbour = False
        for (dx, dy) in directions:
            pos_x, neg_x = x + dx, x - dx
            pos_y, neg_y = y + dy, y - dy
            neg_has_current_player = self._in_bounds(neg_x, neg_y) and self.board[neg_x][neg_y] == self.player
            pos_has_current_player = self._in_bounds(pos_x, pos_y) and self.board[pos_x][pos_y] == self.player
            if neg_has_current_player or pos_has_current_player:
                has_neighbour = True
                print("Neighbour found!")
                print(neg_has_current_player)
                print(pos_has_current_player)
                print(f"{x+dx}, {y+dy}")
                if neg_has_current_player and pos_has_current_player:
                    # Both directions have existing lines. Find line that ends in (x-dx, y-dy) and line that starts with (x+dx, y+dy)
                    # Delete both lines and replace with a new line that starts at the startpoitn of the first line, and ends with the endpoint of the 2nd. Length = line1 length + line2 length + 1
                    left_line = self._find_line(x - dx, y - dy, (-dx, -dy))
                    right_line = self._find_line(x + dx, y + dy, (dx, dy))
                    if left_line is None:
                        left_line = ((((x - dx, y - dy),(x - dx, y - dy))), 1)
                    else:
                        player_lines.remove(left_line)
                    if right_line is None:
                        right_line = ((((x + dx, y + dy),(x + dx, y + dy))), 1)
                    else:
                        player_lines.remove(right_line)

                    (left_start, left_end), left_length = left_line
                    (right_start, right_end), right_length = right_line
                    player_lines.add((((left_start), (right_end)), left_length  + right_length + 1))

                elif neg_has_current_player:
                    # Find line in set that ends in (x-dx, y-dy)
                    # Replace that lines endpoint with (x, y) and length with line.length + 1
                    left_line = self._find_line(x - dx, y - dy, (-dx, -dy))
                    if left_line is None:
                        left_line = ((((x - dx, y - dy),(x - dx, y - dy))), 1)
                    else:
                        player_lines.remove(left_line)

                    (left_start, (left_end_x, left_end_y)), left_length = left_line
                    player_lines.add((((left_start), (left_end_x + dx, left_end_y + dy)), left_length + 1))
                
                elif pos_has_current_player:
                    # Find line that starts with (x+dx, y+dy)
                    # Replace that lines startpoint with (x, y) and length with line.length + 1
                    line = self._find_line(x + dx, y + dy, (dx, dy))
                    if line is None:
                        line = ((((x + dx, y + dy), (x + dx, y + dy))), 1)
                    else:
                        player_lines.remove(line)
                    ((right_start_x, right_start_y), right_end), right_length = line
                    player_lines.add((((right_start_x - dx, right_start_y - dy), right_end), right_length + 1))
                    

                    
        if not has_neighbour:
            player_lines.add((((x, y), (x, y)), 1))

        print(player_lines)


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
        print(f"Places: {places}")
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
        
        return self.board.place(*move)
    
    def run(self) -> int:
        """
        Make moves until a player wins.
        Return the winner.
        """
        winner = 0
        while not winner:
            winner = self.move()

        return winner
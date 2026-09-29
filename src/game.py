from itertools import cycle

class Game:
    def __init__(self, board_x: int, board_y: int) -> None:
        self.board_x = board_x
        self.board_y = board_y
        self.board: list[list[int]] = [[0] * board_y for _ in range(board_x)]
        self.players: int = cycle([2, 1])
        self.player: int = 1
        # Each axis has a set of placements which form a line along that axis alongside a length
        self.lines: dict[int, dict[tuple[int, int], list[list[int, set[tuple[int, int]]]]]] = {
            p: {
                (0, 1): [],
                (1, 0): [],
                (1, 1): [],
                (-1, 1): []
            }
            for p in [1, 2]
        }
        self.place_line: dict[int, dict[tuple[int, int], dict[tuple[int, int], int]]] = {
            p: {
                (0, 1): {},
                (1, 0): {},
                (1, 1): {},
                (-1, 1): {}
            }
            for p in [1, 2]
        }

    def __str__(self) -> str:
        return '\n'.join(str(row) for row in self.board)

    def __repr__(self) -> str:
        return f"Game({self.board_x}, {self.board_y})"

    def _add_to_line(self, x: int, y: int, p: int) -> int:
        for axis in self.lines[p].keys():
            lines = self.lines[p][axis]
            place_line = self.place_line[p][axis]

            in_line = False

            for mult in [-1, 1]:
                dx, dy = axis
                dx, dy = mult * dx, mult * dy

                if (x + dx, y + dy) in place_line.keys():
                    i = place_line[(x + dx, y + dy)]
                    lines[i][1].add((x, y))
                    lines[i][0] += 1
                    place_line[(x, y)] = i

                    if lines[i][0] >= 5:
                        return p
                    
                    in_line = True
            if not in_line:
                lines.append([1, {(x, y)}])
                place_line[(x, y)] = len(lines) - 1
        
        return 0

    def place(self, x: int, y: int) -> int:
        if not self.board[x][y]:
            self.board[x][y] = self.player
            win = self._add_to_line(x, y, self.player)
            self.player = next(self.players)

            return win
        else:
            raise Exception("Cannot place on occupied cell")
    
    def places(self, places: list[tuple[int, int]]) -> int:
        for x, y in places:
            if self.place(x, y) != 0:
                return self.player
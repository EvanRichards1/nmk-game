from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, player_id : int, name : str):
        if player_id != 1 and player_id != 2:
            raise Exception(f"Player id {player_id} invalid! Must be 1 or 2.")
        self.player_id = player_id
        self.name = name if name else f"Player_{self.player_id}"

    def __str__(self) -> str:
        return self.name

    @abstractmethod
    def make_move(self, board : list[list[int]]) -> tuple[int, int]:
        pass

    




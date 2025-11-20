from abc import ABC, abstractmethod

class Player(ABC):

    @abstractmethod
    def get_move(self) -> str:
        pass

    def observe(self, opponent_move: str):
        pass
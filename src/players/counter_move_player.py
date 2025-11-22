from .player import Player
import random

class CounterMovePlayer(Player):
    # player that plays the move that beats the opponent's last move

    def __init__(self):
        super().__init__()
        self.last_opponent_move = None

    def observe(self, opponent_move: str):
        self.last_opponent_move = opponent_move

    def get_move(self) -> str:
        if self.last_opponent_move == 'R':
            return 'P'
        elif self.last_opponent_move == 'P':
            return 'S'
        elif self.last_opponent_move == 'S':
            return 'R'
        else:
            return random.choice(['R', 'P', 'S'])
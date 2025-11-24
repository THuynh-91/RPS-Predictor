from .player import Player
import random

class RepeaterPlayer(Player):
    # A player that prefers to repeat its last move.
    rep_preference = 0.5 # Probability to repeat last move

    def __init__(self):
        super().__init__()
        self.last_move = None

    def get_move(self) -> str:
        if self.last_move is not None and random.random() < self.rep_preference:
            move = self.last_move
        else:
            move = random.choice(['R', 'P', 'S'])
        
        self.last_move = move
        return move
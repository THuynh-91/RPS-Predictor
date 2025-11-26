from .player import Player
import random

class SlightBiasPlayer(Player):
    # player that has a slight bias towards Rock

    def __init__(self):
        super().__init__()
        self.bias_move = 'R'
        self.other_moves = ['P', 'S']

    def get_move(self) -> str:
        if random.random() < 0.35:
            return self.bias_move
        else:
            return random.choice(self.other_moves)
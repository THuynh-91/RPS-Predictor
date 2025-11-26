from .player import Player
import random

class FizzBuzzPlayer(Player):
    """
    Plays moves based on FizzBuzz pattern 
    """
    
    MOVES = ['R', 'P', 'S']
    
    def __init__(self):
        self.round_num = 0
    
    def get_move(self) -> str:
        self.round_num += 1
        
        # Or you can do num % 15 == 0
        if self.round_num % 3 == 0 and self.round_num % 5 == 0:
            return 'S'
        elif self.round_num % 3 == 0:
            return 'R'
        elif self.round_num % 5 == 0:
            return 'P'
        else:
            return random.choice(self.MOVES)
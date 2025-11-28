from .player import Player
from predictors.markov_predictor import MarkovPredictor
import random

class MarkovPlayer(Player):
    """
    A player that uses Markov Chain to predict opponent's next move
    and plays the counter.
    
    This is essentially a "Markov AI Player" that learns patterns.
    """
    
    MOVES = ['R', 'P', 'S']
    
    def __init__(self, order: int = 4):
        self.predictor = MarkovPredictor(order=order)
        self.opponent_history = []
        self.last_move = None
        self.order = order
    
    def get_move(self) -> str:
        move = self.predictor.predict()
        
        self.last_move = move
        return move
    
    def observe(self, opponent_move: str):
        self.opponent_history.append(opponent_move)
        
        # Update the predictor 
        if self.last_move:
            self.predictor.update(opponent_move, self.last_move)
import random
from base_predictor import RPSPredictor

''' 
Random Strategy

Pure Random Selection... no learning
'''

class RandomPredictor(RPSPredictor):
    ''' 
    This should obviously be completely random.
    The expected win rate is 33%.

    Check documentation in 'base_predictor.py'
    '''

    # Needs to implement the core methods.

    def __init__(self):
        pass

    def predict(self):
        pass

    def update(self, player_move: str, ai_move: str) -> None:
        pass

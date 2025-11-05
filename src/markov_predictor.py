import random
from base_predictor import RPSPredictor

'''
Higher Order Markov Chain

Pattern detection using transition probabilities.
Tracks sequences/history of moves to predict the next.
'''

class MarkovPredictor(RPSPredictor):
    '''
    Predicts player's next move using a Markov Chain with order k

    It should track the sequence of moves (move1, move2, ..., movek);
    what does the player usually play next?

    If k = 2, history = [R, P, P, P]
    State = (P, P)
    Transitions[State] = {'R':2, 'P': 15, 'S':3}
    Predict that the player will most likely play P
    AI plays S: (S counters P)
    '''

    # Check documentation before implementing
    def __init__(self, order: int = 3):
        pass

    def predict(self) -> str:
        pass

    def update(self, player_move: str, ai_move: str) -> None:
        pass


import random
from base_predictor import RPSPredictor

'''
Q-Learning Predictor

RL approach using Q-learning algorithm.
Learns optimal strategy through trial and error.

Honestly not sure how it should be implemented or flushed out?
- Meet with professor to further discuss.
'''

class QLearningPredictor(RPSPredictor):
    '''
    Q-Learning RL predictor

    Uses Q-Learning to learn optimal policy:
    - States: Hashed sequence of last k moves
    - Actions: AI's moves ... (R, P, S)
    - Rewards: To be determined.. (+1 for win, -1 for loss, 0 for tie).. maybe?
    - Policy: Epsilon-greedy

    # Needs to be thought out further
    '''

    # More parameters to be added
    # Check 'base_predictor.py' for implementation
    
    def __init__(self):
        pass

    def predict(self) -> str:
        pass

    def update(self, player_move: str, ai_move: str) -> None:
        pass
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
        super().__init__()
        
    # Randomly predicts the player's move and returns the counter    
    def predict(self):
        predicted_player_move = random.choice(self.MOVES)
        return self.counter(predicted_player_move)

    # No need to track history, just update scoreboard
    def update(self, player_move: str, ai_move: str) -> None:
        self._record_round(player_move, ai_move)


if __name__ == "__main__":
    print("TEST:\n")

    predictor = RandomPredictor()

    print('5 Random Moves')
    for i in range(1, 6):
        move = predictor.predict()
        print(f'Move {i}: {move}')
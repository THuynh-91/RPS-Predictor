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
    
    print('5 Random Games:')
    for i in range(1, 6):
        ai_move = predictor.predict()
        player_move = random.choice(['R', 'P', 'S'])
        
        print(f"player_move='{player_move}")
        print(f"ai_move='{ai_move}")
        
        predictor.update(player_move, ai_move)
        
        result = predictor.get_result(player_move, ai_move)
        print(f'Round {i}: Player={player_move}, AI={ai_move} | {result.upper()}\n')
import random
from predictors.base_predictor import RPSPredictor

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
    print("RANDOM TESTING")
    predictor = RandomPredictor()
    stats = predictor.get_stats()
    print("Stats", stats)

    for i in range(100000):
        ai_move = predictor.predict()
        player_move = random.choice(['R', 'P', 'S'])
        predictor.update(player_move, ai_move)

        result = predictor.get_result(player_move, ai_move)
        print(f'Round {i+1}: Player={player_move}, AI={ai_move} | {result.upper()}\n')

    stats = predictor.get_stats()
    print("UPDATED STATS\n",stats)

    #Should be 33% All Around as well. 
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
        super().__init__()
        self.order = order

    def predict(self) -> str:
        # Not enough data - takes a random guess
        if len(self.history) < self.order:
            predicted_player_move = random.choice(self.MOVES)
            return self.counter(predicted_player_move)
        
        # This grabs the last k moves (3) in history
        state = tuple(self.history[-self.order:])

        # Checks if we have seen this state before
        if state not in self.transitions:
            predicted_player_move = random.choice(self.MOVES)
            return self.counter(predicted_player_move)
        
        # Finds the most common next move
        counts = self.transitions[state]
        total = sum(counts.values())

        if total == 0:
            predicted_player_move = random.choice(self.MOVES)
            return self.counter(predicted_player_move)
        
        # Predict most likely player move
        predicted_player_move = max(counts, key = counts.get)

        return self.counter(predicted_player_move)

    def update(self, player_move: str, ai_move: str) -> None:
        pass


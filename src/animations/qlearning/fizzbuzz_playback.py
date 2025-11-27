from qlearning_anim import RPSQLearningPlayback

class FizzBuzzPlayback(RPSQLearningPlayback):
    def __init__(self, **kwargs):
        super().__init__(predictor="qlearning", opponent="fizzbuzz", **kwargs)
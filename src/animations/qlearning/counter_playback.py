from qlearning_anim import RPSQLearningPlayback

class CounterPlayback(RPSQLearningPlayback):
    def __init__(self, **kwargs):
        super().__init__(predictor="qlearning", opponent="counter", **kwargs)
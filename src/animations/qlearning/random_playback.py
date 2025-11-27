from qlearning_anim import RPSQLearningPlayback

class RandomPlayback(RPSQLearningPlayback):
    def __init__(self, **kwargs):
        super().__init__(predictor="qlearning", opponent="random", **kwargs)

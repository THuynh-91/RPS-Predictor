from qlearning_anim import RPSQLearningPlayback

class SlightBiasPlayback(RPSQLearningPlayback):
    def __init__(self, **kwargs):
        super().__init__(predictor="qlearning", opponent="slightbias", **kwargs)
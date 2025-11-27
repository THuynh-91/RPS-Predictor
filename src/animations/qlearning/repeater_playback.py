from qlearning_anim import RPSQLearningPlayback

class RepeaterPlayback(RPSQLearningPlayback):
    def __init__(self, **kwargs):
        super().__init__(predictor="qlearning", opponent="repeater", **kwargs)
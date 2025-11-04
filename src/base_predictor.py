from abc import ABC, abstractmethod

'''
RPSPredictor class interface

class vars:
    MOVES: List[str] 
        - All possible moves (R,P,S)

    COUNTERS: Dict[str, str] 
        - The Counter for each move (The winning move)

instance vars:
    history: List[str] 
        - List of Player's past moves in order
    wins: int
        - Num of rounds AI won
    losses: int
        - Num of rounds AI lost
    ties: int
        - Num of rounds that ended in a tie

abstract methods:
    predict() -> str
        - Use the strategy to predict the player's next move, then return the AI move that beats it.
            1. predicted_move = Predict player's next move through strategy (implemented differently depending on strategy)
            2. ai_move = counter(predicted_move)
            3. return ai_move

    update(player_move: str, ai_move: str) -> None
        - Update the predictor after a round.
        1. Add player's move to history
        2. Update scoreboard statistics
        3. Update the strategy (learn)

concrete methods:
    counter(move: str) -> str
        - Returns the move that beats the given move.
        If P, return S because scissors beats paper

    get_result(player: str, ai: str) -> str
        - Returns who won the round from the AI's perspective
            - 'win', 'lose', or 'tie'

    get_stats() -> Dict
        - Returns current metrics
            Dict: {wins: , losses:, ties:, total_games:, win_rate:,}

    reset() -> None
        - Resets predictor to initial
        - Clears history and all statistics
'''

class RPSPredictor(ABC):
    MOVES = ['R', 'P', 'S']
    COUNTERS = {'R':'P', 'P':'S', 'S':'R'}

    def __init__(self):
        self.history = []
        self.wins = 0
        self.losses = 0
        self.ties = 0

    @abstractmethod
    def predict(self) -> str:

        pass
from abc import ABC, abstractmethod

'''
RPSPredictor class interface

class vars:
    MOVES: list[str] 
        - All possible moves (R,P,S)

    COUNTERS: dict[str, str] 
        - The Counter for each move (The winning move)

instance vars:
    history: list[str] 
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

    get_stats() -> dict
        - Returns current metrics
            dict: {wins: , losses:, ties:, total_games:, win_rate:,}

    reset() -> None
        - Resets predictor to initial
        - Clears history and all statistics
'''

class RPSPredictor(ABC):
    MOVES: tuple[str, str, str] = ('R', 'P', 'S')
    COUNTERS = {'R':'P', 'P':'S', 'S':'R'}

    def __init__(self):
        self.history = []
        self.wins = 0
        self.losses = 0
        self.ties = 0

    @abstractmethod
    def predict(self) -> str:
        '''
        Use the strategy to model the player's next move,
        then return the AI move that beats it.
        '''
        pass

    @abstractmethod
    def update(self, player_move: str, ai_move: str) -> None:
        '''
        Update the predictor after a round.
        1. Add player's move to history
        2. Update scoreboard statistics
        3. Update the strategy (learn)
        '''
        pass

    # --- concrete methods ---
    
    # Returns the move that beats the input (check doc above)
    def counter(self, move: str) -> str:
        if move not in self.COUNTERS:
            raise ValueError(f"Invalid move: {move}. Expected one of {self.MOVES}.")
        
        return self.COUNTERS[move]
    
    # Returns result of the match
    def get_result(self, player_move: str, ai_move: str) -> str:
        if player_move not in self.MOVES or ai_move not in self.MOVES:
            raise ValueError("Moves must be one of 'R','P','S'.")
        
        if player_move == ai_move:
            return 'tie'
        
        # player's move is 'P', AI's move is 'S' ... COUNTERS['P'] = 'S'
        if self.COUNTERS[player_move] == ai_move:
            return 'win'
        return 'lose'
    
    # Return metrics of the matches (check doc for specifics)
    def get_stats(self) -> dict[str, float | int]:
        total = self.wins + self.losses + self.ties
        decisive_games = self.wins + self.losses
        
        # Win rate should be on actual wins vs losses not total games
        if decisive_games > 0:
            ai_win_rate = self.wins / decisive_games
            player_win_rate = self.losses / decisive_games
        else:
            ai_win_rate = 0.0
            player_win_rate = 0.0

        return {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'total_games': total,
            'ai_win_rate': ai_win_rate,
            'ai_win_rate_percent': f"{ai_win_rate * 100:.1f}%",
            'player_win_rate': player_win_rate,  
            'player_win_rate_percent': f"{player_win_rate * 100:.1f}%" 
        }
    
    # Clears history and resets scoreboard
    def reset(self) -> None:
        self.history.clear()
        self.wins = 0
        self.losses = 0
        self.ties = 0

    # --- helpers ---

    # Increment win/loss/tie counter based on result
    def _bump_score(self, result: str) -> None:
        if result == 'win':
            self.wins += 1
        elif result == 'lose':
            self.losses += 1
        else:
            self.ties += 1

    # Appends history and updates scoreboard, helper for update 
    def _record_round(self, player_move: str, ai_move: str) -> None:
        self.history.append(player_move)
        result = self.get_result(player_move, ai_move)
        self._bump_score(result)

    # Returns a readable string representation of the predictor showing W-L-T
    def __repr__(self) -> str:
        stats = self.get_stats()
        return f"{self.__class__.__name__}(games={stats['total_games']}, W-L-T={self.wins}-{self.losses}-{self.ties})"
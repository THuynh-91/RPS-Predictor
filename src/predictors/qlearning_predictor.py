import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import random
import pickle
import glob
import numpy as np
from typing import Dict, Optional, Tuple, Literal
from .base_predictor import RPSPredictor
from players.player import Player



class QLearningPredictor(RPSPredictor):
    MOVE_TO_IDX = {'R': 0, 'P': 1, 'S': 2}
    IDX_TO_MOVE = {0: 'R', 1: 'P', 2: 'S'}
    trained = False

    def __init__(self, alpha: float = None,
                 gamma: float = 0.9,
                 epsilon: float = 1.0,
                 decay_rate: float = 0.99):
        super().__init__()

        self.gamma = gamma
        self.epsilon = epsilon
        self.decay_rate = decay_rate

        # q table: state (tuple of last 3 rounds) -> array of Q-values for each predicted move
        self.q_table: Dict[Optional[Tuple], np.ndarray] = {}

        # track number of updates for adaptive learning rate
        self.n_updates: Dict[Optional[Tuple], np.ndarray] = {}

        self.game_history = []  # list of (opponent_move, ai_move) tuples

        self.prev_state = None
        self.prev_action_idx = None

        self.episodes = 0

        q_table_path = self.find_q_table()
        if q_table_path:
            self.load_q_table(q_table_path)

    def _get_state(self) -> Optional[Tuple]:
        """
        Get current state from last 3 rounds of play.
        Returns tuple of last 3 (opponent_move, ai_move) pairs, or None if < 3 rounds.
        """
        if len(self.game_history) < 3:
            return None

        return tuple(self.game_history[-3:])

    def predict(self) -> str:
        """
        Predict opponent's next move and return the counter.
        Uses epsilon-greedy selection.
        """
        state = self._get_state()

        # initialize q values for new state
        if state not in self.q_table:
            self.q_table[state] = np.zeros(3)
            self.n_updates[state] = np.zeros(3)

        if random.random() < self.epsilon:
            predicted_idx = random.randint(0, 2)
        else:
            predicted_idx = np.argmax(self.q_table[state])

        predicted_player_move = self.IDX_TO_MOVE[predicted_idx]
        self.prev_state = state
        self.prev_action_idx = predicted_idx

        # return counter move
        ai_move = self.counter(predicted_player_move)

        return ai_move

    def update(self, opponent_move: str, ai_move: str):
        """
        Update Q-table after observing opponent's actual move.
        Uses adaptive learning rate: eta = 1/(1 + N(s,a))
        """
        self.game_history.append((opponent_move, ai_move))

        if self.prev_action_idx is None:
            return

        predicted_move = self.IDX_TO_MOVE[self.prev_action_idx]
        reward = 0
        if predicted_move == opponent_move:
            reward = 1  # correct
        elif self.counter(predicted_move) == opponent_move:
            reward = 0  # neutral
        else:
            reward = -1  # incorrect

        new_state = self._get_state()

        if new_state not in self.q_table:
            self.q_table[new_state] = np.zeros(3)
            self.n_updates[new_state] = np.zeros(3)

        # adaptive learning
        eta = 1.0 / (1.0 + self.n_updates[self.prev_state][self.prev_action_idx])
        self.n_updates[self.prev_state][self.prev_action_idx] += 1

        # update q table
        old_q = self.q_table[self.prev_state][self.prev_action_idx]
        best_future_q = np.max(self.q_table[new_state])
        new_q = (1 - eta) * old_q + eta * (reward + self.gamma * best_future_q)
        self.q_table[self.prev_state][self.prev_action_idx] = new_q

        self.prev_action_idx = None

        self.episodes += 1

        self.epsilon *= self.decay_rate

    def train_against(self, opponent: Player, episodes: int, msgs=True):
        """
        Train the Q-learner by playing against an opponent.
        """
        if self.trained:
            return

        if msgs:
            print(f"[TRAIN] Training for {episodes} episodes...")
            print(f"[TRAIN] Initial epsilon: {self.epsilon:.4f}")

        wins = 0
        losses = 0
        ties = 0

        for ep in range(episodes):
            ai_move = self.predict()
            opp_move = opponent.get_move()

            # track results
            result = self.get_result(opp_move, ai_move)
            if result == "win":
                wins += 1
            elif result == "lose":
                losses += 1
            else:
                ties += 1

            opponent.observe(ai_move)
            self.update(opp_move, ai_move)

        self.trained = True
        self.save_q_table()

    def _filename(self):
        return f"Q_RPS_ep{self.episodes}_g{self.gamma}_d{self.decay_rate}.pickle"

    def _glob_pattern(self):
        return f"Q_RPS_ep*_g{self.gamma}_d{self.decay_rate}.pickle"

    def save_q_table(self):
        data = {
            "Q": {k: v.tolist() for k, v in self.q_table.items()},
            "N": {k: v.tolist() for k, v in self.n_updates.items()},
            "episodes": self.episodes,
            "gamma": self.gamma,
            "epsilon": self.epsilon,
            "decay_rate": self.decay_rate,
        }

        try:
            with open(self._filename(), "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(f"Failed to save Q-table: {e}")

    def find_q_table(self) -> str | Literal[False]:
        pattern = self._glob_pattern()
        files = glob.glob(pattern)

        if not files:
            return False

        def extract_ep(name):
            try:
                return int(name.split("_ep")[1].split("_")[0])
            except:
                return 0

        return max(files, key=extract_ep)

    def load_q_table(self, path: str):
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)

            # convert lists back to numpy arrays
            self.q_table = {k: np.array(v) for k, v in data["Q"].items()}
            self.n_updates = {k: np.array(v) for k, v in data["N"].items()}

            self.episodes = data.get("episodes", 0)
            self.epsilon = data.get("epsilon", self.epsilon)

            print(f"Loaded Q-table: {path}")
            print(f"  Episodes trained: {self.episodes}")
            print(f"  Current epsilon: {self.epsilon:.4f}")
            print(f"  States learned: {len(self.q_table)}")
            self.trained = True

        except Exception as e:
            print(f"Failed to load Q-table {path}: {e}")

if __name__ == "__main__":
    # Testing
    pass
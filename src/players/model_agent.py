from .player import Player
import random
from typing import Any, Dict, Optional

class ModelAgent(Player):
    """
    Wraps a model/callable so it can act as a Player.
    The model may be:
      - a callable(my_history, opp_history) -> label or probs
      - an object with predict / predict_proba / update / partial_fit
    """
    def __init__(self, model: Any, deterministic: bool = False, action_space=('R','P','S')):
        super().__init__()
        self.model = model
        self.deterministic = deterministic
        self.action_space = list(action_space)
        self.my_history = []
        self.opp_history = []

    def get_move(self) -> str:
        out = None
        try:
            if callable(self.model):
                out = self.model(self.my_history, self.opp_history)
            elif hasattr(self.model, 'predict_proba'):
                out = self.model.predict_proba(self._feature())
            elif hasattr(self.model, 'predict'):
                out = self.model.predict(self._feature())
            elif hasattr(self.model, 'policy'):
                out = self.model.policy(self.my_history, self.opp_history)
        except Exception:
            out = None

        probs = self._interpret_output(out)
        if probs:
            if self.deterministic:
                return max(probs, key=probs.get)
            choices = list(probs.keys())
            weights = [probs[c] for c in choices]
            s = sum(weights)
            if s <= 0:
                return random.choice(self.action_space)
            weights = [w / s for w in weights]
            return random.choices(choices, weights)[0]

        return random.choice(self.action_space)

    def _interpret_output(self, out: Any) -> Optional[Dict[str, float]]:
        if out is None:
            return None

        if isinstance(out, dict):
            probs = {a: float(out.get(a, 0.0)) for a in self.action_space}
            s = sum(probs.values())
            if s > 0:
                return {k: v / s for k, v in probs.items()}
            return None

        if isinstance(out, str) and out in self.action_space:
            return {out: 1.0}

        try:
            import numpy as _np
            arr = _np.asarray(out)
            if arr.ndim == 1 and arr.size == len(self.action_space):
                probs = {a: float(arr[i]) for i, a in enumerate(self.action_space)}
                s = sum(probs.values())
                if s > 0:
                    return {k: v / s for k, v in probs.items()}
        except Exception:
            pass

        if isinstance(out, (list, tuple)) and len(out) == len(self.action_space):
            probs = {a: float(out[i]) for i, a in enumerate(self.action_space)}
            s = sum(probs.values())
            if s > 0:
                return {k: v / s for k, v in probs.items()}

        return None

    def observe(self, opponent_move: Optional[str] = None, my_move: Optional[str] = None):
        """
        Record opponent move (and optionally my move) and update the model.
        Signature matches Player.observe(opponent_move) but also accepts my_move.
        """
        if my_move:
            self.my_history.append(my_move)
        if opponent_move:
            self.opp_history.append(opponent_move)

        try:
            if hasattr(self.model, 'partial_fit'):
                X, y = self._feature_and_label(my_move, opponent_move)
                if X is not None:
                    self.model.partial_fit(X, y)
            elif hasattr(self.model, 'update'):
                self.model.update(opponent_move, my_move)
        except Exception:
            pass

    def _feature(self):
        return {'my': list(self.my_history), 'opp': list(self.opp_history)}

    def _feature_and_label(self, my_move, opp_move):
        return self._feature(), opp_move

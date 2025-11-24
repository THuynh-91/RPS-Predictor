from players.counter_move_player import CounterMovePlayer
from players.random_player import RandomPlayer
from players.repeater_player import RepeaterPlayer
from predictors.random_predictor import RandomPredictor
from predictors.markov_predictor import MarkovPredictor
from predictors.qlearning_predictor import QLearningPredictor  # if you want it

import pandas as pd

def simulate_predictor_vs_player(predictor_cls, player_cls, num_games=100000, to_csv=None):
    predictor = predictor_cls()
    player = player_cls()
    records = []
    w = l = t = 0

    for i in range(num_games):
        ai_move = predictor.predict()
        p_move = player.get_move()
        result = predictor.get_result(p_move, ai_move)
        if result == "win": w += 1
        elif result == "lose": l += 1
        else: t += 1
        records.append({
            "round": i + 1,
            "model_move": ai_move,
            "player_move": p_move,
            "result": result,
            "cum_model_wins": w,
            "cum_player_wins": l,
            "cum_ties": t,
        })
        predictor.update(p_move, ai_move)
        if hasattr(player, "observe"): player.observe(ai_move)

    df = pd.DataFrame.from_records(records)
    if to_csv: df.to_csv(to_csv, index=False)
    return df

if __name__ == "__main__":
    predictors = {
        "random": RandomPredictor,
        "markov": lambda: MarkovPredictor(order=3),
    }
    players = {
        "random": RandomPlayer,
        "repeater": RepeaterPlayer,
        "counter": CounterMovePlayer,
    }

    for p_name, p_ctor in predictors.items():
        for pl_name, pl_ctor in players.items():
            fname = f"results_{p_name}_vs_{pl_name}.csv"
            print(f"{p_name} vs {pl_name}")
            df = simulate_predictor_vs_player(p_ctor, pl_ctor, num_games=100000, to_csv=fname)
            last = df.iloc[-1]
            print(f"  Model wins: {last['cum_model_wins']} | Player wins: {last['cum_player_wins']} | Ties: {last['cum_ties']}")
            print(f"  Saved to {fname}\n")
    print("All CSVs generated successfully!")
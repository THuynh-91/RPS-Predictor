from players.counter_move_player import CounterMovePlayer
from players.model_agent import ModelAgent
from players.random_player import RandomPlayer
from players.markov_player import MarkovPlayer
from players.repeater_player import RepeaterPlayer
from players.fizzbuzz_player import FizzBuzzPlayer
from players.slight_bias_player import SlightBiasPlayer
from predictors.random_predictor import RandomPredictor
from predictors.markov_predictor import MarkovPredictor
from predictors.qlearning_predictor import QLearningPredictor  

import pandas as pd
import os

def simulate_predictor_vs_player(predictor_cls, player_cls, num_games=100000, to_csv=None):
    predictor = predictor_cls() if callable(predictor_cls) else predictor_cls
    player = player_cls()
    
    def reverse_counter(ai_move):
        reverse = {'R': 'S', 'P': 'R', 'S': 'P'}
        return reverse.get(ai_move)
    
    records = []
    w = l = t = 0

    for i in range(num_games):
        ai_move = predictor.predict()
        model_prediction = reverse_counter(ai_move) 
        
        p_move = player.get_move()
        result = predictor.get_result(p_move, ai_move)
        
        if result == "win": w += 1
        elif result == "lose": l += 1
        else: t += 1
        
        records.append({
            "round": i + 1,
            "model_move": ai_move,
            "opponent_move": p_move,
            "model_prediction": model_prediction,
            "result": result,
            "cum_model_wins": w,
            "cum_player_wins": l,
            "cum_ties": t,
        })
        
        predictor.update(p_move, ai_move)
        if hasattr(player, "observe"): 
            player.observe(ai_move)

    df = pd.DataFrame.from_records(records)
    if to_csv: 
        os.makedirs(os.path.dirname(to_csv) if os.path.dirname(to_csv) else '.', exist_ok=True)
        df.to_csv(to_csv, index=False)
    return df

if __name__ == "__main__":
    predictors = {
        #"random": RandomPredictor,
        "markov": lambda: MarkovPredictor(order=3),
        #"qlearning": lambda: QLearningPredictor(gamma=0.9, decay_rate=0.999, verbose=False),
    }
    players = {
        #"random": RandomPlayer,
        #"repeater": RepeaterPlayer,
        #"counter": CounterMovePlayer,
        #"fizzbuzz": FizzBuzzPlayer,
        #"slightbias": SlightBiasPlayer
        "markov": lambda: MarkovPlayer(order=3)
    }

    output_dir = "results"  
    os.makedirs(output_dir, exist_ok=True)

    for p_name, p_ctor in predictors.items():
        if p_name == "qlearning":
            model1 = p_ctor()
            model2 = p_ctor()
            for _ in range(10000):
                m1_move = model1.predict()
                m2_move = model2.predict()
                model1.update(m2_move, m1_move)
                model2.update(m1_move, m2_move)
                model1.epsilon = 0.0
                model2.epsilon = 0.0
            
            fname = os.path.join(output_dir, "results_qlearning_vs_qlearning.csv")
            modelPlayer = ModelAgent(model2)
            df = simulate_predictor_vs_player(model1, lambda: modelPlayer, num_games=100000, to_csv=fname)

            last = df.iloc[-1]
            print(f"qlearning vs qlearning")
            print(f"  Model1 wins: {last['cum_model_wins']} | "
                f"Model2 wins: {last['cum_player_wins']} | "
                f"Ties: {last['cum_ties']}")
            print()

        for pl_name, pl_ctor in players.items():
            model = p_ctor()
            if p_name == "qlearning":
                train_stats = model.train_against(pl_ctor(), episodes=10000)
            fname = os.path.join(output_dir, f"results_{p_name}_vs_{pl_name}.csv")
            print(f"{p_name} vs {pl_name}")
            df = simulate_predictor_vs_player(model, pl_ctor, num_games=100000, to_csv=fname)
            if p_name == "qlearning":
                df_train = pd.DataFrame.from_records(train_stats)
                train_fname = os.path.join(output_dir, f"training_{p_name}_vs_{pl_name}.csv")
                df_train.to_csv(train_fname, index=False)
                print(f"  Training stats saved to {train_fname}")
            last = df.iloc[-1]
            print(f"  Model wins: {last['cum_model_wins']} | Player wins: {last['cum_player_wins']} | Ties: {last['cum_ties']}")
            print(f"  Saved to {fname}\n")
    
    print("All CSVs generated successfully!")

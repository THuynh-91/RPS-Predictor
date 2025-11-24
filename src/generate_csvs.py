#!/usr/bin/env python3
"""
Generate CSV results for different model vs player matchups
"""

from simulate import simulate_model_vs_player
from predictors.random_predictor import RandomPredictor
from predictors.markov_predictor import MarkovPredictor
from players.random_player import RandomPlayer
from players.repeater_player import RepeaterPlayer

if __name__ == "__main__":
    print("Generating CSV files for model vs player simulations...\n")

    # Test 1: RandomPredictor vs RandomPlayer
    print("Test 1: RandomPredictor vs RandomPlayer")
    df1 = simulate_model_vs_player(
        RandomPredictor, 
        RandomPlayer, 
        num_games=100000, 
        to_csv='results_random_vs_random.csv'
    )
    last = df1.iloc[-1]
    print(f"  Model wins: {last['cum_model_wins']} | Player wins: {last['cum_player_wins']} | Ties: {last['cum_ties']}")
    print(f"  Saved to results_random_vs_random.csv\n")

    # Test 2: RandomPredictor vs RepeaterPlayer
    print("Test 2: RandomPredictor vs RepeaterPlayer")
    df2 = simulate_model_vs_player(
        RandomPredictor, 
        RepeaterPlayer, 
        num_games=100000, 
        to_csv='results_random_vs_repeater.csv'
    )
    last = df2.iloc[-1]
    print(f"  Model wins: {last['cum_model_wins']} | Player wins: {last['cum_player_wins']} | Ties: {last['cum_ties']}")
    print(f"  Saved to results_random_vs_repeater.csv\n")

    # Test 3: MarkovPredictor vs RandomPlayer
    print("Test 3: MarkovPredictor vs RandomPlayer")
    df3 = simulate_model_vs_player(
        MarkovPredictor, 
        RandomPlayer, 
        num_games=100000, 
        to_csv='results_markov_vs_random.csv'
    )
    last = df3.iloc[-1]
    print(f"  Model wins: {last['cum_model_wins']} | Player wins: {last['cum_player_wins']} | Ties: {last['cum_ties']}")
    print(f"  Saved to results_markov_vs_random.csv\n")

    # Test 4: MarkovPredictor vs RepeaterPlayer
    print("Test 4: MarkovPredictor vs RepeaterPlayer")
    df4 = simulate_model_vs_player(
        MarkovPredictor, 
        RepeaterPlayer, 
        num_games=100000, 
        to_csv='results_markov_vs_repeater.csv'
    )
    last = df4.iloc[-1]
    print(f"  Model wins: {last['cum_model_wins']} | Player wins: {last['cum_player_wins']} | Ties: {last['cum_ties']}")
    print(f"  Saved to results_markov_vs_repeater.csv\n")

    print("✓ All CSVs generated successfully!")

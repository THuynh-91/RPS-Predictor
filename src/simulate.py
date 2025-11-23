import random
import pandas as pd
from players.random_player import RandomPlayer
from predictors.random_predictor import RandomPredictor
from game import RPSGame
from players.model_agent import ModelAgent

def simulate_games(player_class, predictor_class, num_games=100000):
    player = player_class()
    predictor = predictor_class()
    game = RPSGame(player, predictor)

    results = {
        'player_wins': 0,
        'predictor_wins': 0,
        'ties': 0
    }

    for _ in range(num_games):
        result = game.play()
        if result == 'player':
            results['player_wins'] += 1
        elif result == 'predictor':
            results['predictor_wins'] += 1
        else:
            results['ties'] += 1

    return results

def simulate_model_vs_player(model, player, num_games=100000, deterministic=False, to_csv: str = None):
    if isinstance(model, type):
        model = model()
    if isinstance(player, type):
        player = player()

    agent = ModelAgent(model, deterministic=deterministic)

    def round_result(my, opp):
        if my == opp:
            return 'tie'
        beats = {'R': 'S', 'P': 'R', 'S': 'P'}
        return 'win' if beats.get(my) == opp else 'loss'

    records = []
    model_wins = player_wins = ties = 0

    for i in range(num_games):
        m_move = agent.get_move()
        p_move = player.get_move()

        res = round_result(m_move, p_move)
        if res == 'win':
            model_wins += 1
        elif res == 'loss':
            player_wins += 1
        else:
            ties += 1

        records.append({
            'round': i + 1,
            'model_move': m_move,
            'player_move': p_move,
            'result': res,
            'cum_model_wins': model_wins,
            'cum_player_wins': player_wins,
            'cum_ties': ties
        })

        # let agents observe outcomes
        try:
            agent.observe(opponent_move=p_move, my_move=m_move)
        except Exception:
            pass
        try:
            if hasattr(player, 'observe'):
                player.observe(opponent_move=m_move)
        except Exception:
            pass

    df = pd.DataFrame.from_records(records)
    if to_csv:
        df.to_csv(to_csv, index=False)
    return df

if __name__ == "__main__":
    df = simulate_model_vs_player(RandomPredictor, RandomPlayer, num_games=100000, to_csv=None)
    last = df.iloc[-1]
    print(f"Results after {len(df)} games:")
    print(f"Model wins: {last['cum_model_wins']}")
    print(f"Player wins: {last['cum_player_wins']}")
    print(f"Ties: {last['cum_ties']}")
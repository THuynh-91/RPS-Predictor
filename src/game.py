from players.slight_bias_player import SlightBiasPlayer
from players.human_player import HumanPlayer
from predictors.random_predictor import RandomPredictor
from predictors.markov_predictor import MarkovPredictor
from predictors.qlearning_predictor import QLearningPredictor
from players.counter_move_player import CounterMovePlayer

'''
Game Controller

CLI game for testing... (will discuss if we want to make a web and host)
'''

class RPSGame:
    def __init__(self, player, predictor):
        self.player = player
        self.predictor = predictor
        self.round_number = 0

    def play_interactive(self, rounds: int = 0):
        '''
        Main interactive game loop.
        Moves: R, P, S
        STATS: Show statistics
        Q: Quit
        '''

        print("="*50)
        print(" "* (25 - len("GAME START")//2) + "GAME START")
        print("="*50)
        print("\nCommands:")
        print("  R, P, S - Make your move")
        print("  STATS   - Show statistics")
        print("  RESET   - Resets history and stats")
        print("  Q       - Quit game\n")

        while rounds == 0 or self.round_number < rounds:
            # Player Input
            user_input = self.player.get_move()

            if user_input == "Q":
                print("\n" + "="*50)
                print(" "* (25 - len("GAME OVER")//2) + "GAME OVER")
                print("="*50)
                self._show_final_stats()
                break
            
            elif user_input == "STATS":
                self._show_stats()
                # This doesn't count as a round
                continue

            elif user_input == "AUTO":
                # fast-forward: R P S sequence 10 times
                self._auto_play_rps_sequence(cycles=10)
                continue

            elif user_input == "RESET":
                self._reset_game()
                continue

            elif user_input not in ['R', 'P', 'S']:
                print("INVALID INPUT! Use R, P, or S\n")
                continue
            self.round_number += 1
            print(f"Round {self.round_number}: You played {user_input}")

            ai_move = self.predictor.predict()
            self.predictor.update(user_input, ai_move)
            self.player.observe(ai_move)
            self._show_round_result(user_input, ai_move)

    def _show_round_result(self, player_move, ai_move):
        symbols = {
            'R': 'Rock',
            'P': 'Paper',
            'S': 'Scissors'
        }

        result = self.predictor.get_result(player_move, ai_move)

        print(f"\n You: {symbols[player_move]}")
        print(f" AI: {symbols[ai_move]}")

        if result == 'win':
            print(" Result: AI WINS!\n")
        elif result == 'lose':
                print(" Result: YOU WIN!\n")
        else:
            print(" Result: TIE!\n")
            
    def _show_stats(self):
        # Shows current game stats
        stats = self.predictor.get_stats()
        
        print("\n" + "="*50)
        print(" "* (25 - len("CURRENT STATISTICS")//2) + "CURRENT STATISTICS")
        print("="*50)
        print(f" Model:          {self.predictor.__class__.__name__}")
        print(f" Total Games:    {stats['total_games']}")
        print(f" AI Wins:        {stats['wins']}")
        print(f" Your Wins:      {stats['losses']}")
        print(f" Ties:           {stats['ties']}")
        print(f" Your Win Rate:  {stats['player_win_rate_percent']}")
        print("="*50 + "\n")

    def _auto_play_rps_sequence(self, cycles: int = 10):
        """
        Fast-forward demo:
        Plays the sequence R, P, S for `cycles` times,
        updating the predictor each round.
        """
        seq = ['R', 'P', 'S']
        print(f"\n[Auto-play] Playing sequence {' '.join(seq)} x {cycles}...\n")

        for _ in range(cycles):
            for move in seq:
                self.round_number += 1
                print(f"[Auto] Round {self.round_number}: You played {move}")
                ai_move = self.predictor.predict()
                self.predictor.update(move, ai_move)
                self.player.observe(ai_move)
                self._show_round_result(move, ai_move)

        print("\n[Auto-play] Finished R P S sequence.\n")

    def _reset_game(self):
        print("\n[Reset] Clearing game history and model state...\n")

        # Reset round counter
        self.round_number = 0

        if hasattr(self.predictor, "reset"):
            self.predictor.reset()

        print("[Reset] Game and model have been reset. Start playing!\n")


    def _show_final_stats(self):
        # Shows final stats when game ends
        stats = self.predictor.get_stats()
        
        print("\n" + "="*50)
        print(" "* (25 - len("FINAL STATISTICS")//2) + "FINAL STATISTICS")
        print(f"Model: {self.predictor.__class__.__name__}")
        print(f"\nTotal Games Played: {stats['total_games']}")
        print(f"\nFinal Score:")
        print(f" AI:    {stats['wins']} wins")
        print(f" You:   {stats['losses']} wins")
        print(f" Ties:  {stats['ties']}")
        print(f"\n Your Win Rate: {stats['player_win_rate_percent']}")
        print("="*50 + "\n")
        
        # Determine overall winner
        if stats['wins'] > stats['losses']:
            print("\nAI is the overall winner!")
        elif stats['losses'] > stats['wins']:
            print("\nYou are the overall winner!")
        else:
            print("\nIt's a tie overall!")
        
        print("\nThanks for playing!\n")

def main():
    q_alpha = None
    q_gamma = 0.9
    q_epsilon = 1.0
    q_decay = 0.999
    text = "ROCK PAPER SCISSORS PREDICTOR"
    print("-"*50)
    print(" "* (25 - len(text)//2) + text)
    print("-"*50)

    print("\nSelect model:")
    print("1. Random")
    print("2. Markov Chain")
    print("3. Q-Learning")

    choice = input("\nChoice (1-3): ")

    if choice == '1':
        predictor = RandomPredictor()
        print("\nRandom selected successfully!\n")

    elif choice == '2':
        predictor = MarkovPredictor(order = 3)
        print("\nMarkov Chain selected successfully!\n")

    elif choice == '3':
        predictor = QLearningPredictor(q_alpha, q_gamma, q_epsilon, q_decay)
        if not predictor.trained:
            episodes = input("\nHow many training episodes? (Press Enter for 10000): ")
            if not episodes:
                episodes = 10000
            else:
                episodes = int(episodes)
            predictor.train_against(SlightBiasPlayer(), episodes)
        print("\nQ-Learning selected successfully!\n")
    else:
        print("Invalid choice")

    player = HumanPlayer()
    game = RPSGame(player, predictor)
    game.play_interactive(100)



if __name__ == "__main__":
    main()


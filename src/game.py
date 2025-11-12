from random_predictor import RandomPredictor
from markov_predictor import MarkovPredictor
from qlearning_predictor import QLearningPredictor

'''
Game Controller

CLI game for testing... (will discuss if we want to make a web and host)
'''

class RPSGame:
    def __init__(self, predictor):
        self.predictor = predictor
        self.round_number = 0

    def play_interactive(self):
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
        print("  Q       - Quit game\n")

        while True:
            self.round_number += 1
            # Player Input
            user_input = input(f"Round {self.round_number} - Your move: ").upper().strip()

            if user_input == "Q":
                print("\n" + "="*50)
                print(" "* (25 - len("GAME OVER")//2) + "GAME OVER")
                print("="*50)
                self._show_final_stats()
                break
            
            elif user_input == "STATS":
                self._show_stats()
                # This doesn't count as a round
                self.round_number -= 1
                continue

            elif user_input not in ['R', 'P', 'S']:
                print("INVALID INPUT! Use R, P, or S\n")
                self.round_number -= 1
                continue

            ai_move = self.predictor.predict()
            self.predictor.update(user_input, ai_move)
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

    def _show_final_stats(self):
        # Shows final stats when game ends
        stats = self.predictor.get_stats()
        
        print(f"Model: {self.predictor.__class__.__name__}")
        print(f"\nTotal Games Played: {stats['total_games']}")
        print(f"\nFinal Score:")
        print(f" AI:    {stats['wins']} wins")
        print(f" You:   {stats['losses']} wins")
        print(f" Ties:  {stats['ties']}")
        print(f"\n Your Win Rate: {stats['player_win_rate_percent']}")
        
        # Determine overall winner
        if stats['wins'] > stats['losses']:
            print("\nAI is the overall winner!")
        elif stats['losses'] > stats['wins']:
            print("\nYou are the overall winner!")
        else:
            print("\nIt's a tie overall!")
        
        print("\nThanks for playing!\n")

def main():
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
        predictor = QLearningPredictor()
        print("\nQ-Learning selected successfully!\n")
    else:
        print("Invalid choice")

    game = RPSGame(predictor)
    game.play_interactive()



if __name__ == "__main__":
    main()


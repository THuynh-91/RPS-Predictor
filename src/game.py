from random_predictor import RandomPredictor
from markov_predictor import MarkovPredictor
from qlearning_predictor import QLearningPredictor

'''
Game Controller

CLI game for testing... (will discuss if we want to make a web and host)
'''

class RPSGame:
    def __init__(self, predictor):
        pass

    def play_interactive(self):
        '''
        Main interactive game loop.
        Moves: R, P, S
        STATS: Show statistics
        Q: Quit
        '''

        pass

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
    game.play_interactive



if __name__ == "__main__":
    main()


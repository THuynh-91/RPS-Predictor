from players.player import Player
import random

class RandomPlayer(Player):
    # Just plays a random move
    def __init__(self):
        super().__init__()

    def get_move(self) -> str:
        return random.choice(['R', 'P', 'S'])
    
    def observe(self, opponent_move: str):
        pass

if __name__ == "__main__":
    player = RandomPlayer()

    # Test1: Generate 20 random moves
    moves = [player.get_move() for _ in range(20)]
    print(f"Moves: {moves}")
    print()
    # Test2: Check distribution of the moves
    move_counts = {'R': 0, 'P': 0, 'S': 0}

    for _ in range(10000):
        move = player.get_move()
        move_counts[move] += 1

    print("Distribution of random moves:")
    print(f"  R: {move_counts['R']} ({move_counts['R']/10000*100:.1f}%)")
    print(f"  P: {move_counts['P']} ({move_counts['P']/10000*100:.1f}%)")
    print(f"  S: {move_counts['S']} ({move_counts['S']/10000*100:.1f}%)")
    print(f"  Expected: ~33.3% each")




from .player import Player

class HumanPlayer(Player):
    # A player that takes input from a human user.

    def get_move(self) -> str:
        move = ''
        valid_moves = ['R', 'P', 'S']
        while move not in valid_moves:
            move = input("Enter your move (R/P/S): ").strip().upper()
            if move not in valid_moves:
                print("Invalid move. Please enter R, P, or S.")
        print(f"You played: {move}")
        return move
    
    def observe(self, opponent_move: str):
        print(f"Opponent played: {opponent_move}")
from minimax_algorithm import minimax_search

class Player:
    def __init__(self, name, game_piece):
        self.name = name
        self.game_piece = game_piece

    def make_move(self, board):
        raise NotImplementedError("Use subclass.")


class HumanPlayer(Player):
    def make_move(self, board):
        valid_move = False
        while not valid_move:
            try:
                row = int(input("Enter row (0 to {}): ".format(board.n - 1)))
                col = int(input("Enter column (0 to {}): ".format(board.n - 1)))
                valid_move = board.place_game_peice(self.game_piece, row, col)
                if not valid_move:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")


class AIPlayer(Player):
    def make_move(self, board):
        move = minimax_search(board, self.game_piece)
        if move:
            board.place_game_peice(self.game_piece, move[0], move[1])
        else:
            print("No valid moves available.")

    
class Board:
    def __init__(self, n):
        self.n = n
        self.board = self.create_board()

    def create_board(self):
        return [["."] * self.n for _ in range(self.n)]

    def print_board(self):
        for row in self.board:
            print(row)

    def place_game_peice(self, game_peice, row, col):
        if 0 <= row < self.n and 0 <= col < self.n and self.board[row][col] == ".":
            self.board[row][col] = game_peice
            return True
        else:
            return False

    def has_row(self):
        for row in self.board:
            if row.count(row[0]) == self.n and row[0] != ".":
                return True
        return False

    def has_col(self):
        for col in range(self.n):
            if all(self.board[row][col] == self.board[0][col] and self.board[row][col] != "." for row in range(self.n)):
                return True
        return False

    def has_diag(self):
        # Check the main diagonal
        if all(self.board[i][i] == self.board[0][0] and self.board[i][i] != "." for i in range(self.n)):
            return True
        # Check the anti-diagonal
        if all(self.board[i][self.n - 1 - i] == self.board[0][self.n - 1] and self.board[i][self.n - 1 - i] != "." for i in range(self.n)):
            return True
        return False

    def has_square(self):
        # Check for 2x2 squares of the same game piece
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                if (self.board[i][j] == self.board[i][j + 1] == self.board[i + 1][j] == self.board[i + 1][j + 1] 
                    and self.board[i][j] != "."):
                    return True
        return False

    def has_plus(self):
        # Check for 'plus' shape in the middle of the board for 5x5
        # For 4x4, it checks for the plus in the center 2x2 area
        center = self.n // 2
        middle = self.board[center]
        
        # Check if the center piece is not empty
        if self.board[center][center] == ".":
            return False

        # Horizontal line of the plus
        if all(middle[j] == middle[center] for j in range(self.n)):
            # Vertical line of the plus
            if all(self.board[i][center] == self.board[center][center] for i in range(self.n)):
                return True
        return False

    def check_winner(self):
        # Check rows and columns for a win
        for i in range(self.n):
            if self.board[i].count(self.board[i][0]) == self.n and self.board[i][0] != ".":
                return self.board[i][0]  # Row winner
            col = [self.board[row][i] for row in range(self.n)]
            if col.count(col[0]) == self.n and col[0] != ".":
                return col[0]  # Column winner

        # Check main diagonal
        if all(self.board[i][i] == self.board[0][0] != "." for i in range(self.n)):
            return self.board[0][0]

        # Check anti-diagonal
        if all(self.board[i][self.n - 1 - i] == self.board[0][self.n - 1] != "." for i in range(self.n)):
            return self.board[0][self.n - 1]

        # Check for 2x2 square win condition if applicable
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                if self.board[i][j] == self.board[i][j + 1] == self.board[i + 1][j] == self.board[i + 1][j + 1] != ".":
                    return self.board[i][j]  # Square winner

        # Check for plus shape win condition if applicable
        if self.n >= 4 and self.has_plus():
            # Since has_plus doesn't tell us which piece, we need to find the center piece for the plus
            center = self.n // 2
            return self.board[center][center]

        return None  # No winner

    def game_won(self):
        # Uses the has_row, has_col, has_diag, has_square, and has_plus methods to determine if the game is won
        return (self.has_row() or self.has_col() or self.has_diag() or
                (self.n >= 4 and (self.has_square() or self.has_plus())))

class Game:
    def __init__(self, board_size, player_name, player_piece):
        self.board = Board(board_size) 
        ai_piece = 'O' if player_piece == 'X' else 'X'  # Automatically assign the opposite piece to AI
        # Initialize players based on the chosen piece
        if player_piece == 'X':
            self.players = [HumanPlayer(player_name, player_piece), AIPlayer("AI Player", ai_piece)]
        else:
            self.players = [AIPlayer("AI Player", ai_piece), HumanPlayer(player_name, player_piece)]
        self.current_player_index = 0

    def play(self):
        # Main game loop
        while not self.is_game_over():
            current_player = self.players[self.current_player_index]
            # Announce the current player's turn
            if isinstance(current_player, HumanPlayer):
                print(f"{current_player.name}'s turn. Please make your move.")
            else:
                print("AI's turn.")
            # Make the move before printing the board
            self.make_move()
            # Now print the board after the move has been made
            self.board.print_board()
            # Switch to the next player
            self.switch_player()
        # Game is over, print the final outcome
        self.display_winner()

    def make_move(self):
        # Get current player and make a move
        player = self.players[self.current_player_index]
        player.make_move(self.board)

    def switch_player(self):
        # Switch to the other player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def is_game_over(self):
        # Check for a win or draw
        return self.board.game_won()

    def display_winner(self):
        # Display the game outcome
        if self.board.game_won():
            winner = "Player 1" if self.current_player_index == 1 else "AI Player"
            print(f"{winner} wins!")
        else:
            print("It's a draw!")

    # Additional methods for evaluating moves, implementing move ordering,
    # and handling complex win conditions would also be included here.

def start_menu():
    print("Welcome to Tic-Tac-Toe!")

    # Player name input
    player_name = input("Please enter your name: ").strip()
    board_size = int(input("Enter the board size: ").strip())

    # Piece selection
    while True:
        player_piece = input(f"{player_name}, choose your piece (X/O): ").upper()
        if player_piece in ['X', 'O']:
            break
        else:
            print("Invalid selection. Please choose 'X' or 'O'.")

    # Instantiate and start the game
    game = Game(board_size, player_name, player_piece)  # Adjusted to match the Game class definition
    game.play()  # Ensure you have a method to start and manage the game
  

if __name__ == "__main__":
    start_menu()

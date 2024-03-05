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


class Board:
    def __init__(self, n, player_name, game_piece):
        self.n = n
        self.player = HumanPlayer(player_name, game_piece)
        self.computer = "Computer"
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


game_board = Board(3, "Cooper", "X")
game_board.player.make_move(game_board)
game_board.print_board()

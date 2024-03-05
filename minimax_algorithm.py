import copy

def minimax_search(board, player):

    # Determine whether the current player is maximizing or minimizing
    is_maximizing_player = player == 'X'  # Assuming 'X' is the maximizing player
    
    best_score = None
    best_move = None
    
    for move in actions(board):
        new_board = result(board, move, player)
        if is_maximizing_player:
            score = min_value(new_board, 'O')  # Assuming 'O' is the opponent
        else:
            score = max_value(new_board, 'X')
        
        if best_score is None or (is_maximizing_player and score > best_score) or (not is_maximizing_player and score < best_score):
            best_score = score
            best_move = move
    
    return best_move

def max_value(board, player):
    """
    Computes the max value for the Minimax algorithm.
    """
    if is_terminal(board):
        return utility(board, player)
    
    v = float('-inf')
    for move in actions(board):
        v = max(v, min_value(result(board, move, player), 'O'))  # Assuming 'O' is the opponent
    return v

def min_value(board, player):
    """
    Computes the min value for the Minimax algorithm.
    """
    if is_terminal(board):
        return utility(board, player)
    
    v = float('inf')
    for move in actions(board):
        v = min(v, max_value(result(board, move, player), 'X'))  # Assuming 'X' is the opponent
    return v

def is_terminal(board):
    # Game is over if there's a win or no more moves can be made (the board is full)
    return board.game_won() or all(board.board[row][col] != "." for row in range(board.n) for col in range(board.n))

def utility(board, player): 
    winner = board.check_winner()
    if winner == player:
        return 1  # Win for the player
    elif winner is None:
        return 0  # Draw
    else:
        return -1  # Loss for the player

def actions(board):
    return [(row, col) for row in range(board.n) for col in range(board.n) if board.board[row][col] == "."]

def result(board, move, player):
    new_board = copy.deepcopy(board)
    if new_board.place_game_peice(player, move[0], move[1]):
        return new_board
    else:
        raise ValueError("Invalid move applied to board")


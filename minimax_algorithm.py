import copy

def minimax_search(board, ai_piece, opponent_piece):
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for move in ordered_actions(board, ai_piece):
        new_board = result(board, move, ai_piece)
        score = min_value(new_board, ai_piece, alpha, beta)  # Pass AI piece as the player

        if score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha, score)  # Update alpha

    print(f"Best Move: {best_move}, Best Score for AI ({ai_piece}): {best_score}")

    return best_move


def max_value(board, ai_piece, alpha, beta):
    if is_terminal(board):
        return utility(board, ai_piece)

    v = float('-inf')
    for move in actions(board):
        # Simulate the move for the ai_piece
        new_board = result(board, move, ai_piece)
        # call min_value as the opponent's turn to play after ai_piece
        v = max(v, min_value(new_board, ai_piece, alpha, beta))
        if v >= beta:
            break  # Alpha-beta pruning
        alpha = max(alpha, v)
    return v

def min_value(board, opponent_piece, alpha, beta):
    if is_terminal(board):
        return utility(board, opponent_piece)

    v = float('inf')
    for move in actions(board):
        # Simulate the move for the opponent_piece
        new_board = result(board, move, opponent_piece)
        #  call max_value as it's ai_piece's turn to play after opponent_piece
        v = min(v, max_value(new_board, opponent_piece, alpha, beta))
        if v <= alpha:
            break  # Alpha-beta pruning
        beta = min(beta, v)
    return v

def is_terminal(board):
    if board.game_won():
        return True
    if all(board.board[row][col] != "." for row in range(board.n) for col in range(board.n)):
        return True  # The board is full
    return False


def utility(board, player):
    if board.check_winner() == player:
        return 10
    elif board.check_winner():
        return -10  # Opponent wins
    else:
        return 0


def ordered_actions(board, player):
    moves = actions(board)  # Get all possible moves
    scored_moves = [(move, score_move(board, move, player)) for move in moves]
    scored_moves.sort(key=lambda x: x[1], reverse=True)  # Sort moves by score
    return [move for move, _ in scored_moves]


def dynamic_scoring_adjustments(temp_board, score, move, player):
    empty_spaces = sum(row.count('.') for row in temp_board.board)
    late_game_threshold = 5  # Adjust based on board size; fewer spaces indicate late game
    
    if empty_spaces <= late_game_threshold:
        # Increase the weight for blocking moves in the late game
        score *= 1.5
    return score


def opponent_strategy(temp_board, player):
    opponent = 'O' if player == 'X' else 'X'
    strategy_score = 0
    
    # Example: if the opponent seems to favor corners, increase the score for moves that block corner strategies
    corner_moves = [(0, 0), (0, temp_board.n-1), (temp_board.n-1, 0), (temp_board.n-1, temp_board.n-1)]
    opponent_moves = [(row, col) for row in range(temp_board.n) for col in range(temp_board.n) if temp_board.board[row][col] == opponent]
    
    if any(move in corner_moves for move in opponent_moves):
        strategy_score += 20 # scoring to reflect strategic adjustment
    
    return strategy_score


def count_potential_wins(temp_board, player):
    potential_wins = 0
    
    # Check for rows, columns, and diagonals
    if temp_board.has_row() or temp_board.has_col() or temp_board.has_diag():
        potential_wins += 1

        # Check for squares
    if temp_board.has_square():
        potential_wins += 1
    
    # Check for plus shapes
    if temp_board.has_plus():
        potential_wins += 1
    
    return potential_wins


def evaluate_immediacy(temp_board, move, player):
    score = 0
    
    # Increase score based on how many potential wins are immediately available
    immediate_potential_wins = count_potential_wins(temp_board, player)
    score += immediate_potential_wins * 50  # Example scoring, adjust based on your strategy
    
    return score


def score_move(board, move, player):
    temp_board = copy.deepcopy(board)
    opponent = 'O' if player == 'X' else 'X'
    
    # Apply the move
    temp_board.place_game_peice(player, move[0], move[1])
    
    score = 0
    
    # Immediate win check
    if temp_board.game_won():
        score += 1000
    
    # Revert move for further analysis
    temp_board.board[move[0]][move[1]] = "."
    
    # Block opponent's immediate win
    temp_board.place_game_peice(opponent, move[0], move[1])
    if temp_board.game_won():
        score += 500  # Significant score for blocking an immediate win
    temp_board.board[move[0]][move[1]] = "."

    # Multiple end goals and immediacy
    temp_board.place_game_peice(player, move[0], move[1])  # Reapply the original move for further analysis
    score += count_potential_wins(temp_board, player) * 30  # Adjust scoring as needed
    score += evaluate_immediacy(temp_board, move, player)
    score += opponent_strategy(temp_board, player)
    score = dynamic_scoring_adjustments(temp_board, score, move, player)

    print(f"Move: {move}, Score: {score}")

    return score


def actions(board):
    return [(row, col) for row in range(board.n) for col in range(board.n) if board.board[row][col] == "."]


def result(board, move, player):
    new_board = copy.deepcopy(board)
    if new_board.place_game_peice(player, move[0], move[1]):
        return new_board
    else:
        raise ValueError("Invalid move applied to board")


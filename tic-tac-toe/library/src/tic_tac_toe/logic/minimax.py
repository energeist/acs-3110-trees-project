from functools import partial

from tic_tac_toe.logic.models import GameState, Mark, Move

def find_best_move(game_state: GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark
    bound_minimax = partial(minimax, maximizer=maximizer)
    return max(game_state.possible_moves, key=bound_minimax)

def pruned_find_best_move(game_state: GameState) -> Move | None:
    maximizer: Mark = game_state.current_mark
    bound_minimax = partial(pruned_minimax, maximizer=maximizer)
    return max(game_state.possible_moves, key=bound_minimax)

def minimax(
    move: Move, maximizer: Mark, choose_highest_score: bool = False
) -> int:
    """The minimax algorithm is used to determine the best possible move for a player in a zero-sum game."""
    
    # base case, return score if a terminal node has been reached
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    
    #recursive case, maximizer's turn
    if move.after_state.current_mark is maximizer:
        best_score = -2
        for possible_move in move.after_state.possible_moves:
            score = minimax(possible_move, maximizer, not choose_highest_score)
            best_score = max(score, best_score)
        return best_score
    
    #recursive case, not maximizer's turn
    else:            
        best_score = 2
        for possible_move in move.after_state.possible_moves:
            score = minimax(possible_move, maximizer, not choose_highest_score)
            best_score = min(score, best_score)
        return best_score
    
def pruned_minimax(
    move: Move, maximizer: Mark, alpha: int = -2, beta: int = 2, choose_highest_score: bool = False
) -> int:
    """This version of the minimax algorthim uses alpha-beta pruning to reduce the number of nodes that need to be evaluated."""
    
    # base case, return score if a terminal node has been reached
    if move.after_state.game_over:
        return move.after_state.evaluate_score(maximizer)
    
    #recursive case, maximizer's turn
    if move.after_state.current_mark is maximizer:
        best_score = -2
        for possible_move in move.after_state.possible_moves:
            score = pruned_minimax(possible_move, maximizer, alpha, beta, not choose_highest_score)
            best_score = max(score, best_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    
    #recursive case, not maximizer's turn
    else:            
        best_score = 2
        for possible_move in move.after_state.possible_moves:
            score = pruned_minimax(possible_move, maximizer, alpha, beta, not choose_highest_score)
            best_score = min(score, best_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score
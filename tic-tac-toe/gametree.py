# import various utility modules

import enum
import re
import random
import time

# declare winning states as a global constant
# There are 8 game ending states where a win can be determined for either player
# other states are either a draw or the game is still in progress

WINNING_STATES = [
        "???......",
        "...???...",
        "......???",
        "?..?..?..",
        ".?..?..?.",
        "..?..?..?",
        "?...?...?",
        "..?.?.?..",  
    ]
class Mark(str, enum.Enum):
    
    """A representation of the two possible marks in the game."""
    CROSS = "X"
    NAUGHT = "O"
    
    def __str__(self):
        return self.value

    # define a custom eumeration property to return the other mark 
    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT
    
    
class GameTree:
    """This is a game tree representing the game of tic-tac-toe. It contains GameTreeNodes which
    represent the states of the game.  The edges between the nodes represent the possible moves
    that can be made from one state to another.  Handles the game loop and rendering methods in
    this implementation"""
    
    # represent the starting grid as a string of 9 spaces

    # STARTING_GRID = "XOXOX    "
    # STARTING_GRID = "X        "
    
    STARTING_GRID = "OX  X    "
    # random_int = random.randint(0, 8)
    # STARTING_GRID = " " * random_int + "X" + " " * (8 - random_int)
       
    def __init__(self):
        # initialize the root node of the game tree
        self.root = GameTreeNode(Grid(self.STARTING_GRID), Mark("X"))
        self.game_played = [self.root]

    def __str__(self):
        game_progress = ""
        for move in self.game_played:
            game_progress += str(move) + (" -> " if move != self.game_played[-1] else " -> end")
        return str(game_progress)

    def __repr__(self):
        game_progress = ""
        for move in self.game_played:
            game_progress += str(move) + (" -> " if move != self.game_played[-1] else " -> end")
        return str(game_progress)
    
    def render_board(self, game_state):
        """This method renders the current game board to the console."""
        
        # clear the console, should work for modern Windows, Mac, and Linux terminals 
        print("\033c", end="")
        print("Current board state:\n")
        print(game_state)
        
        time.sleep(1)
    
    def play_random(self):
        """This method plays a randomized game of tic-tac-toe for testing purposes.  
        It returns the winning mark or None if the game is a draw."""
        
        # begin playing from the starting game state stored in the root node
        game_state = self.root
        
        # play the game until it is finished
        while not game_state.game_finished():
            
            # render the current board state
            self.render_board(game_state)
            
            # perform a random move
            random_move = game_state.make_random_move()
            
            # update the game state 
            game_state = random_move.after_state

            # add the new game state to the game history
            self.game_played.append(game_state)
        
        # need to render last board state after game ends
        self.render_board(game_state)
        
        # return the winning mark or "draw" if the game is a draw
        return f"Winner is {game_state.winner()}!" if game_state.winner() else "This game ended in a draw."
    
    def play_minimax(self):
        """This method plays a game of tic-tac-toe using the minimax algorithm with alpha-beta pruning for efficiency.  
        It returns the winning mark or None if the game is a draw."""
        
        # begin playing from the starting game state stored in the root node
        game_state = self.root
        
        # play the game until it is finished
        while not game_state.game_finished():
            
            # render the current board state
            self.render_board(game_state)
        
            # get the best move for the current player 
            # maximizing player is always X in this implementation and X always moves first
            _, best_move = game_state.find_best_move(game_state, True)
            
            # perform the best move to update the game state
            game_state = best_move.after_state
            
            # add a board frame to the game_played list
            self.game_played.append(game_state)
            
            # need to render last board state after game ends
            self.render_board(game_state)
        
        # return the winning mark or "draw" if the game is a draw
        return f"Winner is {game_state.winner()}" or "This game ended in a draw."

class Grid:
    
    """Abstracted representation of the game board.  It is represented as a string of 9 spaces"""
    
    def __init__(self, cells = " " * 9):
        self.cells = cells

    def __str__(self):
        return self.cells
    
    def __repr__(self):
        return self.cells
    
    # Helper methods to count the number of each type of space in the current game state
    def count_x(self):
        return self.cells.count("X")
    
    def count_o(self):
        return self.cells.count("O")
    
    def count_empty(self):
        return self.cells.count(" ")
    

class Move:
    
    """Data class abstraction of a move made in the game. It tracks the current player (mark) making a move,
    the cell index of the move, and the state of the game before and after the move is made."""
    
    def __init__(self, mark, cell_index, before_state, after_state):
        self.mark = mark
        self.cell_index = cell_index
        self.before_state = before_state
        self.after_state = after_state
        
    def __str__(self):
        return str(f"before:\n{self.before_state}\nafter:\n{self.after_state}")

    def __repr__(self):
        return str(f"before:\n{self.before_state}\nafter:\n{self.after_state}")


class GameTreeNode:
    
    """A node in the game tree represents a certain state of the game.  It tracks the game state,
    and the player who is to move next.  Handles the game logic in this implementation."""
    
    def __init__(self, game_state, player_to_move = Mark("X")):
        # store children as an instance attribute in a list of GameTreeNodes instead of placeholder?
        # self.children = []
        self.game_state = game_state
        self.player_to_move = player_to_move
        
        # track iterations of minimax?
        self.iteration = 0

    def __str__(self):
        return str(" ___ \n|" + self.game_state.cells[:3] + "|\n|" + self.game_state.cells[3:6] + "|\n|" + self.game_state.cells[6:] + "|\n " + "\u203e"*3 + f"\n\n static eval:{self.static_evaluation(self.current_player())}")

    def __repr__(self):
        return str(self.game_state.cells[:3] + "\n" + self.game_state.cells[3:6] + "\n" + self.game_state.cells[6:])
    
    # Helper method to determine which player is making a move.  X always moves first,
    # so this can be determined by comparing the number of Xs and Os on the board
    
    def current_player(self):
        if self.game_state.count_x() == self.game_state.count_o():
            return self.player_to_move
        else:
            return self.player_to_move.other
    
    # Helper method to determine if the game has not started yet.  This is true if the board is empty.   
    def game_not_started(self):
        return self.game_state.count_empty() == 9
    
    # Method to determine if the current game state is a winning state.  This is true if the current
    # game state's grid layout matches any of the winning patterns for a player.
    def winner(self):
        # check to see if the current game state's grid layout matches any of the winning patterns
        for pattern in WINNING_STATES:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.game_state.cells):
                    return mark
                
    # Helper method to return the winning cells if there is a winner
    def winning_cells(self):
        if self.winner() is not None:
            for pattern in WINNING_STATES:
                for mark in Mark:
                    if re.match(pattern.replace("?", mark), self.game_state.cells):
                        return [i for i, c in enumerate(pattern) if c == "?"]
        else:
            return []
    
    # Helper method to determine if the game is a draw.  This is true if the board full and not
    # in a winning state.
    def draw_state(self):
        if self.winner():
            return False
        else:
            if self.game_state.count_empty() == 0:
                return True
            else:
                return False
    
    # Helper method to determine if the game is over.  This is true if the board is in a winning state
    # or if there are no more possible moves.  
    def game_finished(self):
        if self.winner():
            return True
        if self.winner() is None:
            if self.draw_state():
                return True
        return False
    
    # Method to determine the possible moves from the current game state.  This will return a list of
    # possible valid moves that can be made.    
    def possible_moves(self):
        # initialize an empty list of possible moves
        moves = []
        
        # Valid moves can only be made to empty cells.
        # If the game is not over, iterate through the grid and add a move for each empty cell.
        # If the game is finished, this will return an empty list.
        if not self.game_finished():
            # print("not finished")
            blank_cells = re.finditer(r"\s", self.game_state.cells)
            for match in blank_cells:
                moves.append(self.move_to(match.start()))
        return moves
    
    # Helper method to make a move to a given cell index.  This will return a Move object that can be
    # used to generate the next game state.
    def move_to(self, index):
        
        # validate the proposed move
        if self.game_state.cells[index] != " ":
            raise ValueError("Invalid move: cell is not empty")
        
        next_player = self.current_player().other

        return Move(
            mark = self.current_player(),
            cell_index = index,
            before_state = self,
            
            # after_state will be a new GameTreeNode, which will take a new Grid object with the cells updated
            # to reflect the move that was made.
            after_state = GameTreeNode(
                Grid(
                    # the new grid will contain the existing cells up to the index where the move is being made...
                    self.game_state.cells[:index]
                    # ...plus the moving player's mark...
                    + self.current_player()
                    # ...followed by the remaining cells.
                    + self.game_state.cells[index + 1 :]
                )
            )
        )

    # Method to make a random move, used for testing
    # Returns a move object
    def make_random_move(self):
        random_move = self.move_to(random.choice(self.possible_moves()).cell_index)
        return random_move
    
    # Method to perform static evaluation of the game state.  This is used to determine the score of a
    # terminal node in the game tree.  The score is 1 if the current player is the winner, -1 if the
    # current player is the loser, and 0 if the game is a draw.
        
    def static_evaluation(self, mark):
        if self.game_finished():
            if self.draw_state():
                return 0
            if self.winner() is mark:
                return 1
            else:
                return -1
        else:
            return 0
    
    def find_best_move(self, game_state, maximizing_player, alpha = -2, beta = 2):
        # uses the minimax algorithm with alpha-beta pruning to determine the best possible move for the current player
        # returns a Move object with a before and after state
        
        # print(f"iteration: {iteration}")
        # base case, return score if a leaf node (finished game) has been reached
        if game_state.game_finished():
            print(game_state)
            time.sleep(0.5)
            return game_state.static_evaluation(game_state.current_player()), None
        
        best_move = None
        
        # recursive case with current player as maximizing player
        if maximizing_player:
            
            # initialize best_score to the lowest possible score
            best_score = -2
            
            # iterate through all the possible moves (children) of the current game state
            for move in game_state.possible_moves():
                
                next_state = move.after_state
                # recursively call find_best_move on the child game state
                score, _ = self.find_best_move(next_state, maximizing_player, alpha, beta)
                
                if score > best_score:
                    best_score = score
                    best_move = move
                    
                alpha = max(alpha, best_score)
                
                if beta <= alpha:
                    break
                            
            return best_score, best_move
            
        # recursive case with current player as minimizing player
        else: 
            best_score = 2
            best_move = None
            
            # iterate through all the possible moves (children) of the current game state
            for move in game_state.possible_moves():

                next_state = move.after_state
                # recursively call find_best_move on the child game state
                score, _ = self.find_best_move(next_state, maximizing_player, alpha, beta)
                
                if score < best_score:
                    best_score = score
                    best_move = move
                                
                beta = min(beta, best_score)
                
                if beta <= alpha:
                    break
                
            return best_score, best_move

# Function main runtime code
if __name__ == "__main__":
    
    print("This program will play a game of tic-tac-toe using two AI players as a demo.")
    print("Both AI players are using the minimax algorithm, with alpha-beta pruning incorporated for performance.")
    print("Be warned! This will take a while to run (approximately 90 seconds...)\n")
    
    time.sleep(5)
    
    start = time.time()
    
    # initialize the game tree
    tic_tac_toe = GameTree()
    
    print(tic_tac_toe.play_minimax())
    
    end = time.time()
    
    print(f"Game completed in {(end - start):.3f} seconds.")
    
# import various utility modules

import enum
import re
import random
import time
import os

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

    # define a custom eumeration property to return the other mark 
    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT
    
    
class GameTree:
    """This is a game tree representing the game of tic-tac-toe. It contains GameTreeNodes which
    represent the states of the game.  The edges between the nodes represent the possible moves
    that can be made from one state to another."""
    
    # represent the starting grid as a string of 9 spaces
    STARTING_GRID = " " * 9
       
    def __init__(self):
        # initialize the root node of the game tree
        self.root = GameTreeNode(Grid(self.STARTING_GRID), Mark("X"))
        self.game_played = []

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
    
    def play(self, starting_player = Mark("X")):
        """This method plays a game of tic-tac-toe.  It takes a starting player as an argument and
        returns the winning mark or None if the game is a draw."""
        
        # begin playing from the starting game state stored in the root node
        game_state = self.root
        
        # play the game until it is finished
        while not game_state.game_finished():
            
            # render the current board state
            self.render_board(game_state)
            
            # get the current player
            player = game_state.current_player()
            
            # get the best move for the current player
            move = self.find_best_move(game_state)
            
            # add the move to the list of moves
            moves.append(move)
            
            # update the game state to reflect the move that was made
            game_state = move.after_state
        
        # return the winning mark or None if the game is a draw
        return game_state.winner()
    

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
        return str(f"before: {self.before_state} after: {self.after_state}")

    def __repr__(self):
        return str(f"before: {self.before_state} after: {self.after_state}")


class GameTreeNode:
    
    """A node in the game tree represents a certain state of the game.  It tracks the game state,
    and the player who is to move next"""
    
    def __init__(self, game_state, player_to_move = Mark("X")):
        # store children as an instance attribute in a list of GameTreeNodes instead of placeholder?
        # self.children = []
        self.game_state = game_state
        self.player_to_move = player_to_move

    def __str__(self):
        return str(self.game_state.cells[:2] + "\n" + self.game_state.cells[3:5] + "\n" + self.game_state.cells[6:])

    def __repr__(self):
        return str(self.game_state.cells[:2] + "\n" + self.game_state.cells[3:5] + "\n" + self.game_state.cells[6:])
    
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

    # Method to perform static evaluation of the game state.  This is used to determine the score of a
    # terminal node in the game tree.  The score is 1 if the current player is the winner, -1 if the
    # current player is the loser, and 0 if the game is a draw.
    
    def static_evaluation(self, mark):
        if self.game_finished:
            if self.draw_state:
                return 0
            if self.winner is mark:
                return 1
            else:
                return -1
        raise ValueError("Game is not finished")

# Function main runtime code
if __name__ == "__main__":
    
    print("This program will play a game of tic-tac-toe using two AI players as a demo.")
    print("Both AI players are using the minimax algorithm, with alpha-beta pruning incorporated for performance.\n")
    
    start = time.time()
    
    # initialize the game tree
    tic_tac_toe = GameTree()
    
    print(tic_tac_toe.play())
    
    end = time.time()
    
    print(f"Game completed in {(end - start):.3f} seconds.")
    
    

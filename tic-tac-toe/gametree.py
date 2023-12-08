# import various utility modules

import enum
import re
import random
import time

class GameTree:
    """This is a game tree representing the game of tic-tac-toe. It contains GameTreeNodes which
    represent the states of the game.  The edges between the nodes represent the possible moves
    that can be made from one state to another."""
    
    # represent the starting grid as a string of 9 spaces
    STARTING_GRID = " " * 9
    
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
       
    def __init__(self, root):
        self.root = root

    def __str__(self):
        return str(self.root)

    def __repr__(self):
        return str(self.root)

    
class Mark(str, enum.Enum):
    
    """A representation of the two possible marks in the game."""
    CROSS = "X"
    NAUGHT = "O"

    # define a custom eumeration property to return the other mark 
    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT


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
        return self.game_state.count("X")
    
    def count_o(self):
        return self.game_state.count("O")
    
    def count_empty(self):
        return self.game_state.count(" ")
    

class Move:
    
    """Data class abstraction of a move made in the game. It tracks the current player (mark) making a move,
    the cell index of the move, and the state of the game before and after the move is made."""
    
    def __init__(self, mark, cell_index, before_state, after_state):
        self.mark = mark
        self.cell_index = cell_index
        self.before_state = before_state
        self.after_state = after_state


class GameTreeNode:
    
    """A node in the game tree represents a certain state of the game.  It tracks the game state,
    and the player who is to move next"""
    
    def __init__(self, game_state, player_to_move = Mark("X"), parent=None):
        self.game_state = game_state
        self.player_to_move = player_to_move
        # self.parent = parent
        # self.children = []

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return str(self.state)
    
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
    
    # Methods to determine if the game is in a winning, losing, or draw state
    def winner(self):
        # check to see if the current game state's grid layout matches any of the winning patterns
        for pattern in WINNING_STATES:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.game_state.cells):
                    return mark
                
    # Helper method to return the winning cells if there is a winner
    def winning_cells(self):
        for pattern in WINNING_STATES:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.game_state.cells):
                    return [i for i, c in enumerate(pattern) if c == "?"]
    
    def draw_state(self):
        return self.winner is None and self.game_state.count_empty() == 0
    
    # Helper method to determine if the game is over.  This is true if the board is in a winning state
    # or if there are no more possible moves.  
    def game_finished(self):
        pass
        
    def possible_moves(self):
        pass
    
    def add_child(self, child):
        self.children.append(child)

# Function main runtime code
if __name__ == "__main__":
    pass    
    

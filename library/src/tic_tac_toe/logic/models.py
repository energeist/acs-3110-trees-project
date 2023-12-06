from __future__ import annotations # for typehinting

import enum
import re
from dataclasses import dataclass
from functools import cached_property

WINNING_PATTERNS = ( # all possible winning patterns represented as strings
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)

class Mark(str, enum.Enum): # mixed enum so that we can compare against strings 
    CROSS = 'X'
    NAUGHT = 'O'

    @property
    def other(self) -> "Mark":
        return Mark.CROSS if self is Mark.NAUGHT else Mark.NAUGHT
    
@dataclass(frozen=True)
class Grid:
    cells: str = " " * 9 # represents the 3x3 grid as a string of 9 characters
    
    def __post_init__(self) -> None:
        if not re.match(r"[\sXO]{9}", self.cells):
            raise ValueError(
                f"Invalid grid cells, must contain 9 cells of only 'X', 'O' or ' '.)"
            )
            
    @cached_property
    def x_count(self) -> int:
        return self.cells.count("X")
    
    @cached_property
    def o_count(self) -> int:
        return self.cells.count("O")
    
    @cached_property
    def empty_count(self) -> int:
        return self.cells.count(" ")
    
@dataclass(frozen=True)
class Move: # Data transfer object to carry data between functions
    mark: Mark
    cell_index: int
    before_state: "GameState"
    after_state: "GameState"
    
@dataclass(frozen=True)
class GameState:
    grid: Grid
    starting_mark: Mark = Mark("X")
    
    @cached_property
    def current_mark(self) -> Mark:
        if self.grid.x_count == self.grid.o_count:
            return self.starting_mark
        else:
            return self.starting_mark.other
        
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == 9
    
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self) -> bool:
        return self.grid.empty_count == 0 and self.winner is None
    
    @cached_property
    def winner(self) ->  Mark | None:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return mark
        return None
    
    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return [
                        match.start()
                        for match in re.finditer(r"\?", pattern)
                    ]
        return []
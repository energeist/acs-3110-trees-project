from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tic_tac_toe.logic.models import GameState, Grid, Mark

import re

from tic_tac_toe.logic.exceptions import InvalidGameState

def validate_grid(grid: Grid) -> None:
    if not re.match(r"^[\sXO]{9}$", grid.cells):
        raise ValueError("Invalid grid cells, must contain 9 cells of only 'X', 'O' or ' '.")
    
def validate_game_state(game_state: GameState) -> None:
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.starting_mark)
    validate_winner(
        game_state.grid,
        game_state.starting_mark.other,
        game_state.winner
    )
    
def validate_number_of_marks(grid: Grid) -> None:
    if abs(grid.x_count - grid.o_count) > 1:
        raise InvalidGameState("Invalid number of marks, must be equal or one more than the other.")

def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
    if grid.x_count > grid.o_count:
        if starting_mark != "X":
            raise InvalidGameState("Incorrect starting mark, must be 'X'.")
    elif grid.o_count > grid.x_count:
        if starting_mark != "O":
            raise InvalidGameState("Incorrect starting mark, must be 'O'.")
        
def validate_winner(
    grid: Grid, starting_mark: Mark, winner: Mark | None
) -> None:
    if winner == "X":
        if starting_mark == "X":
            if grid.x_count <= grid.o_count:
                raise InvalidGameState("Wrong number of 'X's")
        else:
            if grid.x_count != grid.o_count:
                raise InvalidGameState("Wrong number of 'X's")
    elif winner == "O":
        if starting_mark == "O":
            if grid.o_count <= grid.x_count:
                raise InvalidGameState("Wrong number of 'O's")
        else:
            if grid.o_count != grid.x_count:
                raise InvalidGameState("Wrong number of 'O's")
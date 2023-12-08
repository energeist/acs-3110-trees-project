from tic_tac_toe.game.engine import TicTacToe
import time

from .args import parse_args
from .renderers import ConsoleRenderer

def main() -> None:
    player1, player2, starting_mark = parse_args()
    if type(player1).__name__ == "MinimaxComputerPlayer" and type(player2).__name__ == "MinimaxComputerPlayer":
        print("This game is initializing with two minimax AI computer players and will take some time to load the game tree.")
        print("Calculations will begin in 5 seconds and will take approximately 40 seconds to complete.  Please wait...")
        time.sleep(5)
    TicTacToe(player1, player2, ConsoleRenderer()).play(starting_mark)

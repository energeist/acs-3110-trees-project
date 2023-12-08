# ACS-3110 Advanced Trees & Sorting Final project

This project uses a game tree representation and the minimax algorithm to build a simple AI on top of a tic-tac-toe game.

## How to run this project

- Clone this repo and `cd tic-tac-toe` to enter the root directory
- You will need to install the library package locally, so start a virtual environment with `python3 -m venv venv`, or similar
- Install the `/library` module locally with `python3 -m pip install library`
- To run the program, `cd frontends` to enter the frontends directory, then use `python3 -m console` to execute main() using default parameters.

At default, the program will instantiate with the `X` marker as a human player and the `O` marker as a minimax AI computer player.  This can be overridden as follows:

- To play as two human players: `python3 -m console -X human -O human`
- To play as two minimax AI players: `python3 -m console -X minimax -O minimax`
- To play as two minimax AI players using alpha-beta pruning optimization: `python3 -m console -X pruned -O pruned`

Running with two minimax AIs takes some time to generate initial states (approximately 40 seconds), so please be patient.  AIs can be mixed and matched with varying degrees of performance enhancement depending on ordering, as can be seen from these results:


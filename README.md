# ACS-3110 Advanced Trees & Sorting Final project

This project uses a game tree representation and the minimax algorithm to build a simple AI on top of a tic-tac-toe game.  There are two implementations in this repository: one barebones implementation for the logic and one built off a pre-existing framework that employs caching for performance and looks a little better, and will also let you play against the AI.

## How to run this project

### Logic demo & testing suite

This simple game tree implementation will play a game of tic-tac-toe with two AI players will pick a random first move to ensure that each game played is different.  There is no human-player option in this version of the game.

- Clone this repo and `cd acs-3110-trees-project/tic-tac-toe` to enter the root directory
- `python3 gametree.py` to run the logic demo showing functional outcomes of the game tree and logic
- `python3 gametreetest.py` to execute the the test suite.

### Playable application

The game framework for this implementation was built with guidance from [this tutorial from Real Python](https://realpython.com/tic-tac-toe-ai-python/)

- Clone this repo and `cd acs-3110-trees-project/tic-tac-toe` to enter the root directory
- You will need to install the library package locally, so start a virtual environment with `python3 -m venv venv`, or similar
- activate your virtual environment with `source venv/bin/activate`
- Install the `library` module locally with `python3 -m pip install library/`
- To run the program, `cd frontends` to enter the frontends directory, then use `python3 -m console` to execute main() using default parameters.

At default, the program will instantiate with the `X` marker as a human player and the `O` marker as a minimax AI computer player.  This can be overridden as follows:

- To play as two human players: `python3 -m console -X human -O human`
- To play as two minimax AI players: `python3 -m console -X minimax -O minimax`
- To play as two minimax AI players using alpha-beta pruning optimization: `python3 -m console -X pruned -O pruned`

When playing with two AI players you should always expect the game to end in a draw!  They're both trying their best to not lose, and they're pretty good at achieving that goal.  

Running with two minimax AIs takes some time to generate initial states (approximately 40 seconds), so please be patient.  For comparison, the same action in the barebones implementation without caching takes almost 120 seconds!  

AIs can be mixed and matched with varying degrees of performance enhancement depending on ordering, as can be seen from these results:

Runtime using two standard minimax AI players:

![image](https://github.com/energeist/acs-3110-trees-project/assets/111889289/a9041516-1be3-4290-8419-630f02b550d0)

Runtime using Player 1 standard minimax AI and Player 2 pruned minimax AI:

![image](https://github.com/energeist/acs-3110-trees-project/assets/111889289/452b6721-e083-4cee-ba3c-fcd88d04adef)

Runtime using Player 1 pruned minimax AI and Player 2 standard minimax AI:

![image](https://github.com/energeist/acs-3110-trees-project/assets/111889289/e18470c1-b4e9-46d2-8c91-dcf82708deb9)

Runtime using two pruned minimax AI players:

![image](https://github.com/energeist/acs-3110-trees-project/assets/111889289/dcce33d7-559d-44f2-8a37-1e2bf365485a)


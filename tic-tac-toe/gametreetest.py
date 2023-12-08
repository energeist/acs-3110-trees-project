from gametree import GameTree, GameTreeNode, Mark, Grid
import unittest

class GameTreeTest(unittest.TestCase):
    
    def test_init_and_properties(self):
        tree = GameTree()
        assert tree.STARTING_GRID == " " * 9
        assert tree.WINNING_STATES == [
            "???......",
            "...???...",
            "......???",
            "?..?..?..",
            ".?..?..?.",
            "..?..?..?",
            "?...?...?",
            "..?.?.?..",  
        ]
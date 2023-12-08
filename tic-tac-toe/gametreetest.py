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
        
class MarkTest(unittest.TestCase):
    
    def test_init_and_properties(self):
        assert Mark.CROSS == "X"
        assert Mark.NAUGHT == "O"
        assert Mark.CROSS.other == Mark.NAUGHT
        assert Mark.NAUGHT.other == Mark.CROSS
        
class GridTest(unittest.TestCase):
    def test_grid_configurations(self):
        grid1 = Grid()
        assert grid1.cells == " " * 9
        assert grid1.count_x() == 0
        assert grid1.count_o() == 0
        assert grid1.count_empty() == 9
    
        grid2 = Grid("XOXOXOXOX")
        assert grid2.cells == "XOXOXOXOX"
        assert grid2.count_x() == 5
        assert grid2.count_o() == 4
        assert grid2.count_empty() == 0

class MoveTest(unittest.TestCase):
    pass

class GameTreeNodeTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
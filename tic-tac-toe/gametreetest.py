from gametree import WINNING_STATES, GameTree, GameTreeNode, Mark, Grid
import unittest

class GameTreeTest(unittest.TestCase):
    def test_init_and_properties(self):
        tree = GameTree()
        assert tree.STARTING_GRID == " " * 9
        assert WINNING_STATES == [
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
        
        grid2 = Grid("XOX   OXO")
        assert grid2.cells == "XOX   OXO"
        assert grid2.count_x() == 3
        assert grid2.count_o() == 3
        assert grid2.count_empty() == 3

class MoveTest(unittest.TestCase):
    pass

class GameTreeNodeTest(unittest.TestCase):
    def test_init_and_properties(self):
        starting_grid = Grid("XOX      ")
        assert starting_grid.cells == "XOX      "
        assert starting_grid.count_x() == 2
        assert starting_grid.count_o() == 1
        assert starting_grid.count_empty() == 6
        
        new_node = GameTreeNode(starting_grid)
        assert new_node.game_state == starting_grid
        # there are 2 Xs and 1 O on board so current player should be Mark.NAUGHT and no finish/win/draw states should register
        assert new_node.current_player() == Mark.NAUGHT
        assert not new_node.game_not_started()
        assert not new_node.winner()
        assert not new_node.winning_cells()
        assert not new_node.draw_state()
        assert not new_node.game_finished()

if __name__ == '__main__':
    unittest.main()
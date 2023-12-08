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
    def test_an_empty_grid(self):
        starting_grid = Grid()
        assert starting_grid.cells == " " * 9
        assert starting_grid.count_x() == 0
        assert starting_grid.count_o() == 0
        assert starting_grid.count_empty() == 9
        
        new_node = GameTreeNode(starting_grid)
        assert new_node.game_state == starting_grid
        # there are no Xs or Os on board so current player should be Mark.CROSS and no finish/win/draw states should register 
        assert new_node.current_player() == Mark.CROSS
        assert new_node.game_not_started()
        assert not new_node.winner()
        assert not new_node.winning_cells()
        assert not new_node.draw_state()
        assert not new_node.game_finished()
        
    def test_an_unfinished_grid(self):
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

    def test_a_winning_grid_for_X(self):
        starting_grid = Grid("XXXOO    ")
        assert starting_grid.cells == "XXXOO    "
        assert starting_grid.count_x() == 3
        assert starting_grid.count_o() == 2
        assert starting_grid.count_empty() == 4
        
        new_node = GameTreeNode(starting_grid)
        
        assert new_node.game_state == starting_grid
        assert not new_node.game_not_started()
        
        # there are 3 Xs and 2 Os on board so current player should be Mark.NAUGHT and winner should be Mark.CROSS
        assert new_node.current_player() == Mark.NAUGHT
        
        # X should be declared winner and winner() should return Mark.CROSS
        assert new_node.winner() == Mark.CROSS
        
        # winning_cells() should return the indices of the winning cells
        assert new_node.winning_cells() == [0, 1, 2]
        
        assert not new_node.draw_state()
        assert new_node.game_finished()
        
        # the game is finished so there should be no possible moves
        assert new_node.possible_moves() == []
        
    def test_a_winning_grid_for_O(self):
        # tests should be the same as above, but inversed
        starting_grid = Grid("OOOXX    ")
        assert starting_grid.cells == "OOOXX    "
        assert starting_grid.count_x() == 2
        assert starting_grid.count_o() == 3
        assert starting_grid.count_empty() == 4
        
        new_node = GameTreeNode(starting_grid)
        
        assert new_node.game_state == starting_grid
        assert not new_node.game_not_started()
        
        # there are 2 Xs and 3 Os on board so current player should be Mark.CROSS and winner should be Mark.NAUGHT
        # assert new_node.current_player() == Mark.CROSS
        
        assert new_node.winner() == Mark.NAUGHT
        
        assert new_node.winning_cells() == [0, 1, 2]
        
        assert not new_node.draw_state()
        assert new_node.game_finished()
        
        assert new_node.possible_moves() == []
        
    def test_a_full_draw_state_grid(self):
        starting_grid = Grid("XOXXOXOXO")
        assert starting_grid.cells == "XOXXOXOXO"
        assert starting_grid.count_x() == 5
        assert starting_grid.count_o() == 4
        assert starting_grid.count_empty() == 0
        
        # finish this
if __name__ == '__main__':
    unittest.main()
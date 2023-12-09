from gametree import WINNING_STATES, GameTree, GameTreeNode, Mark, Move, Grid
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
        
        moves = new_node.possible_moves()
        assert len(moves) == 9
        assert type(moves[0]) == Move
        assert type(moves[0].mark) == Mark
        assert type(moves[0].before_state) == GameTreeNode
        assert type(moves[0].after_state) == GameTreeNode
        assert moves[0].mark == Mark.CROSS
        assert moves[0].cell_index == 0

        # A Move contains before and after state as GameTreeNodes, which have a game_state property that is a Grid, which has a cells property.
        assert moves[0].before_state.game_state.cells == starting_grid.cells
        assert moves[0].after_state.game_state.cells == "X" + starting_grid.cells[1:]
        assert moves[1].after_state.game_state.cells == starting_grid.cells[:1] + "X" + starting_grid.cells[2:]
        assert moves[7].after_state.game_state.cells == starting_grid.cells[:7] + "X" + starting_grid.cells[8:]
        assert moves[8].after_state.game_state.cells == starting_grid.cells[:8] + "X"
    
    def test_an_unfinished_grid_with_X_moving(self):
        starting_grid = Grid("OXOX     ")
        assert starting_grid.cells == "OXOX     "
        assert starting_grid.count_x() == 2
        assert starting_grid.count_o() == 2
        assert starting_grid.count_empty() == 5
        
        new_node = GameTreeNode(starting_grid)
        assert new_node.game_state == starting_grid
        # there are 2 Xs and 2 Os on board so current player should be Mark.NAUGHT and no finish/win/draw states should register
        assert new_node.current_player() == Mark.CROSS
        assert not new_node.game_not_started()
        assert not new_node.winner()
        assert not new_node.winning_cells()
        assert not new_node.draw_state()
        assert not new_node.game_finished()
        
        moves = new_node.possible_moves()
        assert len(moves) == 5
        assert type(moves[0]) == Move
        assert type(moves[0].mark) == Mark
        assert type(moves[0].before_state) == GameTreeNode
        assert type(moves[0].after_state) == GameTreeNode
        assert moves[0].mark == Mark.CROSS
        assert moves[0].cell_index == 4

        # A Move contains before and after state as GameTreeNodes, which have a game_state property that is a Grid, which has a cells property.
        assert moves[0].before_state.game_state.cells == starting_grid.cells
        assert moves[0].after_state.game_state.cells == starting_grid.cells[:moves[0].cell_index] + new_node.current_player() + starting_grid.cells[(moves[0].cell_index + 1):]
        assert moves[1].after_state.game_state.cells == starting_grid.cells[:moves[1].cell_index] + new_node.current_player() + starting_grid.cells[(moves[1].cell_index + 1):]
        assert moves[4].after_state.game_state.cells == starting_grid.cells[:moves[4].cell_index] + new_node.current_player() + starting_grid.cells[(moves[4].cell_index + 1):]  
        
    def test_an_unfinished_grid_with_O_moving(self):
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
        
        moves = new_node.possible_moves()
        assert len(moves) == 6
        assert type(moves[0]) == Move
        assert type(moves[0].mark) == Mark
        assert type(moves[0].before_state) == GameTreeNode
        assert type(moves[0].after_state) == GameTreeNode
        assert moves[0].mark == Mark.NAUGHT
        assert moves[0].cell_index == 3

        # A Move contains before and after state as GameTreeNodes, which have a game_state property that is a Grid, which has a cells property.
        assert moves[0].before_state.game_state.cells == starting_grid.cells
        assert moves[0].after_state.game_state.cells == starting_grid.cells[:moves[0].cell_index] + new_node.current_player() + starting_grid.cells[(moves[0].cell_index + 1):]
        assert moves[1].after_state.game_state.cells == starting_grid.cells[:moves[1].cell_index] + new_node.current_player() + starting_grid.cells[(moves[1].cell_index + 1):]
        assert moves[5].after_state.game_state.cells == starting_grid.cells[:moves[5].cell_index] + new_node.current_player() + starting_grid.cells[(moves[5].cell_index + 1):]  
    
    def test_an_unfinished_with_empty_central_tiles(self):
        starting_grid = Grid("XOX     O")
        assert starting_grid.cells == "XOX     O"
        assert starting_grid.count_x() == 2
        assert starting_grid.count_o() == 2
        assert starting_grid.count_empty() == 5
        
        new_node = GameTreeNode(starting_grid)
        assert new_node.game_state == starting_grid
        # there are 2 Xs and 1 O on board so current player should be Mark.NAUGHT and no finish/win/draw states should register
        assert new_node.current_player() == Mark.CROSS
        assert not new_node.game_not_started()
        assert not new_node.winner()
        assert not new_node.winning_cells()
        assert not new_node.draw_state()
        assert not new_node.game_finished()
        
        moves = new_node.possible_moves()
        assert len(moves) == 5
        assert type(moves[0]) == Move
        assert type(moves[0].mark) == Mark
        assert type(moves[0].before_state) == GameTreeNode
        assert type(moves[0].after_state) == GameTreeNode
        assert moves[0].mark == Mark.CROSS
        assert moves[0].cell_index == 3

        # A Move contains before and after state as GameTreeNodes, which have a game_state property that is a Grid, which has a cells property.
        assert moves[0].before_state.game_state.cells == starting_grid.cells
        assert moves[0].after_state.game_state.cells == starting_grid.cells[:moves[0].cell_index] + new_node.current_player() + starting_grid.cells[(moves[0].cell_index + 1):]
        assert moves[1].after_state.game_state.cells == starting_grid.cells[:moves[1].cell_index] + new_node.current_player() + starting_grid.cells[(moves[1].cell_index + 1):]
        assert moves[4].after_state.game_state.cells == starting_grid.cells[:moves[4].cell_index] + new_node.current_player() + starting_grid.cells[(moves[4].cell_index + 1):]  
    
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
        
        new_node = GameTreeNode(starting_grid)
        
        assert new_node.game_state == starting_grid
        assert not new_node.game_not_started()
        
        # there are 2 Xs and 3 Os on board so current player should be Mark.CROSS and winner should be Mark.NAUGHT
        # assert new_node.current_player() == Mark.CROSS
        
        assert new_node.winner() == None
        
        assert new_node.winning_cells() == []
        
        assert new_node.draw_state()
        assert new_node.game_finished()
        
        assert new_node.possible_moves() == []
        
    def test_a_random_move_on_unfinished_grid(self):
        starting_grid = Grid("XOX      ")
        assert starting_grid.cells == "XOX      "
        assert starting_grid.count_x() == 2
        assert starting_grid.count_o() == 1
        assert starting_grid.count_empty() == 6
        
        new_node = GameTreeNode(starting_grid)
        
        random_move = new_node.make_random_move()

        assert random_move.mark == Mark.NAUGHT
        assert random_move.after_state.game_state.count_x() == 2
        assert random_move.after_state.game_state.count_o() == 2
        assert random_move.after_state.game_state.count_empty() == 5
        
    def test_a_random_game(self):
        game = GameTree()
        game.play_random()
        
        # random game will always take at least 5 moves and ends in 9 moves at most
        assert len(game.game_played) >= 6 # includes root node, so 5 moves is 6 nodes
        assert len(game.game_played) <= 10 # includes root node, so 9 moves is 10 nodes
        
        # first node in game_played should be the root node with game_not_started() == True
        assert game.game_played[0].game_not_started()
        
        # only last frame should be game_finished() == True
        assert not game.game_played[-2].game_finished()
        assert game.game_played[-1].game_finished()
        
        # X goes first so there should always be at least 3 Xs and 2 Os on the board
        assert game.game_played[-1].game_state.count_x() >= 3
        assert game.game_played[-1].game_state.count_o() >= 2
        assert game.game_played[-1].game_state.count_empty() <= 4
          
    def test_static_evaluation(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
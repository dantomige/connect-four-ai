import unittest
from enum import Enum
from game import Board, BoardPlayers

class TestBoardPlayers(unittest.TestCase):

    def test_board_players_str(self):
        self.assertEqual(str(BoardPlayers.RED), "X")
        self.assertEqual(str(BoardPlayers.YELLOW), "O")

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_initial_board_empty(self):
        for row in self.board.board:
            for cell in row:
                self.assertIsNone(cell)

    def test_drop_piece(self):
        self.board.drop_piece(1, BoardPlayers.RED)
        self.assertEqual(self.board.board[5][0], BoardPlayers.RED)

        self.board.drop_piece(1, BoardPlayers.YELLOW)
        self.assertEqual(self.board.board[4][0], BoardPlayers.YELLOW)

    def test_drop_piece_invalid_column(self):
        with self.assertRaises(AssertionError):
            self.board.drop_piece(0, BoardPlayers.RED)
        with self.assertRaises(AssertionError):
            self.board.drop_piece(8, BoardPlayers.YELLOW)

    def test_drop_piece_invalid_player(self):
        with self.assertRaises(AssertionError):
            self.board.drop_piece(1, "InvalidPlayer")

    def test_is_drawn_false(self):
        self.assertFalse(self.board.is_drawn())

    def test_is_drawn_true(self):
        for col in range(1, self.board.NUM_COLS + 1):
            for row in range(self.board.NUM_ROWS):
                self.board.drop_piece(col, BoardPlayers.RED if row % 2 == 0 else BoardPlayers.YELLOW)
        self.assertTrue(self.board.is_drawn())

    def test_reset_board(self):
        self.board.drop_piece(1, BoardPlayers.RED)
        self.board.reset_board()
        for row in self.board.board:
            for cell in row:
                self.assertIsNone(cell)

    def test_board_str(self):
        self.board.drop_piece(1, BoardPlayers.RED)
        self.board.drop_piece(2, BoardPlayers.YELLOW)
        expected_output = ("|   |   |   |   |   |   |   |\n" * 5 + "| X | O |   |   |   |   |   |\n" + "_" * 29)
        self.assertEqual(str(self.board), expected_output)

    def test_horizontal_win(self):
        for col in range(1, 5):
            self.board.drop_piece(col, BoardPlayers.RED)
        self.assertTrue(self.board.has_won_player(BoardPlayers.RED, 4, 5))

    def test_vertical_win(self):
        for row in range(4):
            self.board.drop_piece(1, BoardPlayers.YELLOW)
        self.assertTrue(self.board.has_won_player(BoardPlayers.YELLOW, 1, 2))

    def test_diagonal_win_positive_slope(self):
        moves = [(1, BoardPlayers.RED), (2, BoardPlayers.YELLOW), (2, BoardPlayers.RED),
                 (3, BoardPlayers.YELLOW), (3, BoardPlayers.YELLOW), (3, BoardPlayers.RED),
                 (4, BoardPlayers.YELLOW), (4, BoardPlayers.YELLOW), (4, BoardPlayers.YELLOW), (4, BoardPlayers.RED)]
        for col, player in moves:
            self.board.drop_piece(col, player)
        self.assertTrue(self.board.has_won_player(BoardPlayers.RED, 4, 2))

    def test_diagonal_win_negative_slope(self):
        moves = [(4, BoardPlayers.RED), (3, BoardPlayers.YELLOW), (3, BoardPlayers.RED),
                 (2, BoardPlayers.YELLOW), (2, BoardPlayers.YELLOW), (2, BoardPlayers.RED),
                 (1, BoardPlayers.YELLOW), (1, BoardPlayers.YELLOW), (1, BoardPlayers.YELLOW), (1, BoardPlayers.RED)]
        for col, player in moves:
            self.board.drop_piece(col, player)
        self.assertTrue(self.board.has_won_player(BoardPlayers.RED, 1, 2))

if __name__ == "__main__":
    unittest.main()

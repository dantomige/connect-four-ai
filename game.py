from enum import Enum

class BoardPlayers(Enum):
    RED = 1
    YELLOW = 2

    def switch_players(self):
        if self.name == "RED":
            return BoardPlayers.YELLOW
        elif self.name == "YELLOW":
            return BoardPlayers.RED

    def __str__(self):
        if self.value == 1:
            return "X"
        elif self.value == 2:
            return "O"
        else:
            return "Error"


class Board:

    def __init__(self):
        """ Initializes an empty connect for board
        """
        self.board = [[None for _ in range(7)] for _ in range(6)]
        self.NUM_ROWS = 6
        self.NUM_COLS = 7
        
    def has_won(self, player: BoardPlayers):
        """Determines if 'player' has won the game

        Args:
            player (BoardPlayers): a player of color RED or YELLOW
       
        Returns:
            bool: true if there player has won
        """

        def get_at_location(row, col):
            if not 0 <= row < self.NUM_ROWS or not 0 <= col < self.NUM_COLS:
                return None
            return self.board[row][col]

        def check_four_directions(row, col):
            h_count, v_count, dr_count, dl_count = 0, 0, 0, 0
            for i in range(4):
                # check horizontal
                h_count += (get_at_location(row, col + i) == player)
                # check vertical
                v_count += (get_at_location(row + i, col) == player)
                # check diagonal down right
                dr_count += (get_at_location(row + i, col + i) == player)
                # check diagonal down left
                dl_count += (get_at_location(row - i, col + i) == player)
            return max(h_count, v_count, dr_count, dl_count) == 4 # if any wins
        
        for row in range(self.NUM_ROWS):
            for col in range(self.NUM_COLS):
                if self.board[row][col] == player:
                    if check_four_directions(row, col):
                        return True      
        return False

    def is_drawn(self):
        """Determines if the game is drawn i.e. no other moves can be made.
        """
        for col in range(self.NUM_COLS):
            if self.board[0][col] is None:
                return False
        return True

    def drop_piece(self, column: int, player: BoardPlayers):
        """Drops a piece of color 'player''s types into the column 'column
        where the left most column is of index 1 and the right most is of index 7

        Args:
            column (int): an integer representing the column index
            player (BoardPlayers): player color

        """
        # print(f"Checking player: player={player}, type(player)={type(player)}, BoardPlayers={BoardPlayers}")
        # assert(False, "working")
        assert 0 < column <= self.NUM_COLS, f"column index {column} must be in board"
        assert isinstance(player, BoardPlayers), f"{player} should be of BoardPlayer type"
        assert self.board[0][column - 1] == None, f"column index {column} is already full" 

        curr_row = 0

        while curr_row < self.NUM_ROWS - 1 and self.board[curr_row + 1][column - 1] == None:
            curr_row += 1

        self.board[curr_row][column - 1] = player

    def copy_board(self):
        """Creates a brand new copy of the board
        """

        new_board_internal = [[item for item in row] for row in self.board]
        new_board = Board()
        new_board.board = new_board_internal
        return new_board

    def reset_board(self):
        """Resets the game board
        """
        self.board = [[None for _ in range(7)] for _ in range(6)]

    def __str__(self):
        """Visual representation of the game board where
        """
        
        out = ""
        for row_index in range(6):
            row = "|"
            for col_index in range(7):
                if self.board[row_index][col_index] is not None:
                    row += f' {str(self.board[row_index][col_index])} '
                else:
                    row += f'   '
                row += "|"
            out += row + "\n"
        out += "_" * (self.NUM_COLS * 4 + 1)
        return out

board = Board()
# board.drop_piece(0, BoardPlayers.RED)
# board.drop_piece(0, BoardPlayers.RED)
# board.drop_piece(0, BoardPlayers.RED)
# print(board.has_won(BoardPlayers.RED))
# board.drop_piece(0, BoardPlayers.RED)
# print(board.has_won(BoardPlayers.RED))
# print(board)
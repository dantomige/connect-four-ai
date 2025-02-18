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

class GameState(Enum):
    EMPTY = 1
    PLAYING = 2
    WON = 3
    DRAWN = 4
    

class Board:

    def __init__(self):
        """ Initializes an empty connect for board
        """
        self.board = [[None for _ in range(7)] for _ in range(6)]
        self.NUM_ROWS = 6
        self.NUM_COLS = 7
        self.NUM_TO_WIN = 4
        self.DOWN = self.RIGHT = 1
        self.UP = self.LEFT = -1
        self.STAY = 0
        self.game_state = GameState.EMPTY

    def is_drawn(self) -> bool:
        """Determines if the game is drawn i.e. no other moves can be made.
        """
        for col in range(self.NUM_COLS):
            if self.board[0][col] is None:
                return False
        return True

    def drop_piece(self, column: int, player: BoardPlayers) -> GameState:
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

        if self.is_drawn():
            self.game_state = GameState.DRAWN
        elif self.has_won(player, column, curr_row):
            self.game_state = GameState.WON
        else:
            self.game_state = GameState.PLAYING
        return self.game_state


    def check_direction(self, player: BoardPlayers, column: int, row: int, column_dir: int, row_dir: int) -> int:
        count = 0
        row_indices = [row + delta * row_dir for delta in range(self.NUM_TO_WIN)]
        col_indices = [column - 1 + delta * column_dir for delta in range(self.NUM_TO_WIN)]

        for r, c in zip(row_indices, col_indices):
            if r is None or c is None:
                break
            if (r >= self.NUM_ROWS or r < 0) or (c >= self.NUM_COLS or c < 0):
                break
            if self.board[r][c] != player:
                break
            count += 1

        return count

    def check_diagonal(self, player: BoardPlayers, column: int, row: int) -> bool:
        pos_slope_diag_count = self.check_direction(
            player,
            column,
            row,
            self.RIGHT,
            self.UP
        ) + self.check_direction(
            player,
            column,
            row,
            self.LEFT,
            self.DOWN
        ) - 1

        neg_slope_diag_count = self.check_direction(
            player,
            column,
            row,
            self.RIGHT,
            self.DOWN
        ) + self.check_direction(
            player,
            column,
            row,
            self.LEFT,
            self.UP
        ) - 1

        return pos_slope_diag_count >= 4 or neg_slope_diag_count >= 4
    
    def check_horizontal(self, player: BoardPlayers, column: int, row: int) -> bool:
        count = self.check_direction(
            player,
            column,
            row,
            self.RIGHT,
            self.STAY
        ) + self.check_direction(
            player,
            column,
            row,
            self.LEFT,
            self.STAY
        ) - 1
        return count >= 4

    def check_vertical(self, player: BoardPlayers, column: int, row: int) -> bool:
        count = self.check_direction(player, column, row, self.STAY, self.DOWN)
        return count == 4

    def has_won(self, player: BoardPlayers, column: int, row: int) -> bool:
        """Checks if player has won given that the last move was at column (indexed 1 to 7) and row (indexed 0 to 5)

        Args:
            player (BoardPlayers): a player of RED or YELLOW
            column (_type_): column where the last player piece was dropped
            row (_type_): row where the last player piece was dropped
        """
        checks = [self.check_vertical, self.check_horizontal, self.check_diagonal]
        return any(check(player, column, row,) for check in checks)

        
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

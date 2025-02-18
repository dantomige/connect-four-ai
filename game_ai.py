from game import Board, BoardPlayers


class Connect4AI:

    def __init__(self, board: Board, search_depth: int, player: BoardPlayers):
        self.board = board
        self.search_depth = search_depth
        self.player = player

    def find_best_move(self) -> int:
        """Finds the best move based on the state of the board.

        Returns: the column index [1, 7] of the best move

        Asserts the game has not already ended
        """

        assert not self.board.is_drawn(), "expected the game to not already end (drawn)"
        for player in [BoardPlayers.RED, BoardPlayers.YELLOW]:
            assert not self.board.has_won(player), f"expected the game to not already end (winner: {player})"

        new_board = self.board
        return self.minimax(self.player, self.search_depth, )
    
    def available_moves(self):
        moves = []
        for col in range(self.board.NUM_COLS):
            if self.board[0][col] == None:
                moves.append(col)
        return moves

    def minimax(self, curr_player: BoardPlayers, depth: int):
        
        # terminal states
        if self.board.has_won(self.player):
            return 100
        elif self.board.has_won(self.player.switch_players()):
            return 100
        elif self.board.is_drawn():
            return 0
        elif depth == 0:
            return 0
        
        if curr_player == self.player:
            max_score = -float("inf")

            for move in self.available_moves():

                move_result = self.minimax(curr_player.switch_players(), depth - 1)
                max_score = max(max_score, move_result)
            return max_score
        else:
            min_score = -float("inf")

            for move in self.available_moves():

                move_result = self.minimax(curr_player.switch_players(), depth - 1)
                min_score = min(min_score, move_result)
            return min_score


if __name__ == "__main__":
    board = Board()
    board.drop_piece(1, BoardPlayers.RED)
    game_ai = Connect4AI(board, 50, BoardPlayers.YELLOW)


from game import Board, BoardPlayers, GameState
from enum import Enum
import random

class GameAIStrength(Enum):
    RANDOM = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    MASTER = 5

class Connect4AI:

    def __init__(self, board: Board, player: BoardPlayers, strength: GameAIStrength = GameAIStrength.RANDOM):
        self.board = board
        self.player = player
        self.strength = strength

    def find_best_move(self) -> int:
        """Finds the best move based on the state of the board.

        Returns: the column index [1, 7] of the best move

        Asserts the game has not already ended
        """
        
        assert self.board.get_game_state() != GameState.DRAWN and self.board.get_game_state() != GameState.WON, f"expected the game to not be over: {self.board.get_game_state()}"
        print("THINKING ...")
        if self.strength == GameAIStrength.RANDOM:
            return self.employ_random_strategy()
        elif self.strength == GameAIStrength.EASY:
            print("USING EASY STRATEGY")
            return self.employ_easy_strategy()
        elif self.strength == GameAIStrength.MEDIUM:
            pass
        elif self.strength == GameAIStrength.HARD:
            pass
        elif self.strength == GameAIStrength.MASTER:
            pass
        else:
            assert False, "game strength not found"
    
    def employ_random_strategy(self) -> int:
        moves = self.available_moves()
        assert moves, "there are no possible moves"
        return random.choice(moves)
    
    def employ_easy_strategy(self) -> int:
        best_move, score = self.minimax(self.player, depth = 3)
        # if score == 0: best_move = self.employ_random_strategy()
        print(best_move, score)
        return best_move
    
    def employ_medium_strategy(self) -> int:
        best_move, score = self.minimax(self.player, depth = 5)
        if score == 0: best_move = self.employ_random_strategy()
        # print(best_move, score)
        return best_move
    
    def employ_hard_strategy(self) -> int:
        best_move, score = self.minimax(self.player, depth = 10)
        # print(best_move, score)
        return best_move
    
    def employ_master_strategy(self) -> int:
        best_move, score = self.minimax(self.player, depth = 25)
        # print(best_move, score)
        return best_move
    
    def set_strength(self, strength: GameAIStrength):
        self.strength = strength

    def get_strength(self):
        return self.strength
    
    def available_moves(self) -> int:
        moves = []
        for col in range(1, self.board.NUM_COLS + 1):
            if self.board.is_column_open(col):
                moves.append(col)
        return moves

    def minimax(self, curr_player: BoardPlayers, depth: int):
        
        # terminal states
        if self.board.get_game_state() == GameState.WON:
            return (None, -100) if self.player == curr_player else (None, 100)
        elif self.board.get_game_state() == GameState.DRAWN:
            return None, 0
        elif depth == 0:
            return None, 0
        
        best_moves = []
        if curr_player == self.player:
            best_score = -float("inf")

            for move in self.available_moves():

                self.board.drop_piece(move, curr_player)
                _, score = self.minimax(curr_player.switch_players(), depth - 1)
                assert self.board.undo_last_move(), f"expected to be able to undo last move: {move} {self.player}"
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)
        
        else:
            best_score = float("inf")

            for move in self.available_moves():

                self.board.drop_piece(move, curr_player)
                _, score = self.minimax(curr_player.switch_players(), depth - 1)
                assert self.board.undo_last_move(), f"expected to be able to undo last move: {move} {self.player}"
                if score < best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

        best_move = random.choice(best_moves)
        return best_move, best_score


if __name__ == "__main__":
    board = Board()
    board.drop_piece(1, BoardPlayers.RED)
    game_ai = Connect4AI(board, 50, BoardPlayers.YELLOW)


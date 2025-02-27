from game import Board, BoardPlayers, GameState
from enum import Enum
from typing import Callable
import math
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
        self.num_of_moves = 0

    def find_best_move(self) -> int:
        """Finds the best move based on the state of the board.

        Returns: the column index [1, 7] of the best move

        Asserts the game has not already ended
        """
        
        assert self.board.get_game_state() != GameState.DRAWN and self.board.get_game_state() != GameState.WON, f"expected the game to not be over: {self.board.get_game_state()}"
        self.num_of_moves += 1
        print("THINKING ...")
        if self.strength == GameAIStrength.RANDOM:
            return self.employ_random_strategy()
        elif self.strength == GameAIStrength.EASY:
            print("USING EASY STRATEGY")
            return self.employ_easy_strategy()
        elif self.strength == GameAIStrength.MEDIUM:
            print("USING MEDIUM STRATEGY")
            return self.employ_medium_strategy()
        elif self.strength == GameAIStrength.HARD:
            print("USING HARD STRATEGY")
            return self.employ_hard_strategy()
        elif self.strength == GameAIStrength.MASTER:
            return self.employ_master_strategy()
        else:
            assert False, "game strength not found"
    
    def employ_random_strategy(self) -> int:
        moves = self.available_moves()
        assert moves, "there are no possible moves"
        return random.choice(moves)
    
    def employ_easy_strategy(self) -> int:
        best_move, score = self.minimax(self.player, depth = 3)
        print(best_move, score)
        return best_move
    
    def employ_medium_strategy(self) -> int:
        best_move, score = self.minimax(self.player, depth = 5)
        print(best_move, score)
        return best_move
    
    def identify_winning_moves(self, player):
        winning_moves = []
        for col in range(1, self.board.NUM_COLS + 1):
            if self.board.is_column_open(col):
                self.board.drop_piece(col, player)
                if self.board.get_game_state() == GameState.WON:
                    winning_moves.append(col)
                self.board.undo_last_move()
        return winning_moves
    
    def employ_hard_strategy(self) -> int:
        def strategy(moves):
            # block opponent winning moves first
            opponent_winning_moves = self.identify_winning_moves(self.player.switch_players())
            if opponent_winning_moves:
                return random.choice(opponent_winning_moves)
            
            # prefer center moves
            else:
                return min(moves, key=lambda move: abs(4-move))

        k = 0.2
        max_depth = 10
        depth = int((max_depth)/(1 + math.e ** -(k * self.num_of_moves)))

        print("starting depth", depth)
        best_move, score = self.minimax(self.player, depth, move_func=strategy)
        print(best_move, score)
        return best_move
    
    def employ_master_strategy(self) -> int:
        def strategy(moves):
            # block opponent winning moves first

            # prefer center moves

            # prefer moves that create offense
                # 2x2 square
                # 3 in a row
            pass
        best_move, score = self.minimax(self.player, depth = 41)
        print(best_move, score)
        return best_move
    
    def set_strength(self, strength: GameAIStrength):
        self.strength = strength

    def get_strength(self):
        return self.strength
    
    def available_moves(self, sort_func: Callable[[int], int] = lambda move: -abs(4-move)) -> int:
        moves = []
        for col in range(1, self.board.NUM_COLS + 1):
            if self.board.is_column_open(col):
                moves.append(col)
        moves.sort(key=sort_func, reverse=True)
        return moves

    def minimax(
            self, 
            curr_player: BoardPlayers, 
            depth: int, 
            alpha: int = -float("inf"),
            beta: int = float("inf"),
            move_func: Callable[[list[int]], int] = random.choice
            ):
        
        # print(depth)
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
                _, score = self.minimax(curr_player.switch_players(), depth - 1, alpha, beta, move_func)
                assert self.board.undo_last_move(), f"expected to be able to undo last move: {move} {self.player}"
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

                # pruning
                if best_score > beta:
                    break
                alpha = max(alpha, best_score)
        
        else:
            best_score = float("inf")

            for move in self.available_moves():

                self.board.drop_piece(move, curr_player)
                _, score = self.minimax(curr_player.switch_players(), depth - 1, alpha, beta, move_func)
                assert self.board.undo_last_move(), f"expected to be able to undo last move: {move} {self.player}"
                if score < best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)

                if best_score < alpha:
                    break
                beta = min(beta, best_score)

        assert best_moves, "expected to be able to find a move to play"
        # print("best options", best_moves)
        best_move = move_func(best_moves)
        # print("after", best_move)
        return best_move, best_score


if __name__ == "__main__":
    board = Board()
    board.drop_piece(1, BoardPlayers.RED)
    game_ai = Connect4AI(board, 50, BoardPlayers.YELLOW)


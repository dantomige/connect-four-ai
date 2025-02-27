from enum import Enum
from game import Board, BoardPlayers, GameState
from game_ai import GameAIStrength, Connect4AI
import random

if __name__ == "__main__":
    print("WELCOME TO CONNECT FOUR.")
    print(f"THE FIRST PLAYER HAS PIECE {BoardPlayers.RED}.")
    print(f"THE SECOND PLAYER HAS PIECE {BoardPlayers.YELLOW}.")

    strength_index = int(input(" * EASY: 0\n * MEDIUM: 1\n * HARD: 2\n * MASTER: 3\nPlease input your desired difficulty (type a number): "))

    board = Board()
    player = BoardPlayers.RED
    ai_player = BoardPlayers.YELLOW
    strength_options = [GameAIStrength.EASY, GameAIStrength.MEDIUM, GameAIStrength.HARD, GameAIStrength.MASTER]
    game_ai = Connect4AI(board, ai_player, strength=strength_options[strength_index])

    while True:
        print("Here is the current board")
        print(board)
        player_move = int(input("Select a column to drop a piece in [1, 7]: "))
        game_state = board.drop_piece(player_move, player)
        if game_state == GameState.WON:
            print("Player one won!")
            break
        elif game_state == GameState.DRAWN:
            print("The game ended in a draw")
            break

        ai_move = game_ai.find_best_move()
        game_state = board.drop_piece(ai_move, ai_player)
        print(f"Player two dropped in column {ai_move}.")
        if game_state == GameState.WON:
            print("Player two won!")
            break
        elif game_state == GameState.DRAWN:
            print("The game ended in a draw")
            break

    print("FINAL BOARD: ")
    print(board)

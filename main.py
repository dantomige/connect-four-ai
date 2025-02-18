from enum import Enum
from game import Board, BoardPlayers, GameState
import random

if __name__ == "__main__":
    print("WELCOME TO CONNECT FOUR.")
    print(f"THE FIRST PLAYER HAS PIECE {BoardPlayers.RED}.")
    print(f"THE SECOND PLAYER HAS PIECE {BoardPlayers.YELLOW}.")

    board = Board()
    curr_player = BoardPlayers.RED

    while True:
        print("Here is the current board")
        print(board)
        index = int(input("Select a column to drop a piece in [1, 7]: "))

        game_state = board.drop_piece(index, curr_player)
        if game_state == GameState.WON:
            print("Player one won!")
            break
        elif game_state == GameState.DRAWN:
            print("The game ended in a draw")
            break
        curr_player = BoardPlayers.switch_players(curr_player)

        player_two_move = random.randint(1, board.NUM_COLS)
        game_state = board.drop_piece(player_two_move, curr_player)
        print(f"Player two dropped in column {player_two_move}.")
        if game_state == GameState.WON:
            print("Player two won!")
            break
        elif game_state == GameState.DRAWN:
            print("The game ended in a draw")
            break
        curr_player = BoardPlayers.switch_players(curr_player)

    print("FINAL BOARD: ")
    print(board)

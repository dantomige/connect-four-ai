from enum import Enum
from game import Board, BoardPlayers
import random

if __name__ == "__main__":
    print("WELCOME TO CONNECT FOUR.")
    print(f"THE FIRST PLAYER HAS PIECE {BoardPlayers.RED}.")
    print(f"THE SECOND PLAYER HAS PIECE {BoardPlayers.YELLOW}.")

    board = Board()
    PLAYER_ONE = BoardPlayers.RED
    PLAYER_TWO = BoardPlayers.YELLOW
    winner = None

    while True:
        print("Here is the current board")
        print(board)
        index = int(input("Select a column to drop a piece in [1, 7]: "))
        board.drop_piece(index, PLAYER_ONE)

        if board.has_won(PLAYER_ONE):
            winner = PLAYER_ONE
            break
        elif board.is_drawn():
            break
        
        player_two_move = random.randint(1, board.NUM_COLS)
        board.drop_piece(player_two_move, PLAYER_TWO)
        print(f"Player two dropped in column {player_two_move}.")

        if board.has_won(PLAYER_TWO):
            winner = PLAYER_TWO
            break
        elif board.is_drawn():
            break

    print("FINAL BOARD: ")
    print(board)
    if winner is None:
        print("The game ended in a draw")
    elif winner == PLAYER_ONE:
        print("Player one won!")
    else:
        print("Player two won!")

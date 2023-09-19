from classes import *


"""
Pieces are represented by a letter

Board position reference:
X -------------
Y    [0, 1, 2, 3, 4, 5, 6, 7],
|    [1, 0, 0, 0, 0, 0, 0, 0],
|    [2, 0, 0, 0, 0, 0, 0, 0],
|    [3, 0, 0, 0, 0, 0, 0, 0],
|    [4, 0, 0, 0, 0, 0, 0, 0],
|    [5, 0, 0, 0, 0, 0, 0, 0],
|    [6, 0, 0, 0, 0, 0, 0, 0],
|    [7, 0, 0, 0, 0, 0, 0, 0]


accessing a tile:   board[Y][X] => piece
"""

def print_board(board):
    print("    0  1  2  3  4  5  6  7")
    for i, row in enumerate(board):
        print(i, end="  ")
        for j in row:
            print(j, end=" ")
        print()
    print()

def add_piece(board, piece):
    board[piece.ypos][piece.xpos] = piece

def piece_testbench(board,piece):       #adds a given piece to the board at location. Board is printed, and possible captures and moves are printed out
    add_piece(board,piece)
    print_board(board)
    piece.find_poss_moves()
    print(piece.poss_captures)
    print(piece.poss_moves)


"""
White pawns (from bottom)
"""
PW0 = Pawn(0, 0, 6, board)
add_piece (board, PW0)

PW1 = Pawn(0, 1, 6, board)
add_piece (board, PW1)

PW2 = Pawn(0, 2, 6, board)
add_piece (board, PW2)

PW3 = Pawn(0, 3, 6, board)
add_piece (board, PW3)

PW5 = Pawn(0, 5, 6, board)
add_piece (board, PW5)

PW6 = Pawn(0, 6, 6, board)
add_piece (board, PW6)

PW7 = Pawn(0, 7, 6, board)
add_piece (board, PW7)


RW0 = Rook(0, 3, 4, board)

"""
Black pawns (from top)
"""

BP0 = Pawn (1,4,4,board)
BP1 = Pawn (1,2,4,board)
BP2 = Pawn (1,3,5,board)
BP3 = Pawn (1,3,3,board)
add_piece (board, BP1)
add_piece (board, BP3)

"""
Testing code
"""


bishop = Bishop (1,5,5,board)
queen = Queen(0,3,4,board)
king = King(0,3,4,board)

piece_testbench(board,king)
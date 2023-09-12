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
    for row in board:
        for cell in row:
            print(cell, end=" ")
        print()

def add_piece(board, piece):
    board[piece.ypos][piece.xpos] = piece

def piece_testbench(board,piece):
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

PW4 = Pawn(0, 4, 6, board)
add_piece (board, PW4)

PW5 = Pawn(0, 5, 6, board)
add_piece (board, PW5)

PW6 = Pawn(0, 6, 6, board)
add_piece (board, PW6)
PW7 = Pawn(0, 7, 6, board)
add_piece (board, PW7)

"""
Black pawns (from top)
"""
PB0 = Pawn(1, 1, 4, board)
PB0.has_moved = True
add_piece (board,PB0)
print_board(board)

piece_testbench(board,PB0)
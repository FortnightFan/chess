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

board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

def print_board(board):
    for row in board:
        for cell in row:
            if cell == 0:
                print(".", end=" ")
            else:
                print(cell, end=" ")
        print()

def add_piece(board, piece):
    board[piece.ypos][piece.xpos] = piece

PW0 = Pawn(0, 0, 5, board)
PW1 = Pawn(0, 1, 6, board)
PW2 = Pawn(0, 2, 6, board)
PW3 = Pawn(0, 3, 6, board)
PW4 = Pawn(0, 4, 6, board)
PW5 = Pawn(0, 5, 6, board)
PW6 = Pawn(0, 6, 6, board)
PW7 = Pawn(0, 7, 6, board)

PB0 = Pawn(1, 0, 1, board)
#White pieces
add_piece (board, PW0)
add_piece (board, PW1)
add_piece (board, PW2)
add_piece (board, PW3)
add_piece (board, PW4)
add_piece (board, PW5)
add_piece (board, PW6)
add_piece (board, PW7)

#Black pieces
add_piece (board,PB0)

RW0 = Rook(0,4,0, board)

add_piece (board,RW0)

print_board(board)
RW0.possible_moves()
print(RW0.poss_moves)
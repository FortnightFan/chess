from chess import *

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

def clear_board():
    global board
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
    global tile

    class Tile (Piece):
        def __str__ (self):
            return (f"__")

    tile = Tile(2,0,0,board)
    for i in range (0,8):
        for j in range (0,8):
            board[i][j] = tile


def white_pin_testbench():        #expected output: Black rook can only move in 3 col, or capture the rook.    
    add_piece(board, King(1,3,0,board))  #adds piece to board with x,y coords
    add_piece(board, Rook(0,3,7,board))  #adds piece to board with x,y coords
    add_piece(board, Pawn(0,2,4,board))  #adds piece to board with x,y coords

    RB = Rook (1,3,4,board)
    add_piece(board, RB)  #adds piece to board with x,y coords

    find_all_poss_moves(board)

    check_pin(board, RB) #removes possible moves that will put own king in check
    piece_testbench(board, RB) #adds piece to board, prints board, all possible moves.

    clear_all_lists()
    clear_board()

def black_pin_testbench(): #expected output: White rook can only move in col 3, or capture white rook
    add_piece(board, King(0,3,0,board))
    add_piece(board, Rook(1,3,7,board))
    add_piece(board, Pawn(1,2,4,board))
 
    RW = Rook(0,3,4,board)
    add_piece(board, RW)

    find_all_poss_moves(board)

    check_pin(board, RW)
    piece_testbench(board, RW)

    clear_all_lists()

print("BLACK ROOK TEST")
white_pin_testbench()
#print_board(board) #TEST TO MAKE SURE BOARD IS CLEARED
print("\nWHITE ROOK TEST")
black_pin_testbench() #INCORRECT OUTPUT. CAPTURES PAWN ONLY



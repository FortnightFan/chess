from chess import *
import code
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

def clear_board(): #call to clear board
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
    for i in range (0,8):
        for j in range (0,8):
            board[i][j] = tile

def white_rook_pin_testbench(): #expected output: Black rook can only move in 3 col, or capture the rook.    
    add_piece(board, King(1,3,0,board, 0))  #adds piece to board with x,y coords
    add_piece(board, Rook(0,3,7,board, 0))  #adds piece to board with x,y coords
    add_piece(board, Pawn(0,2,4,board, 0))  #adds piece to board with x,y coords

    RB = Rook (1,3,4,board, 0)
    add_piece(board, RB)  #adds piece to board with x,y coords

    init(board)
    find_all_poss_moves(board)

    check_pin(board, RB) #removes possible moves that will put own king in check
    piece_testbench(board, RB) #adds piece to board, prints board, all possible moves.

    clear_all_lists(board)
    clear_board()

def white_rook_diff_initial_pin_testbench(): #expected output: Black rook can only move in col 6, or capture white rook.
    add_piece(board, King(1,6,0,board, 0))  #adds piece to board with x,y coords
    add_piece(board, Rook(0,6,7,board, 0))  #adds piece to board with x,y coords
    add_piece(board, Pawn(0,5,4,board, 0))  #adds piece to board with x,y coords

    RB = Rook (1,6,4,board, 0)
    add_piece(board, RB)  #adds piece to board with x,y coords

    init(board)
    find_all_poss_moves(board)

    check_pin(board, RB) #removes possible moves that will put own king in check
    piece_testbench(board, RB) #adds piece to board, prints board, all possible moves.

    clear_all_lists(board)
    clear_board()

def black_rook_pin_testbench(): #expected output: White rook can only move in col 3, or capture white rook
    add_piece(board, King(0,3,0,board, 0))
    add_piece(board, Rook(1,3,7,board, 0))
    add_piece(board, Pawn(1,2,4,board, 0))
 
    RW = Rook(0,3,4,board, 0)
    add_piece(board, RW)

    init(board)
    find_all_poss_moves(board)

    check_pin(board, RW)
    piece_testbench(board, RW)

    clear_all_lists(board)
    clear_board()

def stalemate_testbench():  #expected output: White has no legal moves, therefore 'True' should be printed out
    king =  King(0,4,7,board, False)
    add_piece(board,king)
    init(board)

    add_piece(board, Horse(1,3,7,board))
    add_piece(board, Horse(1,5,7,board))
    add_piece(board, Horse(1,3,6,board))
    add_piece(board, Horse(1,4,6,board))
    add_piece(board, Horse(1,5,6,board))

    add_piece(board, Queen(1,2,6,board))
    add_piece(board, Queen(1,6,6,board))
    add_piece(board, Queen(1,4,5,board))
    add_piece(board, Pawn(0,0,5,board))
    print_board(board)
    find_all_poss_moves(board)
    legal_king_moves(board, king)

    print(king.poss_moves,king.poss_captures)
    print(is_white_stalemate(board))

def checkmate_testbench_white():
    add_piece(board,board[white_king_pos[1]][white_king_pos[0]])
    init(board)

    add_piece(board, Queen(1,3,7,board))
    add_piece(board, Queen(1,4,6,board))

    pawn = Pawn(0,0,6,board)
    add_piece(board, pawn)

    print_board(board)

    find_all_poss_moves(board)

    print(is_white_checkmate(board))

# print("BLACK ROOK TEST")
# white_rook_pin_testbench()
# print("\nBLACK ROOK DIFFERENT INITIAL LOCATION TEST")
#white_rook_diff_initial_pin_testbench()#INCORRECT OUTPUT. CAPTURES PAWN ONLY
# print("\nWHITE ROOK TEST")
# black_rook_pin_testbench() #INCORRECT OUTPUT. CAPTURES PAWN ONLY


# stalemate_testbench()

def promotions_testbench():
    fen_to_board("rnb2bnr/pp1P1kp1/2p2p1p/4p3/4P3/8/PPP2PPP/R1BQKBNR w KQ - 0 11")
    move_piece(board, board[1][3], (3,0))
    check_promotions(board, 0)
    print_board(board)

def live_shell_testbench():
    fen_to_board("4B3/8/4n3/1p6/2b5/k1K5/8/8 w - - 0 0")
    namespace = locals()
    namespace.update(globals())
    code.interact(local=namespace)
    

def misc_testbench():
    fen_to_board("4K3/8/4kp2/4p3/6P1/1p3P2/8/8 w - - 0 0 ")
    print_board(board)
    find_all_poss_moves(board)
    legal_king_moves(board)
    print(is_black_stalemate(board))

    
misc_testbench()
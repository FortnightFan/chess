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

def print_board(board):         #prints status of the board to terminal. 
    print("    0  1  2  3  4  5  6  7")
    for i, row in enumerate(board):
        print(i, end="  ")
        for j in row:
            print(j, end=" ")
        print()
    print()

def add_piece(board, piece):        #adds piece to board. x,y coords are stored inside object
    board[piece.ypos][piece.xpos] = piece

def move_piece(board, piece, pos):  #moves a piece to tuple pos
    global white_king_pos, black_king_pos

    x, y = piece.xpos, piece.ypos
    piece.xpos, piece.ypos = pos[0], pos[1]
    
    if board[pos[1]][pos[0]] != Tile:
        ret_val = board[pos[1]][pos[0]]
    
    add_piece(board, piece)
    board[y][x] = tile
    if isinstance(piece, King):
        piece.has_moved == True
        if piece.color == 0:
            white_king_pos = (piece.xpos, piece.ypos)
        elif piece.color == 1:
            black_king_pos = (piece.xpos, piece.ypos)
    elif isinstance(piece,Pawn) or isinstance(piece,Rook):
        piece.has_moved == True
    
    return ret_val
def find_all_poss_moves(board):
    for row in range (0,8):
        for col in range (0,8):
            board[col][row].find_poss_moves()

def clear_all_lists(board):
    for row in range(0,8):
        for col in range(0,8):
            board[row][col].clear_lists()
            
def piece_testbench(board,piece):       #adds a given piece to the board at location. Board is printed, and possible captures and moves are printed out
    add_piece(board,piece)
    print_board(board)
    print(piece.poss_captures)
    print(piece.poss_moves)

def legal_king_moves(board,king):      #removes illegal king moves
    x,y = king.xpos,king.ypos
    moves_to_remove = []
    captures_to_remove = []
    
    if (king.color == 0):
        for i in range(len(king.poss_moves)):
            move_piece(board,king,king.poss_moves[i])
            if (is_white_in_check(board) == True):
                moves_to_remove.append(i)
            move_piece(board,king, (x,y))
            
        for i in range(len(king.poss_captures)):
            temp = board[king.poss_captures[i][1]][king.poss_captures[i][0]]
            move_piece(board, king, king.poss_captures[i])
            if (is_white_in_check(board) == True):
                captures_to_remove.append(i)     
            move_piece(board, king, (x, y))
            add_piece (board, temp)            

    elif (king.color == 1):
        for i in range(len(king.poss_moves)):
            move_piece(board,king,king.poss_moves[i])
            if (is_black_in_check(board) == True):
                moves_to_remove.append(i)
            move_piece(board,king, (x,y))

        for i in range(len(king.poss_captures)):
            temp = board[king.poss_captures[i][1]][king.poss_captures[i][0]]
            move_piece(board, king, king.poss_captures[i])
            if (is_black_in_check(board) == True):
                captures_to_remove.append(i)     
            move_piece(board, king, (x, y))
            add_piece (board, temp)    
                            
    for index in reversed(moves_to_remove):
            king.poss_moves.pop(index)
    if not captures_to_remove == []:
        for index in reversed(captures_to_remove):
            king.poss_captures.pop(index)
                
                
def check_pin(board, piece):    #removes possible moves that will cause their own king to be checked. 
    x, y = piece.xpos, piece.ypos
    
    moves_to_remove = []
    captures_to_remove = []
    if (piece.color == 0):
        for i in range(len(piece.poss_moves)):
            move_piece(board, piece, piece.poss_moves[i])
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 1:
                        board[row][col].find_poss_moves()
                        if white_king_pos in board[row][col].poss_captures:
                            moves_to_remove.append(i)
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))

        for i in range(len(piece.poss_captures)):
            temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
            move_piece(board, piece, piece.poss_captures[i])
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 1:
                        board[row][col].find_poss_moves()
                        if white_king_pos in board[row][col].poss_captures:
                            captures_to_remove.append(i)
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))
            add_piece (board, temp)

    elif (piece.color == 1):
        for i in range(len(piece.poss_moves)):
            move_piece(board, piece, piece.poss_moves[i])
            
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 0:
                        board[row][col].find_poss_moves()
                        if black_king_pos in board[row][col].poss_captures:
                            moves_to_remove.append(i) 
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))

        for i in range(len(piece.poss_captures)):
            temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
            move_piece(board, piece, piece.poss_captures[i])
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 0:
                        board[row][col].find_poss_moves()
                        if black_king_pos in board[row][col].poss_captures:
                            captures_to_remove.append(i)
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))
            add_piece (board, temp)

    for index in reversed(moves_to_remove):
        piece.poss_moves.pop(index)
    if not captures_to_remove == []:
        for index in reversed(captures_to_remove):
            piece.poss_captures.pop(index)
        
def can_white_castle(board):    #returns a bool that is true if the white king can castle
    king = board[white_king_pos[1]][white_king_pos[0]]
    if king.has_moved == True:
        return False
    else:   #check short side
        if (board[7][2] == Tile and board[7][1] == Tile and isinstance(board[7][0], Rook)):
            if (board[7][0].has_moved == False):
                rook = move_piece(board, king, (0,7))
                move_piece(board, rook, (3,7))
                return True
        return False

def can_black_castle(board):    #returns a bool that is true if the black king can castle
    king = board[black_king_pos[1]][black_king_pos[0]]    
    if king.has_moved == True:
        return False
    else:   #check short side
        if (board[0][2] == Tile and board[0][1] == Tile and isinstance(board[0][0], Rook)):
            if (board[0][0].has_moved == False):
                return True
        return False
"""
Functions for when king is in check-state
"""    
def is_black_in_check(board):  #returns a bool, True if in check. 
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col].color == 0:
                board[row][col].find_poss_moves()
                if black_king_pos in board[row][col].poss_captures:
                    board[row][col].clear_lists()
                    return True
                board[row][col].clear_lists()
    return False

def is_white_in_check(board):  #returns a bool, True if in check. 
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col].color == 1:
                board[row][col].find_poss_moves()
                if white_king_pos in board[row][col].poss_captures:
                    board[row][col].clear_lists()
                    return True
                board[row][col].clear_lists()
    return False

def can_white_block(board): #called when white is in check. Corrects piece moves so they have to protect king
    return_val = False
    moves_to_remove = []
    captures_to_remove = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col].color == 0 and not(isinstance(board[row][col], King)):
                piece = board[row][col]
                piece.find_poss_moves()
                for i in range (len(piece.poss_moves)):
                    move_piece(board, piece, piece.poss_moves[i])
                    if is_white_in_check(board) == True:
                        moves_to_remove.append(i)
                        return_val = True
                    move_piece(board, piece, (col,row))
                for index in reversed(moves_to_remove):
                    piece.poss_moves.pop(index)
                moves_to_remove = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col].color == 0 and not(isinstance(board[row][col], King)):
                piece = board[row][col]
                for i in range (len(piece.poss_captures)):
                    temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
                    move_piece(board, piece, piece.poss_captures[i])
                    if is_white_in_check(board) == True:
                        captures_to_remove.append(i)
                        return_val = True
                    move_piece(board, piece, (col,row))
                    add_piece(board, temp)
                if not captures_to_remove == []:
                    for index in reversed(captures_to_remove):
                        piece.poss_captures.pop(index)
                captures_to_remove = []
    return return_val
                
def can_black_block(board): #called when black is in check. Corrects piece moves so they have to protect king. Returns true/false if there's a move to protect
    moves_to_remove = []
    captures_to_remove = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col].color == 1 and not(isinstance(board[row][col], King)):
                piece = board[row][col]
                piece.find_poss_moves()
                for i in range (len(piece.poss_moves)):
                    move_piece(board, piece, piece.poss_moves[i])
                    if is_black_in_check(board) == True:
                        moves_to_remove.append(i)
                    move_piece(board, piece, (col,row))
                for index in reversed(moves_to_remove):
                    piece.poss_moves.pop(index)
                moves_to_remove = []
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col].color == 1 and not(isinstance(board[row][col], King)):
                piece = board[row][col]
                for i in range (len(piece.poss_captures)):
                    temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
                    move_piece(board, piece, piece.poss_captures[i])
                    if is_black_in_check(board) == True:
                        captures_to_remove.append(i)
                    move_piece(board, piece, (col,row))
                    add_piece(board, temp)
                if not captures_to_remove == []:
                    for index in reversed(captures_to_remove):
                        piece.poss_captures.pop(index)
                captures_to_remove = []
    return False            
    
def is_white_checkmate(board):
    if is_white_in_check(board) == True:
        king = board[white_king_pos[1]][white_king_pos[0]]
        king.find_poss_moves()
        legal_king_moves(board, king)
        if king.poss_moves == [] and king.poss_captures == [] and not(can_white_block(board)):
            return True
    return False

def is_black_checkmate(board):
    if is_black_in_check(board) == True:
        king = board[black_king_pos[1]][black_king_pos[0]]
        king.find_poss_moves()
        legal_king_moves(board, king)
        if king.poss_moves == [] and king.poss_captures == [] and not(can_black_block(board)):
            return True
    return False
"""
Testing notes:

    Before looking at a piece, always run find_all_poss_moves().
    After testing a piece, always run clear_all_lists().
    
    To set up a board, reference the piece class in classes.py to set up parameters.
    Use the add_piece(board, PIECE) function to update the global board variable.
    
    piece_testbench(board, PIECE) will print out the current board status, and print out all possible moves/captures of a certain piece. 
    
    check_pin(board, PIECE) will modify pieces so they cannot move in a way that endangers the king piece. Always run this after PIECE.find_poss_moves.
"""
    
def add_white_pieces():
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
    
    RW1 = Rook (0,0,7, board)
    RW2 = Rook (0,7,7, board)
    add_piece (board, RW1)
    add_piece (board, RW2)
    
    BW1 = Bishop (0,1,7, board)
    BW2 = Bishop (0,6,7, board)
    add_piece (board, BW1)
    add_piece (board, BW2)
    
    KW = King (0,3,7, board)
    add_piece (board, KW)
    
    QW = Queen (0,4,7, board)
    add_piece (board, QW)
    
    HW1 = Horse (0,2,7, board)
    add_piece (board, HW1)
    
    HW2 = Horse (0,5,7, board)
    add_piece (board, HW2)

def add_black_pieces():
    BP0 = Pawn (1,0,1,board)
    add_piece (board, BP0)

    BP1 = Pawn (1,1,1,board)
    add_piece (board, BP1)

    BP2 = Pawn (1,2,1,board)
    add_piece (board, BP2)

    BP3 = Pawn (1,3,1,board)
    add_piece (board, BP3)

    BP4 = Pawn (1,4,1,board)
    add_piece (board, BP4)

    BP5 = Pawn (1,5,1,board)
    add_piece (board, BP5)

    BP6 = Pawn (1,6,1,board)
    add_piece (board, BP6)

    BP7 = Pawn (1,7,1,board)
    add_piece (board, BP7)

    RW1 = Rook (1,0,0, board)
    RW2 = Rook (1,7,0, board)
    add_piece (board, RW1)
    add_piece (board, RW2)
    
    BW1 = Bishop (1,1,0, board)
    BW2 = Bishop (1,6,0, board)
    add_piece (board, BW1)
    add_piece (board, BW2)
    
    KW = King (1,3,0, board)
    add_piece (board, KW)
    
    QW = Queen (1,4,0, board)
    add_piece (board, QW)
    
    HW1 = Horse (1,2,0, board)
    add_piece (board, HW1)
    
    HW2 = Horse (1,5,0, board)
    add_piece (board, HW2)

def init(board):
    global white_king_pos, black_king_pos
    for row in range(0,8):
        for col in range(0,8):
            piece = board[row][col]
            if isinstance(piece, King):
                if piece.color == 0:
                    white_king_pos = (piece.xpos,piece.ypos)
                elif piece.color == 1:
                    black_king_pos = (piece.xpos,piece.ypos)
                    

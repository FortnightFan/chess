from chess import *
from classes import *
import time
from stockfish import Stockfish
import os
import platform

system = platform.system()
if (system == "Windows"):
    script_directory = os.path.dirname(os.path.abspath(__name__))
    stockfish_path = os.path.join(script_directory, "stockfish-windows-x86-64-avx2.exe")   
    stockfish = Stockfish(path=stockfish_path)

elif (system == "Linux"):
    stockfish = Stockfish('stockfish')
else:
    print("ERROR")
    exit()

def fish_init():
    stockfish.set_depth(10)
    stockfish.update_engine_parameters({"Hash": 32, "Skill Level": 15})

def move_to_tuple(color, move):    #returns piece location, and piece move location.
    ret1 = 0
    ret2 = 0
    ret3 = 0
    ret4 = 0
    
    if isinstance(move, str) and len(move) >= 4 and 'a' <= move[0] <= 'h' and 'a' <= move[2] <= 'h' and '1' <= move[1] <= '8' and '1' <= move[3] <= '8':   
        ret1 = ord(move[0])-ord('a')
        ret3 = ord(move[2])-ord('a')
        ret2 = int(move[1])
        ret4 = int(move[3])
        piece = board[8-ret2][ret1]
        if isinstance(piece,Tile):
            return False
    else:
        return False
    return (ret1,8-ret2), (ret3,8-ret4)

def board_to_fen(board, color):
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            qrook = True
        else:
            qrook = False
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            krook = True
        else:
            krook = False
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            Qrook = True
        else:
            Qrook = False
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            Krook = True
        else:
            Krook = False

    str_ret = ""
    temp = 0
    for i in range (0,8):
        for j in range (0,8):
            piece = board[i][j]
            if isinstance(piece, Tile):
                temp += 1

            if isinstance(piece, Pawn):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'p'
                elif piece.color == 0:
                    str_ret += 'P'

            elif isinstance(piece, Horse):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'n'
                elif piece.color == 0:
                    str_ret += 'N'      

            elif isinstance(piece, Bishop):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'b'
                elif piece.color == 0:
                    str_ret += 'B'

            elif isinstance(piece, Rook):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'r'
                elif piece.color == 0:
                    str_ret += 'R'      

            elif isinstance(piece, Queen):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'q'
                elif piece.color == 0:
                    str_ret += 'Q'

            elif isinstance(piece, King):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'k'
                elif piece.color == 0:
                    str_ret += 'K'   
        if temp != 0:
            str_ret += str(temp)
            temp = 0
        str_ret += '/'
    str_ret = ''.join(str_ret[:-1])
    if color == 0:
        str_ret += " w "
    elif color == 1:
        str_ret += " b "

    str_ret += "-"
    # king = board[white_king_pos[1]][white_king_pos[0]]
    # if king.has_moved == False:
    #     if Krook == True:
    #        str_ret += 'K'
    #     if Qrook == True:
    #         str_ret += 'Q'

    # king = board[black_king_pos[1]][black_king_pos[0]]
    # if king.has_moved == False:
    #     if krook == True:
    #        str_ret += 'k'
    #     if qrook == True:
    #         str_ret += 'q'

    str_ret += " - 0 0"
    return str_ret

def fen_to_board(fen):
    global black_king_pos
    global white_king_pos
    fen = fen.split("/")
    for i,str  in enumerate (fen): 
        new_j = 0
        for j,char in enumerate(str):
            if i < 8 and new_j < 8:
                if '1' <= char <= '8':
                    val = int(char)-1  
                    for h in range(new_j,val):
                        board[i][h] = tile
                    new_j += val
                elif char == 'r':
                    if (j,i) == (0,7) or (j,i) == (0,0):
                        board[i][new_j] = Rook(1,new_j,i,board,False)
                    else:
                        board[i][new_j] = Rook(1,new_j,i,board,True)
                elif char == 'R':
                    if (j,i) == (7,7) or (j,i) == (7,0):
                        board[i][new_j] = Rook(0,new_j,i,board,False)
                    else:
                        board[i][new_j] = Rook(0,new_j,i,board,True)

                elif char == 'p':
                    board[i][new_j] = Pawn(1,new_j,i,board)
                elif char == 'P':
                    board[i][new_j] = Pawn(0,new_j,i,board)

                elif char == 'n':
                    board[i][new_j] = Horse(1,new_j,i,board)
                elif char == 'N':
                    board[i][new_j] = Horse(0,new_j,i,board)

                elif char == 'b':
                    board[i][new_j] = Bishop(1,new_j,i,board)
                elif char == 'B':
                    board[i][new_j] = Bishop(0,new_j,i,board)
            
                elif char == 'k':
                    if (j,i) != (4,0):
                        board[i][new_j] = King(1,new_j,i,board,True)
                    else:
                        board[i][new_j] = King(1,new_j,i,board,False)
                    black_king_pos = (j,i)
                elif char == 'K':
                    if (j,i) != (4,7):
                        board[i][new_j] = King(0,new_j,i,board,True)
                    else:
                        board[i][new_j] = King(0,new_j,i,board,False)
                    white_king_pos = (new_j,i)

                elif char == 'q':
                    board[i][new_j] = Queen(1,new_j,i,board)
                elif char == 'Q':
                    board[i][new_j] = Queen(0,new_j,i,board)
                new_j += 1
    fen = fen[7].split(" ")
    if fen[1] == 'w':
        return 0
    elif fen[1] == 'b':
        return 1                

def get_best_move(board, color):
    fen = board_to_fen(board, color)
    stockfish.set_fen_position(fen)
    move = stockfish.get_best_move()
    return move, move_to_tuple(color, move)


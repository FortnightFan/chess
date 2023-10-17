from chess import *
from classes import *
import time
from stockfish import Stockfish
import os
import platform

def init():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    stockfish_path = os.path.join(script_directory, "stockfish-ubuntu-x86-64-avx2")
    stockfish = Stockfish(path=stockfish_path)
    stockfish.set_depth(6)
    
def move_to_tuple(color, move):    #returns piece location, and piece move location.
    """
    Currently working for pawn movements. Need help getting other types of movements. 
    """
    ret1 = 0
    ret2 = 0
    ret3 = 0
    ret4 = 0
    
    letter = move[0]
    if 'a' <= letter <= 'h':    #check if it is a pawn move
        ret1 = ord(letter)-ord('a')
        if move[1] == 'x':  #check if its a capture
            ret3 = ord(move[2])-ord('a')
            num = move[3]
            ret4 = 8 - int(num) 
            col = [row[ret1] for row in board]
            for piece in col:
                if isinstance(piece, Pawn):
                    piece.find_poss_moves()
                    if any((ret3, ret4) == poss_move for poss_move in piece.poss_captures):
                        ret2 = piece.ypos
        else:
            ret2 = 8 - int(move[1])
            letter = move[2]
            ret3 = ord(letter)-ord('a') 
            ret4 = 8 - int(move[3])

    elif letter == "K" or letter == "Q" or letter == "R" or letter == "B" or letter == "N": #it is a horse, king,queen,rook, bishop move
        letter = move[1]
        if 'a' <= letter <= 'h':
            ret3 = ord(letter)-ord('a') 
            num = move[3]
            ret4 = 8 - int(num)    
        if letter == 'x':   #incomplete
            return 1
    return (ret1,ret2), (ret3,ret4)



add_piece(board, Pawn(0,3,5,board, False))
add_piece(board, Pawn(1,4,4,board, False))
print_board(board)
print (move_to_tuple(0,"dxe4"))


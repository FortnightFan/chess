from chess import *
"""
Declare all NFC id values and match them to predefined piece objects.
"""


"""
Identify all pieces on board
"""


"""
Create threads to get readings from readers
"""





pawn = Rook(0,0,2,board)
add_piece(board, pawn)
add_piece(board,Pawn(0,0,1,board))
pawn.find_poss_moves()
piece_testbench(board, pawn)

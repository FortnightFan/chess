from chess import *

# add_white_pieces()
# add_black_pieces()
king =  King(0,4,7,board, False)
add_piece(board,king)
init(board)

add_piece(board, Queen(1,3,7,board))
add_piece(board, Queen(1,4,6,board))

pawn = Pawn(0,0,6,board)
add_piece(board, pawn)

print_board(board)

find_all_poss_moves(board)

print(is_white_checkmate(board))

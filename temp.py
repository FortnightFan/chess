import chess


chess.fen_to_board("k7/ppp5/1r4qK/6R1/8/8/5P2/8 w - - 0 1")
chess.print_board(chess.board)





chess.find_all_poss_moves(chess.board)
chess.update_king_pos(chess.board)

print(chess.is_white_checkmate(chess.board))

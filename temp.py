import chess

def chess_piece_logic(piece, color):
    chess.clear_all_lists(chess.board)
    chess.find_all_poss_moves(chess.board)
    chess.update_king_pos(chess.board)
    try:
        chess.legal_king_moves(chess.board, color)
        chess.check_pin(chess.board, piece)
    except Exception as e:
        print(f"ERROR in chess_piece_logic: {e}")
        
chess.fen_to_board("rnbp2Pr/ppp2ppp/4pn2/5b2/8/8/PPPPPPPP/RNBQ1BNR w - - 0 1")

chess.find_all_poss_moves(chess.board)
chess.update_king_pos(chess.board)
print(chess.black_king_pos)
print(chess.is_black_checkmate(chess.board))

chess.print_board(chess.board)
piece = chess.board[0][7]
print(piece)
chess_piece_logic(chess.board[1][4], 1)
print(piece.poss_captures)
chess.clear_all_lists(chess.board)





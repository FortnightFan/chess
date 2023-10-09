Helper functions: 

	print_board(board) : Prints out current status of the board. Pieces are represented by 2 characters: 
				1. Name of Piece (K for king, H for horse...)
				2. Color of Piece (B/W)
				
	move_piece(board, piece, (x,y)) : Moves a piece to the location declared in the tuple. 

	add_white_pieces()/add_black_pieces() : Adds all black/white pieces in starting position to the board. 
	
	find_all_poss_moves(board) : Runs find_poss_moves for all pieces on the board. Only base logic. 

	clear_all_lists() : Clears all poss_moves[] and poss_captures[] for all pieces on the board. 

Game Logic Functions:

	add_piece(board, piece) : Adds a piece to the board from the parameter. Piece needs to be declared with color, x/y positions, etc. 

	piece_testbench(board, piece) : Simulates lifting a piece. Will print out the current board status, and print out the piece's poss_moves[] and poss_captures[]

	legal_king_moves(board, king) : Removes illegal moves inside the king's poss_moves[] and poss_captures[]. 

	check_pin(board, piece) : Removes illegal moves for any given piece that is absolutely pinned. (Own king cannot be in check after a move)
	
	init() : Corrects king position. Call this after adding all the needed pieces. 

  	can_black/white_castle()  : Returns True if the king can correctly castle. False otherwise. 

Check Logic Functions

	is_black_in_check(board)/is_white_in_check : Returns a bool that states True if black/white is in check, or False otherwise.

	can_black_block(board)/can_white_block(board) : Sets all legal moves of a chess position has during a check, besides king. Returns True if there is at least 1 legal move, False otherwise.

	is_black_checkmate(board)/is_white_checkmate(board) : Returns a bool that states True if black/white is in checkmate, or False otherwise. 






GENERAL TESTBENCH PROCESS:

1. Start by declaring and adding all your pieces to the board.
2. Call init() to correct the king position. 
3. Call the find_all_poss_moves(). 
4. Call whatever functions are needed to test. 
5. Call piece_testbench() to print out the logic for a specified piece.
6. Call clear_all_lists() after. 
7. Call clear_board() afterwards. 
8. Observe if the board behavior is as expected. If not, make note of what happens in a comment.

Reference white_rook_pin_testbench() if anything is unclear. 

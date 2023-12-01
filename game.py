from chess import *

def print_board_game(board):
    for i, row in enumerate(board):
        print(8-i, end="  ")
        for j in row:
            print(j, end=" ")
        print()
    print("   A  B  C  D  E  F  G  H")

global state #variable to track state of the game
state = 0
game_over_id = -1

white_ai_switch = False
black_ai_switch = True

def initialize_game():
    global state
    fish_init()
    color = fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 4")
    init(board)

    print_board_game(board)

    print("Game Start!\n")
    if color == 0:
        if white_ai_switch:
            state = 4
        else:
            state = 0
    elif color == 1:
        if black_ai_switch:
            state = 5
        else:
            state = 1
    
def white_move():   
    global state
    global game_over_id

    find_all_poss_moves(board)
    legal_king_moves(board, 0)
    
    if (is_white_stalemate(board)):
        game_over_id = 0
        state = 6
        return
    
    move = input("White's Turn! Enter move:\n")
    while (1):
        move = move_to_tuple(0,move)
        if (move == False):
            print("ERROR: Invalid input. Please try again.")
            move = input("White's Turn! Enter move:\n")
        else:
            piece = board[move[0][1]][move[0][0]]
            check_pin(board,piece)
            if ((move[1] in piece.poss_moves) or (move[1] in piece.poss_captures)) and piece.color == 0:
                break
            else:
                print("ERROR: Piece can't move there. Please try again.")
                move = input("White's Turn! Enter move:\n")
                
    move_piece(board, piece, move[1])

    clear_all_lists(board)
    
    check_promotions(board, 0)

    if (black_ai_switch):
        state = 5
    elif (is_black_in_check(board)):
        state = 3
    else:
        state = 1
    print("\n------------------------------\n")
    print_board_game(board)

def black_move():
    global state
    global game_over_id

    find_all_poss_moves(board)
    legal_king_moves(board, 1)

    if (is_black_stalemate(board)):
        game_over_id = 0
        state = 6
        return
    
    move = input("Black's Turn! Enter move:\n")
    while (1):
        move = move_to_tuple(1,move)
        if (move == False):
            print("ERROR: Invalid input. Please try again.")
            move = input("Black's Turn! Enter move:\n")
        else:
            piece = board[move[0][1]][move[0][0]]
            check_pin(board,piece)
            if ((move[1] in piece.poss_moves) or (move[1] in piece.poss_captures)) and piece.color == 1:
                break
            else:
                print("ERROR: Piece can't move there. Please try again.")
                move = input("Black's Turn! Enter move:\n")

    move_piece(board, piece, move[1])
    clear_all_lists(board)
    
    check_promotions(board, 1)

    if (white_ai_switch):
        state = 4
    elif (is_white_in_check(board)):
        state = 2
    else:
        state = 0
    print("\n------------------------------\n")
    print_board_game(board)

def white_move_check():
    global state
    global game_over_id
    find_all_poss_moves(board)
    val = is_white_checkmate(board)
    if (val == True):
        game_over_id = 2
        state = 6
        return
    else:
        move = input("White is in CHECK: Enter move:\n")
        while(1):
            move = move_to_tuple(0,move)
            if (move == False):
                print("ERROR: Invalid input. Please try again.")
                move = input("White is in CHECK: Enter move:\n")
                move = move_to_tuple(1,move)
            else:
                piece = board[move[0][1]][move[0][0]]
                if (move[1] in piece.poss_moves) or (move[1] in piece.poss_captures) and piece.color == 0:
                    break
                else:
                    print("ERROR: Piece can't move there. Please try again.")
                    move = input("White is in CHECK: Enter move:\n")
        move_piece(board, piece, move[1])
        clear_all_lists(board)
        check_promotions(board, 0)
    if (black_ai_switch):
        state = 5
    elif (is_black_in_check(board)):
        state = 3
    else:
        state = 1
    print("\n------------------------------\n")
    print_board_game(board)

def black_move_check():
    global state
    global game_over_id
    find_all_poss_moves(board)
    val = is_black_checkmate(board)
    if (val == True):
        game_over_id = 2
        state = 6
        return
    else:
        move = input("Black is in CHECK: Enter move:\n")
        while(1):
            move = move_to_tuple(0,move)
            if (move == False):
                print("ERROR: Invalid input. Please try again.")
                move = input("Black is in CHECK: Enter move:\n")
                move = move_to_tuple(1,move)
            else:
                piece = board[move[0][1]][move[0][0]]
                if ((move[1] in piece.poss_moves) or (move[1] in piece.poss_captures)) and piece.color == 1:
                    break
                else:
                    print("ERROR: Piece can't move there. Please try again.")
                    move = input("Black is in CHECK: Enter move:\n")
        move_piece(board, piece, move[1])
        clear_all_lists(board)
        check_promotions(board, 1)

    if (white_ai_switch):
        state = 4
    elif (is_white_in_check(board)):
        state = 2
    else:
        state = 0
    print("\n------------------------------\n")
    print_board_game(board)
    
def white_move_ai():
    global state
    global game_over_id

    find_all_poss_moves(board)
    legal_king_moves(board, 0)

    if is_white_checkmate(board):
        game_over_id = 1
        state = 6
        return   
    
    if is_white_stalemate(board):
        game_over_id = 0
        state = 6
        return
    
    print ("White AI's Turn:")
    move,tup = get_best_move(board, 0)
    if move == None:
        game_over_id = 1
        state = 6
        return
    move_piece(board, board[tup[0][1]][tup[0][0]], tup[1])  
    print (f"White AI moves {move}")
    
    check_promotions(board, 0)

    if (black_ai_switch):
        state = 5
    elif (is_black_in_check(board)):
        state = 3
    else:
        state = 1
        
    clear_all_lists(board)
    print("\n------------------------------\n")
    print_board_game(board)
      
def black_move_ai():
    global state
    global game_over_id
    find_all_poss_moves(board)
    legal_king_moves(board, 1)
    if is_black_checkmate(board):
        game_over_id = 2
        state = 6
        return
    
    if is_black_stalemate(board):
        game_over_id = 0
        state = 6
        return

    print ("Black AI's Turn:")
    move,tup = get_best_move(board, 1)
    if move == None:
        game_over_id = 2
        state = 6
        return
    move_piece(board, board[tup[0][1]][tup[0][0]], tup[1])  
    print (f"Black AI moves {move}")
    
    check_promotions(board, 1)

    if (white_ai_switch):
        state = 4
    elif (is_white_in_check(board)):
        state = 2
    else:
        state = 0
    clear_all_lists(board)
    print("\n------------------------------\n")
    print_board_game(board)
    
def game_over():
    print("Good game!")
    if (game_over_id == 2):
        print ("White wins!")
    elif (game_over_id == 1):
        print ("Black wins!")
    elif (game_over_id == 0):
        print ("Tie!")
    print(board_to_fen(board, 0))
    exit()

initialize_game()

while (1):
    if (state == 0):
        white_move()
    elif (state == 1):
        black_move()
    elif (state == 2):
        white_move_check()
    elif (state == 3):
        black_move_check()
    elif (state == 4):
        white_move_ai()
    elif (state == 5):
        black_move_ai()
    elif (state == 6):
        game_over()

"""
State 0: White's move
State 1: Black's move
State 2: White's move, currently in check.
State 3: Black's move, currently in check.
State 4: White's move, AI on.
State 5: Black's move, AI on. 
State 6: End
"""


"""
8/4kpQ1/1p2p2p/7P/1b1P4/6PR/5K2/4q3 w - - 0 0 < not a checkmate but happened anyways. why?
4K3/8/4kp2/4p3/6P1/1p3P2/8/8 w - - 0 0 < not a tie???
"""
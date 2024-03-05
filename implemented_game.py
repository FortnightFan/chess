import chess
import serial
import threading
import time
# import queue
import copy

EASY = 5
NORMAL = 10
HARD = 18

White_AI = {
    'switch'        :   False,
    'difficulty'    :   EASY
}

Black_AI = {
    'switch'        :   False,
    'difficulty'    :   EASY
}

Button_Pressed = False

White_Pieces = {
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Queen(0,0,0,chess.board),
    ''   :  chess.King(0,0,0,chess.board),
    ''   :  chess.Horse(0,0,0,chess.board),
    ''   :  chess.Horse(0,0,0,chess.board),
    ''   :  chess.Bishop(0,0,0,chess.board),
    ''   :  chess.Bishop(0,0,0,chess.board),
    ''   :  chess.Rook(0,0,0,chess.board),
    ''   :  chess.Rook(0,0,0,chess.board)
}

Black_Pieces = {
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Queen(1,0,0,chess.board),
    ''   :  chess.King(1,0,0,chess.board),
    ''   :  chess.Horse(1,0,0,chess.board),
    ''   :  chess.Horse(1,0,0,chess.board),
    ''   :  chess.Bishop(1,0,0,chess.board),
    ''   :  chess.Bishop(1,0,0,chess.board),
    ''   :  chess.Rook(1,0,0,chess.board),
    ''   :  chess.Rook(1,0,0,chess.board)
}

"""
Initialization function
Modifies variables
    -ser1,ser2,ser3,ser4,ser5,ser6,ser7,ser8
    -reader_thread_1,reader_thread_2,reader_thread_3,reader_thread_4,reader_thread_5,reader_thread_6,reader_thread_7,reader_thread_8
"""
ser1,ser2,ser3,ser4,ser5,ser6,ser7,ser8 = None,None,None,None,None,None,None,None
reader_thread_1,reader_thread_2,reader_thread_3,reader_thread_4,reader_thread_5,reader_thread_6,reader_thread_7,reader_thread_8 = None,None,None,None,None,None,None,None

def ready():
    global ser1,ser2,ser3,ser4,ser5,ser6,ser7,ser8
    global reader_thread_1,reader_thread_2,reader_thread_3,reader_thread_4,reader_thread_5,reader_thread_6,reader_thread_7,reader_thread_8
    
    #Arduino serial ports and threads
    try:
        ser1 = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
        reader_thread_1 = threading.Thread(target=read_port_1)
        reader_thread_1.daemon = True
        print("Serial port 1 successfully connected.")
        reader_thread_1.start()
    except:
        print("ERROR: Serial port 1 not found")
    try:
        ser2 = serial.Serial('/dev/ttyUSB1',9600,timeout=1)
        reader_thread_2 = threading.Thread(target=read_port_2)
        reader_thread_2.daemon = True
        print("Serial port 2 successfully connected.")
        reader_thread_2.start()
    except:
        print("ERROR: Serial port 2 not found")

    try:
        ser3 = serial.Serial('/dev/ttyUSB2',9600,timeout=1),
        reader_thread_3 = threading.Thread(target=read_port_3)
        reader_thread_3.daemon = True
        print("Serial port 3 successfully connected.")
        reader_thread_3.start()
    except:
        print("ERROR: Serial port 3 not found")
    
    try:
        ser4 = serial.Serial('/dev/ttyUSB3',9600,timeout=1),
        reader_thread_4 = threading.Thread(target=read_port_4)
        reader_thread_4.daemon = True
        print("Serial port 4 successfully connected.")
        reader_thread_4.start()
    except:
        print("ERROR: Serial port 4 not found")

    try:
        ser4 = serial.Serial('/dev/ttyUSB4',9600,timeout=1),
        reader_thread_5 = threading.Thread(target=read_port_5)
        reader_thread_5.daemon = True
        print("Serial port 5 successfully connected.")
        reader_thread_5.start()
    except:
        print("ERROR: Serial port 5 not found")
        
    try:
        ser3 = serial.Serial('/dev/ttyUSB5',9600,timeout=1),
        reader_thread_6 = threading.Thread(target=read_port_3)
        reader_thread_6.daemon = True
        print("Serial port 6 successfully connected.")
        reader_thread_6.start()
    except:
        print("ERROR: Serial port 6 not found")
        
    try:
        ser3 = serial.Serial('/dev/ttyUSB6',9600,timeout=1),
        reader_thread_7 = threading.Thread(target=read_port_3)
        reader_thread_7.daemon = True
        print("Serial port 7 successfully connected.")
        reader_thread_7.start()
    except:
        print("ERROR: Serial port 7 not found")
        
    try:
        ser3 = serial.Serial('/dev/ttyUSB7',9600,timeout=1),
        reader_thread_8 = threading.Thread(target=read_port_3)
        reader_thread_8.daemon = True
        print("Serial port 8 successfully connected.")
        reader_thread_8.start()
    except:
        print("ERROR: Serial port 8 not found")
        
    #Raspberry pi periferal IO
    io_thread = threading.Thread(target=io_control)    
    io_thread.daemon = True
    io_thread.start()

def exit():    
    try:
        ser1.close()
        ser2.close()
        ser2.close()
        print("Serial ports successfully closed.")
    except:
        print("ERROR: Port(s) not found") 


"""
Arduino/RFID Reader Functions
Modifies variables:
    -reader_board_mem
"""
reader_board_mem = [["" for _ in range(8)] for _ in range(8)]  #Variable that stores immediate reference data of on-board pieces. Updated constantly.
internal_board_mem = copy.deepcopy(reader_board_mem) #Variable that references the reader board for logic. Updated only on events
led_board = [[0 for _ in range(8)] for _ in range(8)]   #Variable that stores the values for the 8x8 led matrices.

def deserialize (serialized_data):
    ret_list = ["","","","","","","",""]
    ser_data = serialized_data.split(" ")
    for i in range (0,len(ser_data)):
        tup = ser_data[i].split("/")
        ret_list[int(tup[0])-1] = tup[1]
    return ret_list

def read_port_1():
    global reader_board_mem
    while True:
        try:
            data = ser1.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data)
                print(data)
                for i in range (0,8):
                    reader_board_mem[0][i] = data[i]
                ser1.flushInput()
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            time.sleep(0.25)

def read_port_2():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_3():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_4():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_5():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_6():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_7():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_8():
    global reader_board_mem
    while True:
        time.sleep(0.25)

"""
Controls on-board buttons, switches, etc. 
Modifies variables:
    -White_AI
    -Black_AI
    -game_state
"""
   
import GPIO #dummy import for testing
BUTTON = False
#import RPi.GPIO as GPIO
def io_control():
    global BUTTON
    global game_state
    GPIO.setmode(GPIO.BCM)
    button_pin = 18  # Example GPIO pin
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    button_pressed_time = None
    difficulty_levels = ["OFF", EASY, NORMAL, HARD]
    black_difficulty = 0    #Index
    white_difficulty = 0    #index
    try:
        while True:
            if GPIO.input(button_pin) == GPIO.LOW:  # Button pressed
                if button_pressed_time is None:
                    button_pressed_time = time.time()
            else:
                if button_pressed_time is not None:
                    press_duration = time.time() - button_pressed_time
                    if press_duration < 1:
                        # Short press - toggle game state
                        if game_state == 0 or game_state == 2 or game_state == 4: #If white's turn
                            print("Black turn")
                            BUTTON = True
                        elif game_state == 1 or game_state == 3 or game_state == 5: #If black's turn
                            print("White turn")
                            BUTTON = True
                    else:
                        # Long press - change difficulty
                        if game_state == 0 or game_state == 2 or game_state == 4: #If white's turn
                            white_difficulty = (white_difficulty + 1) % len(difficulty_levels)
                            if type(white_difficulty) == int:
                                White_AI['difficulty'] = difficulty_levels[white_difficulty]
                                White_AI['switch'] = True
                            else:
                                White_AI['switch'] = False
                        elif game_state == 1 or game_state == 3 or game_state == 5: #If black's turn
                            black_difficulty = (black_difficulty + 1) % len(difficulty_levels)
                            if type(black_difficulty) == int:
                                Black_AI['difficulty'] = difficulty_levels[black_difficulty]
                                Black_AI['switch'] = True
                    button_pressed_time = None  # Reset timer
            time.sleep(0.1)
    finally:
        GPIO.cleanup() 


# game_state_dict = {
#         "White_turn" : 0,
#         "Black_turn" : 1,
#         "White_turn_check" : 2,
#         "Black_turn_check" : 3,
#         "White_turn_AI" : 4,
#         "Black_turn_AI" : 5,
#         "White_checkmate" : 6,
#         "Black_checkmate" : 7,
#         "Stalemate" : 8
#     }

game_state = 0

#State machine that constantly runs. game_state var must be updated within functions.
def game_control():  
    global internal_board_mem
    global reader_board_mem 
    chess.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")  #Testing, delete later
    chess.init(chess.board)
    while True:
        internal_board_mem = reader_board_mem
        match game_state:
            case 0:
                white_move()
                chess.clear_all_lists(chess.board)
                if Black_AI['switch']:
                    game_state = 5
                elif chess.is_black_in_check(chess.board):
                    game_state = 3
                else:
                    game_state = 1
            case 1:
                black_move()
                chess.clear_all_lists(chess.board)
                if White_AI['switch']:
                    game_state = 4
                elif chess.is_black_in_check(chess.board):
                    game_state = 2
                else:
                    game_state = 0
            case 2:
                white_move_check()
            case 3:
                black_move_check()
            case 4:
                white_move_AI()
            case 5:
                black_move_AI()
            case 6:
                white_checkmate()
            case 7:
                black_checkmate()
            case 8:
                stalemate()
            
            
            
            #Game logic to determine next state val
            
    # while(1):
    #     chess.print_board(chess.board)
    #     time.sleep(1)

"""
GAME-LOGIC HELPER FUNCTIONS
"""
#Updates the board within the chess class to reflect the value of the matrix
def update_chess_positions(reader_board_mem):
    for i in range (0,8):
        for j in range (0,8):
            if reader_board_mem[i][j] == "":
                chess.board[i][j] = chess.tile
            elif reader_board_mem[i][j] in White_Pieces:
                chess.move_piece(chess.board, White_Pieces[reader_board_mem[i][j]], (i,j))
            elif reader_board_mem[i][j] in Black_Pieces:
                chess.move_piece(chess.board, Black_Pieces[reader_board_mem[i][j]], (i,j))
                
#Finds all possible moves on the board specifically for a given piece.
def chess_piece_logic(piece, color):
    chess.clear_all_lists(chess.board)
    chess.find_all_poss_moves(chess.board)
    chess.legal_king_moves(chess.board, color)
    chess.check_pin(chess.board, piece)

def set_leds(tuples_list):
    global led_board
    if tuples_list == None:
        led_board = [[0 for _ in range(8)] for _ in range(8)]
    else:
         for i in range (0,len(tuples_list)):
             x,y = tuples_list[i]    
             led_board[y][x] = 1 

"""
Game-state functions
"""
def white_move():
    global BUTTON
    global game_state
    with threading.Lock():
        temp_reader_board_mem = reader_board_mem
        internal_board_mem = reader_board_mem
    exit = False
    
    global piece
    global piece_ID
    piece_ID = {
        'UID' : "00000000",
        'pos' : (-1,-1)
    }
    piece = chess.tile
    while True:
        #State 1: Monitor board state, check button state
        while (temp_reader_board_mem == internal_board_mem):
            with threading.Lock():
                temp_reader_board_mem = reader_board_mem
            update_chess_positions(temp_reader_board_mem)   #Most likely need to move
            time.sleep(0.25)
            #If button is pressed, return.
            if BUTTON == True:
                if White_AI['switch']:
                    BUTTON = False
                    game_state = 4
                    return
                else:
                    BUTTON = False
                    return
                
        #State 2: Loop and find the lifted piece. Run chess logic and display on the lights.
        exit = False
        while not exit:
            if BUTTON == True:
                if White_AI['switch']:
                    game_state = 4
                    return
                else:
                    BUTTON = False
                    return
            for i in range (0,8):
                for j in range (0,8):
                    if temp_reader_board_mem[i][j] != internal_board_mem[i][j]:
                        try:
                            piece_ID['UID'] = internal_board_mem[i][j]
                            piece_ID['pos'] = (i,j)
                            piece = White_Pieces[internal_board_mem[i][j]]
                            if piece.color == 0:
                                exit = True
                                chess_piece_logic(piece, 0)
                                print(piece.poss_moves)
                                #Turn on lights
                        except:
                            print("ERROR: Key index not found")
                                
        #State 3: Monitor board state, look for the lifted piece. 
        while (not (piece_ID['UID'] in temp_reader_board_mem)):
            with threading.Lock():
                temp_reader_board_mem = reader_board_mem
            update_chess_positions(temp_reader_board_mem)
            time.sleep(0.25)
            #If button is pressed, return.
            if BUTTON == True:
                if White_AI['switch']:
                    BUTTON = False
                    game_state = 4
                    return
                else:
                    BUTTON = False
                    return
        update_chess_positions(temp_reader_board_mem)
        
def black_move():
    pass

def white_move_check():
    pass

def black_move_check():
    pass

def white_move_AI():
    global BUTTON
    global internal_board_mem
    global game_state
    with threading.Lock():
        internal_board_mem = reader_board_mem
    update_chess_positions(internal_board_mem)
    chess.white_ai_skill = White_AI['difficulty']
    move,tup = chess.get_best_move(chess.board, 0)
    print (tup)
    #Turn on light
    while True:
        #State 1: Monitor board state, check button state
        while (temp_reader_board_mem == internal_board_mem):
            with threading.Lock():
                temp_reader_board_mem = reader_board_mem
            update_chess_positions(temp_reader_board_mem)
            time.sleep(0.25)
            #If button is pressed, return.
            if BUTTON == True:
                if White_AI['switch']:
                    BUTTON = False
                    game_state = 0
                    return
                else:
                    BUTTON = False
                    return
                
    #Turn off light
    
def black_move_AI():
    pass
    
def white_checkmate():
    pass

def black_checkmate():
    pass

def stalemate():
    pass
  
if __name__ == "__main__":
    
    # chess.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # chess.print_board(chess.board)
    # chess.init(chess.board)

    # reader_board_mem[6][3] = "2109"
    # white_move()
    # # ready()
    # # game_control()
    # # time.sleep(20)    
    # # exit()
    
    pass


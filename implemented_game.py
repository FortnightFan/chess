import chess
import serial
import threading
import time
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

BUTTON = False
SWITCH_TURN = False

White_Pieces = {
    '1'         :  chess.Pawn(0,0,0,chess.board),
    '2'         :  chess.Pawn(0,0,0,chess.board),
    '3'         :  chess.Pawn(0,0,0,chess.board),
    '4'         :  chess.Pawn(0,0,0,chess.board),
    '5'         :  chess.Pawn(0,0,0,chess.board),
    '6'         :  chess.Pawn(0,0,0,chess.board),
    '7'         :  chess.Pawn(0,0,0,chess.board),
    '8'         :  chess.Pawn(0,0,0,chess.board),
    '5a255081'  :  chess.Queen(0,0,0,chess.board),
    'b82c5e12'  :  chess.King(0,0,0,chess.board),
    'd36db3e'   :  chess.Horse(0,0,0,chess.board),
    '12'        :  chess.Horse(0,0,0,chess.board),
    '1a3a9c81'  :  chess.Bishop(0,0,0,chess.board),
    '14'        :  chess.Bishop(0,0,0,chess.board),
    '15'        :  chess.Rook(0,0,0,chess.board),
    '16'        :  chess.Rook(0,0,0,chess.board)
}

Black_Pieces = {
    '17'        :  chess.Pawn(1,0,0,chess.board),
    '18'        :  chess.Pawn(1,0,0,chess.board),
    '19'        :  chess.Pawn(1,0,0,chess.board),
    '20'        :  chess.Pawn(1,0,0,chess.board),
    '21'        :  chess.Pawn(1,0,0,chess.board),
    '22'        :  chess.Pawn(1,0,0,chess.board),
    '23'        :  chess.Pawn(1,0,0,chess.board),
    '24'        :  chess.Pawn(1,0,0,chess.board),
    '25'        :  chess.Queen(1,0,0,chess.board),
    '26'        :  chess.King(1,0,0,chess.board),
    '27'        :  chess.Horse(1,0,0,chess.board),
    '28'        :  chess.Horse(1,0,0,chess.board),
    '29'        :  chess.Bishop(1,0,0,chess.board),
    '30'        :  chess.Bishop(1,0,0,chess.board),
    '31'        :  chess.Rook(1,0,0,chess.board),
    '32'        :  chess.Rook(1,0,0,chess.board)
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
        ser3 = serial.Serial('/dev/ttyUSB2',9600,timeout=1)
        reader_thread_3 = threading.Thread(target=read_port_3)
        reader_thread_3.daemon = True
        print("Serial port 3 successfully connected.")
        reader_thread_3.start()
    except:
        print("ERROR: Serial port 3 not found")
    
    try:
        ser4 = serial.Serial('/dev/ttyUSB3',9600,timeout=1)
        reader_thread_4 = threading.Thread(target=read_port_4)
        reader_thread_4.daemon = True
        print("Serial port 4 successfully connected.")
        reader_thread_4.start()
    except:
        print("ERROR: Serial port 4 not found")

    try:
        ser5 = serial.Serial('/dev/ttyUSB4',9600,timeout=1)
        reader_thread_5 = threading.Thread(target=read_port_5)
        reader_thread_5.daemon = True
        print("Serial port 5 successfully connected.")
        reader_thread_5.start()
    except:
        print("ERROR: Serial port 5 not found")
        
    try:
        ser6 = serial.Serial('/dev/ttyUSB5',9600,timeout=1)
        reader_thread_6 = threading.Thread(target=read_port_6)
        reader_thread_6.daemon = True
        print("Serial port 6 successfully connected.")
        reader_thread_6.start()
    except:
        print("ERROR: Serial port 6 not found")
        
    try:
        ser7 = serial.Serial('/dev/ttyUSB6',9600,timeout=1)
        reader_thread_7 = threading.Thread(target=read_port_7)
        reader_thread_7.daemon = True
        print("Serial port 7 successfully connected.")
        reader_thread_7.start()
    except:
        print("ERROR: Serial port 7 not found")
        
    try:
        ser8 = serial.Serial('/dev/ttyUSB7',9600,timeout=1)
        reader_thread_8 = threading.Thread(target=read_port_8)
        reader_thread_8.daemon = True
        print("Serial port 8 successfully connected.")
        reader_thread_8.start()
    except:
        print("ERROR: Serial port 8 not found")
        
    #Raspberry pi periferal IO
    io_thread = threading.Thread(target=io_control)    
    io_thread.daemon = True
    io_thread.start()
    
    #LED matrix updater.
    # led_matrix_thread = threading.Thread(target=update_matrix)
    # led_matrix_thread.daemon = True
    # led_matrix_thread.start()

"""
Arduino/RFID Reader Functions
Modifies variables:
    -reader_board_mem
"""
reader_board_mem = [["" for _ in range(8)] for _ in range(8)]  #Variable that stores immediate reference data of on-board pieces. Updated constantly.
internal_board_mem = copy.deepcopy(reader_board_mem) #Variable that references the reader board for logic. Updated only on events
led_board = [[0 for _ in range(8)] for _ in range(8)]   #Variable that stores the values for the 8x8 led matrices.

def deserialize (serialized_data, reader_num):
    global ser1,ser2,ser3,ser4,ser5,ser6,ser7,ser8
    ret_list = ["","","","","","","",""]
    ser_data = serialized_data.split(" ")
    if len(ser_data) != 8:
        print(f"ERROR port {reader_num}: Incorrect data sizing")
        match reader_num:
            case 1:
                print(f"Resetting port {reader_num}")
                ser1.flush()
                ser1.close()
                time.sleep(.25)
                ser1 = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
                time.sleep(.5)
            case 2:
                print(f"Resetting port {reader_num}")
                ser2.flush()
                ser2.close()
                time.sleep(.25)
                ser2 = serial.Serial('/dev/ttyUSB1',9600,timeout=1)
                time.sleep(.5)
            case 3:
                print(f"Resetting port {reader_num}")
                ser3.flush()
                ser3.close()
                time.sleep(.25)
                ser3 = serial.Serial('/dev/ttyUSB2',9600,timeout=1)
                time.sleep(.5)
            case 4:
                print(f"Resetting port {reader_num}")
                ser4.flush()
                ser4.close()
                time.sleep(.25)
                ser4 = serial.Serial('/dev/ttyUSB3',9600,timeout=1)
                time.sleep(.5)
            case 5:
                print(f"Resetting port {reader_num}")
                ser5.flush()
                ser5.close()
                time.sleep(.25)
                ser5 = serial.Serial('/dev/ttyUSB4',9600,timeout=1)
                time.sleep(.5)
            case 6:
                print(f"Resetting port {reader_num}")
                ser6.flush()
                ser6.close()
                time.sleep(.25)
                ser6 = serial.Serial('/dev/ttyUSB5',9600,timeout=1)
                time.sleep(.5)
            case 7:
                print(f"Resetting port {reader_num}")
                ser7.flush()
                ser7.close()
                time.sleep(.25)
                ser7 = serial.Serial('/dev/ttyUSB6',9600,timeout=1)
                time.sleep(.5)
            case 8:
                print(f"Resetting port {reader_num}")
                ser8.flush()
                ser8.close()
                time.sleep(.25)
                ser8 = serial.Serial('/dev/ttyUSB7',9600,timeout=1)
                time.sleep(.5)
        return ret_list
    else:
        for i in range (0,8):
            ret_list[i] = ser_data[i]
        
    return ret_list

def read_port_1():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser1.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,1)
                for i in range (0,8):
                    reader_board_mem[0][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser1.flush()
            time.sleep(0.25)

def read_port_2():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser2.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,2)
                for i in range (0,8):
                    reader_board_mem[1][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser2.flush()
            time.sleep(0.25)
            
def read_port_3():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser3.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,3)
                for i in range (0,8):
                    reader_board_mem[2][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser3.flush()
            time.sleep(0.25)
            
def read_port_4():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser4.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,4)
                for i in range (0,8):
                    reader_board_mem[3][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser4.flush()
            time.sleep(0.25)
            
def read_port_5():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser5.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,5)
                for i in range (0,8):
                    reader_board_mem[4][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser5.flush()
            time.sleep(0.25)
            
def read_port_6():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser6.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,6)
                for i in range (0,8):
                    reader_board_mem[5][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser6.flush()
            time.sleep(0.25)
            
def read_port_7():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser7.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,7)
                for i in range (0,8):
                    reader_board_mem[6][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser7.flush()
            time.sleep(0.25)
            
def read_port_8():
    global reader_board_mem
    time.sleep(1)
    while True:
        try:
            data = ser8.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data,8)
                for i in range (0,8):
                    reader_board_mem[7][i] = data[i]
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser8.flush()
            time.sleep(0.25)

"""
Controls on-board buttons, switches, etc. 
Modifies variables:
    -White_AI
    -Black_AI
    -game_state
"""
   
# import GPIO #dummy import for testing
import RPi.GPIO as GPIO
def io_control():
    global SWITCH_TURN
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
                        with lock:
                            SWITCH_TURN = True
                    else:
                        # Long press - change difficulty
                        if game_state == 0 or game_state == 2 or game_state == 4: #If white's turn
                            white_difficulty = (white_difficulty + 1) % len(difficulty_levels)
                            if white_difficulty != 0:
                                White_AI['difficulty'] = difficulty_levels[white_difficulty]
                                White_AI['switch'] = True
                                with lock:
                                    BUTTON = True
                            else:
                                White_AI['switch'] = False
                                BUTTON = True
                        elif game_state == 1 or game_state == 3 or game_state == 5: #If black's turn
                            black_difficulty = (black_difficulty + 1) % len(difficulty_levels)
                            if black_difficulty != 0:
                                Black_AI['difficulty'] = difficulty_levels[black_difficulty]
                                Black_AI['switch'] = True
                                BUTTON = True
                            else:
                                Black_AI['switch'] = False
                                BUTTON = True
                    button_pressed_time = None  # Reset timer
            time.sleep(0.25)
    finally:
        GPIO.cleanup() 

"""
Function to update the 8x8 led matrix
Modifies variables:
    - led_board
"""
def update_matrix():
    global led_board
    # Defines the number of rows and columns in your matrix
    numRows = 8
    numCols = 8

    # Defines the pins on the Raspberry Pi connected to the rows and columns
    rowPins = [4, 17, 27, 22, 5, 6, 13, 19]
    colPins = [26, 21, 20, 16, 12, 25, 24, 23]

    # Set up GPIO
    GPIO.setmode(GPIO.BCM)

    # Sets row pins as OUTPUT and column pins as INPUT
    for row_pin in rowPins:
        GPIO.setup(row_pin, GPIO.OUT)

    for col_pin in colPins:
        GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while True:
            # Loops through each column
            for col in range(numCols):
                # Activates the current column
                GPIO.setup(colPins[col], GPIO.OUT)
                GPIO.output(colPins[col], GPIO.LOW)

                # Loops through each row in the current column
                for row in range(numRows):
                    # Turn on or off the LED at the current row and column based on the display matrix
                    GPIO.output(rowPins[row], led_board[row][col])
                    time.sleep(0)  # Adjust this sleep as needed for brightness control (flashes with delay on)

                    # Turns off the LED at the current row and column
                    GPIO.output(rowPins[row], GPIO.LOW)

                # Deactivate the current column for the next iteration
                GPIO.setup(colPins[col], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    except Exception as e:
        print (f"ERROR: {e}")
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
"""
Game control state machine that runs the main thread.
Modifies variables:
    - game_state
    - internal_board_mem
    - reader_board_mem
"""
def game_control(): 
    global game_state
    global internal_board_mem
    global reader_board_mem 
    chess.init(chess.board)
    while True:
        internal_board_mem = reader_board_mem
        match game_state:
            case 0:
                while(True):
                    return_id = white_move()
                    """
                    Return values:
                        None: Successful move completed
                        -1: Error occured, reset.
                        0: Change turn to black.
                        1: Turn on white AI.
                    """
                    chess.clear_all_lists(chess.board)

                    if return_id == 1:
                        if White_AI['switch']:
                            game_state = 4
                            print (f"Game state: 4")
                            break                        
                    elif return_id == 0:
                        if Black_AI['switch']:
                            game_state = 5
                            print (f"Game state: 5")
                            break
                        else:
                            game_state = 1
                            print (f"Game state: 1")
                            break
                        
                    
            case 1:
                while(True):
                    return_id = black_move()
                    """
                    Return values:
                        None: Successful move completed
                        -1: Error occured, reset.
                        0: Change turn to white.
                        1: Turn on white AI.
                    """
                    chess.clear_all_lists(chess.board)

                    if return_id == 1:
                        if Black_AI['switch']:
                            game_state = 5
                            print (f"Game state: 5")
                            break                        
                    elif return_id == 0:
                        if White_AI['switch']:
                            game_state = 4
                            print (f"Game state: 4")
                            break
                        else:
                            game_state = 0
                            print (f"Game state: 0")
                            break
                        
            case 4:
                while(True):
                    return_id = white_move_AI()
                    """
                    Return values: 
                        None: Successful, switch to black's turn.
                        1: Turn off white AI, switch to white's turn.
                    """
                    if return_id == None:
                        if Black_AI['switch']:
                            game_state = 5
                        else:
                            game_state = 1
                        break
                    elif return_id == 1:
                        game_state = 0
                        break
            case 5:
                while(True):
                    return_id = black_move_AI()
                    """
                    Return values: 
                        None: Successful, switch to white's turn.
                        1: Turn off black AI, switch to black's turn.
                    """
                    if return_id == None:
                        if White_AI['switch']:
                            game_state = 4
                        else:
                            game_state = 2
                        break            
                    elif return_id == 1:
                        game_state = 1
                        break
            case 8:
                stalemate()

"""
GAME-LOGIC HELPER FUNCTIONS
"""
#Updates the board within the chess class to reflect the value of the matrix
def update_chess_positions(reader_board_mem):
    for i in range (0,8):
        for j in range (0,8):
            if reader_board_mem[i][j] == "" or reader_board_mem[i][j] == "00000000":
                chess.board[i][j] = chess.tile
            elif reader_board_mem[i][j] in White_Pieces:
                chess.board[i][j] = White_Pieces[reader_board_mem[i][j]]
                White_Pieces[reader_board_mem[i][j]].ypos,White_Pieces[reader_board_mem[i][j]].xpos = i,j
            elif reader_board_mem[i][j] in Black_Pieces:
                chess.board[i][j] = Black_Pieces[reader_board_mem[i][j]]
                Black_Pieces[reader_board_mem[i][j]].ypos,Black_Pieces[reader_board_mem[i][j]].xpos = i,j
                
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
lock = threading.Lock()
"""
Game-state functions
"""
"""
Return values:
    None: Successful move completed
    -1: Error occured, reset.
    0: Change turn to black.
    1: Turn on white AI.
"""
def white_move():
    global BUTTON
    global SWITCH_TURN
    global game_state
    global piece
    global piece_ID
    
    with lock:
        temp_reader_board_mem = copy.deepcopy(reader_board_mem)
        internal_board_mem = copy.deepcopy(reader_board_mem)
    exit = False
    update_chess_positions(internal_board_mem)

    piece_ID = {
        'UID' : "-1",
        'pos' : (-1,-1)
    }
    
    piece = chess.tile
    exit = False
    while True:
        #State 1: Monitor board state, check button state
        print("White_move_state 1")
        chess.print_board(chess.board)
        while (temp_reader_board_mem == internal_board_mem):
            with lock:
                temp_reader_board_mem = reader_board_mem[:]  
            time.sleep(.25)
            
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    return 1
                
        #State 2: Loop and find the lifted piece. Run chess logic and display on the lights.
        while not exit:
            for i in range (0,8):
                for j in range (0,8):
                    if temp_reader_board_mem[i][j] != internal_board_mem[i][j]:
                        try:
                            piece_ID['UID'] = internal_board_mem[i][j]
                            piece_ID['pos'] = (i,j)
                            piece = White_Pieces[piece_ID['UID']]
                            if piece.color == 0:
                                exit = True
                                chess_piece_logic(piece, 0)
                                chess.print_board(chess.board)
                                print (piece.poss_moves)
                                print(piece.poss_captures)
                                #Turn on lights
                        except Exception as e:
                            exit = True
                            print(f"ERROR: {e}\nResetting white move")
                            return(-1)
                            
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    return 1

        print("White_move_state 2")
        #State 3: Monitor board state, look for the lifted piece. 
        while not any(piece_ID['UID'] in sublist for sublist in temp_reader_board_mem):
            temp_reader_board_mem = reader_board_mem[:]
            time.sleep(0.25)
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    return 1

        update_chess_positions(temp_reader_board_mem)
        chess.print_board(chess.board)
        return #successful move has been made
"""
Return values:
    None: Successful move completed
    -1: Error occured, reset.
    0: Change turn to black.
    1: Turn on white AI.
"""
def black_move():
    global BUTTON
    global SWITCH_TURN
    global game_state
    global piece
    global piece_ID
    
    with lock:
        temp_reader_board_mem = copy.deepcopy(reader_board_mem)
        internal_board_mem = copy.deepcopy(reader_board_mem)
    exit = False
    update_chess_positions(internal_board_mem)

    piece_ID = {
        'UID' : "-1",
        'pos' : (-1,-1)
    }
    
    piece = chess.tile
    exit = False
    while True:
        #State 1: Monitor board state, check button state
        print("Black_move_state 1")
        chess.print_board(chess.board)
        while (temp_reader_board_mem == internal_board_mem):
            with lock:
                temp_reader_board_mem = reader_board_mem[:]  
            time.sleep(.25)
            
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    return 1
                
        #State 2: Loop and find the lifted piece. Run chess logic and display on the lights.
        while not exit:
            for i in range (0,8):
                for j in range (0,8):
                    if temp_reader_board_mem[i][j] != internal_board_mem[i][j]:
                        try:
                            piece_ID['UID'] = internal_board_mem[i][j]
                            piece_ID['pos'] = (i,j)
                            piece = Black_Pieces[piece_ID['UID']]
                            if piece.color == 1:
                                exit = True
                                chess_piece_logic(piece, 1)
                                chess.print_board(chess.board)
                                print (piece.poss_moves)
                                print(piece.poss_captures)
                                #Turn on lights
                        except Exception as e:
                            exit = True
                            print(f"ERROR: {e}\nResetting black move")
                            return(-1)
                            
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    return 1

        print("Black_move_state 2")
        #State 3: Monitor board state, look for the lifted piece. 
        while not any(piece_ID['UID'] in sublist for sublist in temp_reader_board_mem):
            temp_reader_board_mem = reader_board_mem[:]
            time.sleep(0.25)
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    return 1
        
        update_chess_positions(temp_reader_board_mem)
        chess.print_board(chess.board)
        return #successful move has been made

def white_move_AI():
    global BUTTON
    global SWITCH_TURN
    global internal_board_mem
    global game_state
    
    if White_AI['difficulty'] != 'OFF':
        chess.white_ai_skill = White_AI['difficulty']
    
    while True:
        with lock:
            internal_board_mem = reader_board_mem
        update_chess_positions(internal_board_mem)
        move,tup = chess.get_best_move(chess.board, 0)
        if tup != -1:
            break
        with lock:
            if BUTTON == True:
                BUTTON = False
                if not White_AI['switch']:
                    set_leds(None)
                    return (1)
            if SWITCH_TURN == True:
                SWITCH_TURN = False
                set_leds(None)
                return
        time.sleep(0.5)
        
    chess.print_board(chess.board)
    print (tup)
    set_leds(tup)
    
    #Wait for button push to progress.
    while True:
        with lock:
            if BUTTON == True:
                BUTTON = False
                if not White_AI['switch']:
                    set_leds(None)
                    return (1)
            if SWITCH_TURN == True:
                SWITCH_TURN = False
                set_leds(None)
                return
        time.sleep(0.25)
    
    
def black_move_AI():
    global BUTTON
    global SWITCH_TURN
    global internal_board_mem
    global game_state
    
    if Black_AI['difficulty'] != 'OFF':
        chess.black_ai_skill = Black_AI['difficulty']
    
    while True:
        with lock:
            internal_board_mem = reader_board_mem
        update_chess_positions(internal_board_mem)
        move,tup = chess.get_best_move(chess.board, 0)
        if tup != -1:
            break
        
        with lock:
            if BUTTON == True:
                BUTTON = False
                if not Black_AI['switch']:
                    set_leds(None)
                    return (1)
            if SWITCH_TURN == True:
                SWITCH_TURN = False
                set_leds(None)
                return        
        
        time.sleep(0.5)
        
    chess.print_board(chess.board)
    print (tup)
    set_leds(tup)
    
    #Wait for button push to progress.
    while True:
        with lock:
            if BUTTON == True:
                BUTTON = False
                if not Black_AI['switch']:
                    set_leds(None)
                    return (1)
            if SWITCH_TURN == True:
                SWITCH_TURN = False
                set_leds(None)
                return
        time.sleep(0.25)   

def white_checkmate():
    pass

def black_checkmate():
    pass

def stalemate():
    pass

if __name__ == "__main__":
    
    ready()
    time.sleep(5)
    game_control()

    
    pass


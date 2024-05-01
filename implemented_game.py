import chess
import serial
import threading
import time
import copy
# import GPIO #dummy import for testing
import RPi.GPIO as GPIO
# from luma.core.interface.serial import spi, noop
# from luma.led_matrix.device import max7219
# from luma.core.render import canvas
# from luma.core.legacy import text
# from luma.core.legacy.font import proportional, LCD_FONT
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

game_state = 0

White_Pieces = {
    '42f8cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '4308cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '4318cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '4328cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '4278cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '4288cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '4298cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '42a8cf231290'          :  chess.Pawn(0,0,0,chess.board),
    '4238cf231290'          :  chess.Queen(0,0,0,chess.board),
    '4248cf231290'          :  chess.King(0,0,0,chess.board),
    '42c8cf231290'          :  chess.Horse(0,0,0,chess.board),
    '42b8cf231290'          :  chess.Horse(0,0,0,chess.board),
    '4c8df231290'           :  chess.Bishop(0,0,0,chess.board),
    '4d8df231290'           :  chess.Bishop(0,0,0,chess.board),
    '42d8cf231290'          :  chess.Rook(0,0,0,chess.board),
    '42e8cf231290'          :  chess.Rook(0,0,0,chess.board)
}

Black_Pieces = {
    '4218cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '4228cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '41d8cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '41e8cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '41f8cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '4208cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '41a8cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '41b8cf231290'          :  chess.Pawn(1,0,0,chess.board),
    '4108cf231290'          :  chess.Queen(1,0,0,chess.board),
    '4118cf231290'          :  chess.King(1,0,0,chess.board),
    '4168cf231290'          :  chess.Horse(1,0,0,chess.board),
    '4178cf231290'          :  chess.Horse(1,0,0,chess.board),
    '4e8cf231290'           :  chess.Bishop(1,0,0,chess.board),
    '4f8cf231290'           :  chess.Bishop(1,0,0,chess.board),
    '4188cf231290'          :  chess.Rook(1,0,0,chess.board),
    '4198cf231290'          :  chess.Rook(1,0,0,chess.board)
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
        
    # Raspberry pi periferal IO
    io_thread = threading.Thread(target=io_control)    
    io_thread.daemon = True
    io_thread.start()
    
    # # LED matrix updater.
    led_matrix_thread = threading.Thread(target=update_matrix)
    led_matrix_thread.daemon = True
    led_matrix_thread.start()

    #8x8 matrices runner.
    # max_display_thread = threading.Thread(target=run_chess_timer)
    # max_display_thread.daemon = True
    # max_display_thread.start()


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
                time.sleep(.1)
                ser1 = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
                time.sleep(.5)
            case 2:
                print(f"Resetting port {reader_num}")
                ser2.flush()
                ser2.close()
                time.sleep(.1)
                ser2 = serial.Serial('/dev/ttyUSB1',9600,timeout=1)
                time.sleep(.5)
            case 3:
                print(f"Resetting port {reader_num}")
                ser3.flush()
                ser3.close()
                time.sleep(.1)
                ser3 = serial.Serial('/dev/ttyUSB2',9600,timeout=1)
                time.sleep(.5)
            case 4:
                print(f"Resetting port {reader_num}")
                ser4.flush()
                ser4.close()
                time.sleep(.1)
                ser4 = serial.Serial('/dev/ttyUSB3',9600,timeout=1)
                time.sleep(.5)
            case 5:
                print(f"Resetting port {reader_num}")
                ser5.flush()
                ser5.close()
                time.sleep(.1)
                ser5 = serial.Serial('/dev/ttyUSB4',9600,timeout=1)
                time.sleep(.5)
            case 6:
                print(f"Resetting port {reader_num}")
                ser6.flush()
                ser6.close()
                time.sleep(.1)
                ser6 = serial.Serial('/dev/ttyUSB5',9600,timeout=1)
                time.sleep(.5)
            case 7:
                print(f"Resetting port {reader_num}")
                ser7.flush()
                ser7.close()
                time.sleep(.1)
                ser7 = serial.Serial('/dev/ttyUSB6',9600,timeout=1)
                time.sleep(.5)
            case 8:
                print(f"Resetting port {reader_num}")
                ser8.flush()
                ser8.close()
                time.sleep(.1)
                ser8 = serial.Serial('/dev/ttyUSB7',9600,timeout=1)
                time.sleep(.5)
        return ret_list
    else:
        for i in range (0,8):
            ret_list[i] = ser_data[i]
        
    return ret_list

def read_port_1():
    global reader_board_mem
    global ser1
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
            time.sleep(0.25)

def read_port_2():
    global reader_board_mem
    global ser2
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
            time.sleep(0.25)
            
def read_port_3():
    global reader_board_mem
    global ser3
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
            time.sleep(0.25)
            
def read_port_4():
    global reader_board_mem
    global ser4
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
            time.sleep(0.25)
            
def read_port_5():
    global reader_board_mem
    global ser5
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
            time.sleep(0.25)
            
def read_port_6():
    global reader_board_mem
    global ser6
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
            time.sleep(0.25)
            
def read_port_7():
    global reader_board_mem
    global ser7
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
            time.sleep(0.25)
            
def read_port_8():
    global reader_board_mem
    global ser8
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
            time.sleep(0.25)

"""
Controls on-board buttons, switches, etc. 
Modifies variables:
    -White_AI
    -Black_AI
    -game_state
"""

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

"""
Controls 8x8 matrices.
"""

global timer1, timer2, active_timer, last_button_press, device
timer1 = 60  # Initialize timer1 with 60 seconds
timer2 = 60  # Initialize timer2 with 60 seconds
active_timer = None
last_button_press = time.time()
# serial = spi(port=0, device=0, gpio=noop())
# device = max7219(serial, cascaded=4, block_orientation=-90)

def handle_timer_button_press():
    global timer1, timer2, active_timer, last_button_press
    current_time = time.time()
    if current_time - last_button_press < 0.1:  # Debounce manually
        return
    last_button_press = current_time

    if active_timer is None:
        timer1 = 60
        active_timer = 1
    elif active_timer == 1:
        if timer2 is None:
            timer2 = 60
        active_timer = 2
    else:
        active_timer = 1

def display_message(device, message):
    text_width = len(message) * 8  
        # Calculate the starting position to center the text
    start_pos = max((device.width - text_width) // 2, 0)
        # Display the centered text
    with canvas(device) as draw:
        text(draw, (start_pos, 0), message, fill="white", font=proportional(LCD_FONT))

def run_chess_timer():
    global timer1, timer2, active_timer, last_button_press, device
    display_message(device, "CHESS")

    # Main program loop
    while timer1 > 0 and timer2 > 0:
        time.sleep(1)
        if active_timer == 1:
            timer1 -= 1
            display_message(device, f"W: {timer1}")
        elif active_timer == 2:
            timer2 -= 1
            display_message(device, f"B: {timer2}")

    if timer1 <= 0:
        winner = "White wins!"
    elif timer2 <= 0:
        winner = "Black wins!"

    display_message(device, winner)
    time.sleep(10)
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
                    chess.clear_all_lists(chess.board)
                    chess.update_king_pos(chess.board)
                    return_id = white_move()
                    """
                    Return values:
                        None: Successful move completed
                        -1: Error occured, reset.
                        0: Change turn to black.
                        1: Turn on white AI.
                        2: Checkmate, exit.
                    """
                    chess.clear_all_lists(chess.board)
                    # chess.check_promotions(chess.board,0) #Commented out, will not work currently
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
                    elif return_id == 2:
                        return                                    
            case 1:
                while(True):
                    chess.clear_all_lists(chess.board)
                    chess.update_king_pos(chess.board)
                    return_id = black_move()
                    """
                    Return values:
                        None: Successful move completed
                        -1: Error occured, reset.
                        0: Change turn to white.
                        1: Turn on white AI.
                        2: Checkmate, exit
                    """
                    chess.clear_all_lists(chess.board)
                    # chess.check_promotions(chess.board,1)
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
                    elif return_id == 2:
                        return
                        
            case 4:
                while(True):
                    return_id = white_move_AI()
                    """
                    Return values: 
                        None: Successful, switch to black's turn.
                        1: Turn off white AI, switch to white's turn.
                        0: Update white ai difficulty
                    """
                    if return_id == None:
                        with lock:
                            internal_board_mem = copy.deepcopy(reader_board_mem)
                        update_chess_positions(internal_board_mem)
                        chess.find_all_poss_moves(chess.board)
                        chess.update_king_pos(chess.board)
                        try:
                            print("Checking if black is in checkmate...")
                            if chess.is_black_checkmate(chess.board):
                                print("White wins!")
                                white_checkmate()
                                return
                            print("White is not in checkmate.")
                        except Exception as e:
                            print(f"ERROR in black_move_AI: {e}")
                        if Black_AI['switch']:
                            game_state = 5
                        else:
                            game_state = 1
                        break
                    elif return_id == 1:
                        game_state = 0
                        break
                    elif return_id == 2:
                        return
                    
            case 5:
                while(True):
                    return_id = black_move_AI()
                    """
                    Return values: 
                        None: Successful, switch to white's turn.
                        1: Turn off black AI, switch to black's turn.
                    """
                    if return_id == None:
                        with lock:
                            internal_board_mem = copy.deepcopy(reader_board_mem)
                        update_chess_positions(internal_board_mem)
                        chess.find_all_poss_moves(chess.board)
                        chess.update_king_pos(chess.board)
                        try:
                            print("Checking if white is in checkmate...")
                            if chess.is_white_checkmate(chess.board):
                                print("Black wins!")
                                black_checkmate()
                                return
                            print("White is not in checkmate.")
                        except Exception as e:
                            print(f"ERROR in black_move_AI: {e}")
                            
                        if White_AI['switch']:
                            game_state = 4
                        else:
                            game_state = 0
                        break            
                    elif return_id == 1:
                        game_state = 1
                        break
                    elif return_id == 2:
                        return
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
    chess.find_all_poss_moves(chess.board)
    chess.update_king_pos(chess.board)
    try:
        chess.legal_king_moves(chess.board, color)
        chess.check_pin(chess.board, piece)
    except Exception as e:
        print(f"ERROR in chess_piece_logic: {e}")

def set_leds(tuples_list):
    global led_board
    if tuples_list == None:
        led_board = [[0 for _ in range(8)] for _ in range(8)]
    else:
        for i in range (0,len(tuples_list)):
            x,y = tuples_list[i]    
            led_board[7-y][7-x] = 1 
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
        chess.find_all_poss_moves(chess.board)
        chess.update_king_pos(chess.board)
        try:
            print("Checking if black is in checkmate...")
            if chess.is_black_checkmate(chess.board):
                print("White wins!")
                white_checkmate()
                return 2
            print("Black is not in checkmate.")
        except Exception as e:
            print(f"ERROR in white_move: {e}")
        chess.clear_all_lists(chess.board)
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
                    set_leds(None)
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    set_leds(None)
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
                                if (piece.poss_moves == [] and piece.poss_captures == []):
                                    print(f"No possible moves for {piece}")
                                    set_leds(None)
                                else:
                                    print (piece.poss_moves)
                                    print(piece.poss_captures)
                                    set_leds(piece.poss_moves)
                                    set_leds(piece.poss_captures)
                        except Exception as e:
                            exit = True
                            print(f"ERROR: {e}\nResetting white move")
                            return(-1)
            time.sleep(0.1)
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    set_leds(None)
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    set_leds(None)
                    return 1

        print("White_move_state 2")
        #State 3: Monitor board state, look for the lifted piece. 
        while not any(piece_ID['UID'] in sublist for sublist in temp_reader_board_mem):
            temp_reader_board_mem = reader_board_mem[:]
            time.sleep(0.1)
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    set_leds(None)
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    set_leds(None)
                    return 1

        set_leds(None)
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
        chess.find_all_poss_moves(chess.board)
        chess.update_king_pos(chess.board)
        try:
            print("Checking if white is in checkmate...")
            if chess.is_white_checkmate(chess.board):
                print("Black wins!")
                black_checkmate()
                return 2
            print("White is not in checkmate.")

        except Exception as e:
            print(f"ERROR in black_move: {e}")
        chess.clear_all_lists(chess.board)
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
                    set_leds(None)
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    set_leds(None)
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
                                if (piece.poss_moves == [] and piece.poss_captures == []):
                                    print(f"No possible moves for {piece}")
                                    set_leds(None)
                                else:
                                    print (piece.poss_moves)
                                    print(piece.poss_captures)
                                    set_leds(piece.poss_moves)
                                    set_leds(piece.poss_captures)
                        except Exception as e:
                            exit = True
                            print(f"ERROR: {e}\nResetting black move")
                            set_leds(None)
                            return(-1)
            time.sleep(0.1)               
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    set_leds(None)
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    set_leds(None)
                    return 1

        print("Black_move_state 2")
        #State 3: Monitor board state, look for the lifted piece. 
        while not any(piece_ID['UID'] in sublist for sublist in temp_reader_board_mem):
            temp_reader_board_mem = reader_board_mem[:]
            time.sleep(0.1)
            #If button is pressed, return.
            with lock:
                if SWITCH_TURN == True:
                    SWITCH_TURN = False
                    set_leds(None)
                    return 0
                if BUTTON == True:
                    BUTTON = False
                    set_leds(None)
                    return 1
        set_leds(None)
        update_chess_positions(temp_reader_board_mem)
        chess.print_board(chess.board)
        return #successful move has been made

def white_move_AI():
    global BUTTON
    global SWITCH_TURN
    global internal_board_mem
    global game_state
    
    update_chess_positions(reader_board_mem)
    chess.find_all_poss_moves(chess.board)
    chess.update_king_pos(chess.board)
    try:
        print("Checking if white is in checkmate...")
        if chess.is_black_checkmate(chess.board):
            print("White wins!")
            white_checkmate()
            return 2
        print("Black is not in checkmate.")
    except Exception as e:
        print(f"ERROR in white_move_AI: {e}")
        
    if White_AI['difficulty'] != 'OFF':
        chess.white_ai_skill = White_AI['difficulty']
    
    while True:
        with lock:
            internal_board_mem = reader_board_mem
        update_chess_positions(internal_board_mem)
        move,tup = chess.get_best_move(chess.board, 0)
        if tup != -1:   #Valid best move found
            break
        if tup == -2:   #either checkmate or stalemate occurred, exit.
            return
        with lock:
            if BUTTON == True:
                print(f"White AI: {White_AI}")
                BUTTON = False
                set_leds(None)
                if not White_AI['switch']:
                    return (1)
                else:
                    return (0)
            if SWITCH_TURN == True:
                SWITCH_TURN = False
                set_leds(None)
                return
        time.sleep(0.25)
        
    chess.print_board(chess.board)
    print (tup)
    set_leds(tup)
    
    #Wait for button push to progress.
    while True:
        with lock:
            if BUTTON == True:
                print(f"White AI: {White_AI}")
                BUTTON = False
                if not White_AI['switch']:
                    set_leds(None)
                    return (1)
                else:
                    return (0)
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
    
    update_chess_positions(reader_board_mem)
    chess.find_all_poss_moves(chess.board)
    chess.update_king_pos(chess.board)
    try:
        print("Checking if black is in checkmate...")
        if chess.is_white_checkmate(chess.board):
            print("Black wins!")
            black_checkmate()
            return 2
        print("White is not in checkmate.")
    except Exception as e:
        print(f"ERROR in black_move_AI: {e}")
    
    if Black_AI['difficulty'] != 'OFF':
        chess.black_ai_skill = Black_AI['difficulty']
    
    while True:
        with lock:
            internal_board_mem = reader_board_mem
        update_chess_positions(internal_board_mem)
        move,tup = chess.get_best_move(chess.board, 1)
        if tup != -1:
            break
        if tup == -2:   #either checkmate or stalemate occurred, exit.
            return
        with lock:
            if BUTTON == True:
                BUTTON = False
                print(f"Black AI: {Black_AI}")
                if not Black_AI['switch']:
                    set_leds(None)
                    return (1)
                else:
                    return (0)
            if SWITCH_TURN == True:
                SWITCH_TURN = False
                set_leds(None)
                return        
        
        time.sleep(0.25)
        
    chess.print_board(chess.board)
    print (tup)
    set_leds(tup)
    
    #Wait for button push to progress.
    while True:
        with lock:
            if BUTTON == True:
                BUTTON = False
                print(f"Black AI: {Black_AI}")
                if not Black_AI['switch']:
                    set_leds(None)
                    return (1)
                else:
                    return (0)
            if SWITCH_TURN == True:
                SWITCH_TURN = False
                set_leds(None)
                return
        time.sleep(0.25)   

def white_checkmate():
    global led_board
    led_board[0] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[1] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[2] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[3] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[4] = [1, 1, 1, 1, 1, 1, 1, 1]
    led_board[5] = [0, 1, 1, 1, 1, 1, 1, 0]
    led_board[6] = [0, 0, 1, 1, 1, 1, 0, 0]
    led_board[7] = [0, 0, 0, 1, 1, 0, 0, 0]
    time.sleep(5)

def black_checkmate():
    global led_board
    led_board[0] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[1] = [0, 0, 1, 1, 1, 1, 0, 0]
    led_board[2] = [0, 1, 1, 1, 1, 1, 1, 0]
    led_board[3] = [1, 1, 1, 1, 1, 1, 1, 1]
    led_board[4] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[5] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[6] = [0, 0, 0, 1, 1, 0, 0, 0]
    led_board[7] = [0, 0, 0, 1, 1, 0, 0, 0]
    time.sleep(5)

def stalemate():
    pass

if __name__ == "__main__":
    ready()
    
    for i in range (0,8):
        led_board[i] = [1,1,1,1,1,1,1,1]
        time.sleep(0.5)
        led_board[i] = [0,0,0,0,0,0,0,0]
        time.sleep(0.5)
        
    game_control()
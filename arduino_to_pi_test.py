import chess
import serial
import threading
import time
import copy
"""
Reader communication testing
"""


reader_board_mem = [["" for _ in range(8)] for _ in range(8)]  #Variable that stores immediate reference data of on-board pieces. Updated constantly.
led_board = [[0 for _ in range(8)] for _ in range(8)]   #Variable that stores the values for the 8x8 led matrices.


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
                time.sleep(.25)
            case 2:
                print(f"Resetting port {reader_num}")
                ser2.flush()
                ser2.close()
                time.sleep(.25)
                ser2 = serial.Serial('/dev/ttyUSB1',9600,timeout=1)
                time.sleep(.25)
            case 3:
                print(f"Resetting port {reader_num}")
                ser3.flush()
                ser3.close()
                time.sleep(.25)
                ser3 = serial.Serial('/dev/ttyUSB2',9600,timeout=1)
                time.sleep(.25)
            case 4:
                print(f"Resetting port {reader_num}")
                ser4.flush()
                ser4.close()
                time.sleep(.25)
                ser4 = serial.Serial('/dev/ttyUSB3',9600,timeout=1)
                time.sleep(.25)
            case 5:
                print(f"Resetting port {reader_num}")
                ser5.flush()
                ser5.close()
                time.sleep(.25)
                ser5 = serial.Serial('/dev/ttyUSB4',9600,timeout=1)
                time.sleep(.25)
            case 6:
                print(f"Resetting port {reader_num}")
                ser6.flush()
                ser6.close()
                time.sleep(.25)
                ser6 = serial.Serial('/dev/ttyUSB5',9600,timeout=1)
                time.sleep(.25)
            case 7:
                print(f"Resetting port {reader_num}")
                ser7.flush()
                ser7.close()
                time.sleep(.25)
                ser7 = serial.Serial('/dev/ttyUSB6',9600,timeout=1)
                time.sleep(.25)
            case 8:
                print(f"Resetting port {reader_num}")
                ser8.flush()
                ser8.close()
                time.sleep(.25)
                ser8 = serial.Serial('/dev/ttyUSB7',9600,timeout=1)
                time.sleep(.25)
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
                reader_board_mem[0] = data
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
                reader_board_mem[1] = data
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
                reader_board_mem[2] = data
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
                reader_board_mem[3] = data
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
                reader_board_mem[4] = data
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
                reader_board_mem[5] = data
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
                reader_board_mem[6] = data
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
                reader_board_mem[7] = data
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            ser8.flush()
            time.sleep(0.25)

White_Pieces = {
    '1'         :  chess.Pawn(0,0,0,chess.board),
    '2'         :  chess.Pawn(0,0,0,chess.board),
    '3'         :  chess.Pawn(0,0,0,chess.board),
    '4'         :  chess.Pawn(0,0,0,chess.board),
    '5'         :  chess.Pawn(0,0,0,chess.board),
    '6'         :  chess.Pawn(0,0,0,chess.board),
    '7'         :  chess.Pawn(0,0,0,chess.board),
    '8'         :  chess.Pawn(0,0,0,chess.board),
    '33bc6e'    :  chess.Queen(0,0,0,chess.board),
    'b82c5e12'  :  chess.King(0,0,0,chess.board),
    'd36db3e'   :  chess.Horse(0,0,0,chess.board),
    'a574660'   :  chess.Horse(0,0,0,chess.board),
    '1a3a9c81'  :  chess.Bishop(0,0,0,chess.board),
    '11'        :  chess.Bishop(0,0,0,chess.board),
    'a574660'   :  chess.Rook(0,0,0,chess.board),
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
    '6946a318'  :  chess.King(1,0,0,chess.board),
    '27'        :  chess.Horse(1,0,0,chess.board),
    '28'        :  chess.Horse(1,0,0,chess.board),
    '29'        :  chess.Bishop(1,0,0,chess.board),
    '30'        :  chess.Bishop(1,0,0,chess.board),
    '31'        :  chess.Rook(1,0,0,chess.board),
    '32'        :  chess.Rook(1,0,0,chess.board)
}

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

White_AI = {
    'switch'        :   False,
    'difficulty'    :   3
}

Black_AI = {
    'switch'        :   False,
    'difficulty'    :   3
}

def chess_piece_logic(piece, color):
    chess.clear_all_lists(chess.board)
    chess.find_all_poss_moves(chess.board)
    # chess.legal_king_moves(chess.board, color)
    # chess.check_pin(chess.board, piece)
    
BUTTON = False
def white_move():
    global BUTTON
    global game_state
    global piece
    global piece_ID
    
    with threading.Lock():
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
            with threading.Lock():
                temp_reader_board_mem = reader_board_mem[:]  
            time.sleep(.25)
            
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
                            
            if BUTTON == True:
                if White_AI['switch']:
                    game_state = 4
                    return
                else:
                    BUTTON = False
                    return

        print("White_move_state 2")
        #State 3: Monitor board state, look for the lifted piece. 
        while not any(piece_ID['UID'] in sublist for sublist in temp_reader_board_mem):
            temp_reader_board_mem = reader_board_mem[:]
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
        chess.print_board(chess.board)

        return

def white_move_AI():
    global BUTTON
    global internal_board_mem
    global game_state
    with threading.Lock():
        internal_board_mem = reader_board_mem
    update_chess_positions(internal_board_mem)
    chess.print_board(chess.board)
    chess.white_ai_skill = 1
    move,tup = chess.get_best_move(chess.board, 0)
    print (tup)
    #Turn on light
    # while True:
    #     #State 1: Monitor board state, check button state
    #     while (temp_reader_board_mem == internal_board_mem):
    #         with threading.Lock():
    #             temp_reader_board_mem = reader_board_mem
    #         update_chess_positions(temp_reader_board_mem)
    #         time.sleep(0.25)
    #         #If button is pressed, return.
    
ready()
time.sleep(5)
# white_move_AI()
# while True:
#     print("Reader UIDs")
#     for i in range(0,8):
#         print(reader_board_mem[i])
#     print("\n")
    
#     time.sleep(0.5)
    
while(white_move() == -1):
    pass


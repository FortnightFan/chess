import chess
import serial
import threading
import time
"""
Find difficulty values of AI. 
    - OFF
    - EASY      - Skill = 5
    - NORMAL    - Skill = 10
    - HARD      - Skill = 18
"""

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

"""
Initialization function
Modifies variables
    -ser1,ser2,ser3
"""
ser1,ser2,ser3 = None,None,None
def ready():
    global ser1,ser2,ser3
    #Arduino serial ports and threads
    try:
        ser1 = serial.Serial('/dev/ttyUSB0',9600)
        ser2 = serial.Serial('/dev/ttyUSB1',9600)
        ser3 = serial.Serial('/dev/ttyUSB2',9600)
        print("Serial ports successfully connected.")
    except:
        print("ERROR: Serial port(s) not found")

    reader_thread_1 = threading.Thread(target=read_port_1)
    reader_thread_1.daemon = True
    reader_thread_2 = threading.Thread(target=read_port_2)
    reader_thread_2.daemon = True
    reader_thread_3 = threading.Thread(target=read_port_3)
    reader_thread_3.daemon = True
    
    io_thread = threading.Thread(target=io_control)    
        
    # game_thread = threading.Thread(target=game_control)
    
    reader_thread_1.start()
    reader_thread_2.start()
    reader_thread_3.start()
    io_thread.start()
    # game_thread.start()

def exit():    
    try:
        ser1.close()
        ser2.close()
        ser3.close()
        print("Serial ports successfully closed.")
    except:
        print("ERROR: Port(s) not found") 


"""
Arduino/RFID Reader Functions
Modifies variables:
    -reader_board_mem
"""
reader_board_mem = chess.board  #Variable that stores immediate reference data of on-board pieces.

def deserialize (serialized_data):
    ser_data = serialized_data.split("/")
    return ser_data[0],ser_data[1]

def read_port_1():
    global reader_board_mem
    while True:
        try:
            data = ser1.readline().decode('ascii').strip()
            reader,data = deserialize(data)
            print(f"Reader: {int(reader)+2}\nData: {data}")
            ser1.flushInput()
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except:
            print("ERROR: Signal downlink 1")
            time.sleep(3)
        finally:
            time.sleep(0.25)
    pass
def read_port_2():
    global reader_board_mem
    while True:
        time.sleep(0.25)
    pass
def read_port_3():
    global reader_board_mem
    while True:
        time.sleep(0.25)
    pass
def read_port_4():
    global reader_board_mem
    while True:
        time.sleep(0.25)
    pass
def read_port_5():
    global reader_board_mem
    while True:
        time.sleep(0.25)
    pass
def read_port_6():
    global reader_board_mem
    while True:
        time.sleep(0.25)
    pass
def read_port_7():
    global reader_board_mem
    while True:
        time.sleep(0.25)
    pass
def read_port_8():
    global reader_board_mem
    while True:
        time.sleep(0.25)
    pass

"""
Controls on-board buttons, switches, etc. 
Modifies variables:
    -White_AI
    -Black_AI
    -game_state
"""
def io_control():
    while True:
        time.sleep(0.25)
    pass    

game_state_dict = {
        "White_turn" : 0,
        "Black_turn" : 1,
        "White_turn_check" : 2,
        "Black_turn_check" : 3,
        "White_turn_AI" : 4,
        "Black_turn_AI" : 5,
        "White_checkmate" : 6,
        "Black_checkmate" : 7,
        "Stalemate" : 8
    }
game_state = game_state_dict["White_turn"]

def game_control():    
    time.sleep(5)   #Get board readings
    chess.board = reader_board_mem
    board_mem = reader_board_mem
    
    # chess.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # while(1):
    #     chess.print_board(chess.board)
    #     time.sleep(1)

if __name__ == "__main__":
    ready()
    game_control()
    pass
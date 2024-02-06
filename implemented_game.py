import chess
import serial
import threading
import time
import queue

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

Piece_Queue = queue.Queue()

"""
Initialization function
Modifies variables
    -ser1,ser2,ser3
    -reader_thread_1,reader_thread_2,reader_thread_3
"""
ser1,ser2,ser3 = None,None,None
reader_thread_1,reader_thread_2,reader_thread_3 = None,None,None

def ready():
    global ser1,ser2,ser3
    global reader_thread_1,reader_thread_2,reader_thread_3
    
    #Arduino serial ports and threads
    try:
        ser1 = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
        reader_thread_1 = threading.Thread(target=read_port_1)
        reader_thread_1.daemon = True
        print("Serial port 1 successfully connected.")
    except serial.SerialException:
        ser1 = serial.Serial('COM4', 9600,timeout=1)
        reader_thread_1 = threading.Thread(target=read_port_1)
        reader_thread_1.daemon = True
        print("Serial port 1 successfully connected.")
    except:
        print("ERROR: Serial port 1 not found")
    try:
        ser2 = serial.Serial('/dev/ttyUSB1',9600,timeout=1)
        reader_thread_2 = threading.Thread(target=read_port_2)
        reader_thread_2.daemon = True
        print("Serial port 2 successfully connected.")
    except:
        print("ERROR: Serial port 2 not found")
    try:
        ser3 = serial.Serial('/dev/ttyUSB2',9600,timeout=1),
        reader_thread_3 = threading.Thread(target=read_port_3)
        reader_thread_3.daemon = True
        print("Serial port 3 successfully connected.")
    except:
        print("ERROR: Serial port 3 not found")
    
    if reader_thread_1 != None:
        reader_thread_1.start()
    if reader_thread_2 != None:
        reader_thread_2.start()
    if reader_thread_3 != None:
        reader_thread_3.start()
        
    io_thread = threading.Thread(target=io_control)    
    io_thread.daemon = True
    io_thread.start()

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
    ret_list = ["","","","","","",""]
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
    #     when button is pressed
    #         print(1)
    # pass    

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

def board_setup():
    global reader_board_mem
    while(True):
        UID = Piece_Queue.get()
        if UID in reader_board_mem:
            pass
        time.sleep(1)
        pass

def game_control():    
    chess.board = reader_board_mem
    board_mem = reader_board_mem
    print("End")
    # chess.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # while(1):
    #     chess.print_board(chess.board)
    #     time.sleep(1)

if __name__ == "__main__":
    ready()
    time.sleep(20)    
    exit()
    pass


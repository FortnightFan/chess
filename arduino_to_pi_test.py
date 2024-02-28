import chess
import serial
import threading
import time
# import queue
import copy

"""
Reader communication testing
"""


reader_board_mem = [["" for _ in range(8)] for _ in range(8)]  #Variable that stores immediate reference data of on-board pieces. Updated constantly.

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
        reader_thread_6 = threading.Thread(target=read_port_6)
        reader_thread_6.daemon = True
        print("Serial port 6 successfully connected.")
        reader_thread_6.start()
    except:
        print("ERROR: Serial port 6 not found")
        
    try:
        ser3 = serial.Serial('/dev/ttyUSB6',9600,timeout=1),
        reader_thread_7 = threading.Thread(target=read_port_7)
        reader_thread_7.daemon = True
        print("Serial port 7 successfully connected.")
        reader_thread_7.start()
    except:
        print("ERROR: Serial port 7 not found")
        
    try:
        ser3 = serial.Serial('/dev/ttyUSB7',9600,timeout=1),
        reader_thread_8 = threading.Thread(target=read_port_8)
        reader_thread_8.daemon = True
        print("Serial port 8 successfully connected.")
        reader_thread_8.start()
    except:
        print("ERROR: Serial port 8 not found")


def deserialize (serialized_data):
    ret_list = ["","","","","","","",""]
    ser_data = serialized_data.split(", ")
    for i in range (0,8):
        if len(ser_data[i]) != 8:
            print("ERROR: Incorrect data sizing")
            return ret_list
        else:
            ret_list[i] = ser_data[i]
    return ret_list

def read_port_1():
    global reader_board_mem
    while True:
        try:
            data = ser1.readline().decode('utf-8').strip()    
            if data:   
                data = deserialize(data)
                for i in range (0,8):
                    reader_board_mem[i][0] = data[i]
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
        try:
            data = ser2.readline().decode('utf-8').strip()    
            if data:   
                data = deserialize(data)
                for i in range (0,8):
                    reader_board_mem[i][1] = data[i]
                ser2.flushInput()
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
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

White_Pieces = {
    '1'   :  chess.Pawn(0,0,0,chess.board),
    '2'   :  chess.Pawn(0,0,0,chess.board),
    '3'   :  chess.Pawn(0,0,0,chess.board),
    '4'   :  chess.Pawn(0,0,0,chess.board),
    '5'   :  chess.Pawn(0,0,0,chess.board),
    '6'   :  chess.Pawn(0,0,0,chess.board),
    '7'   :  chess.Pawn(0,0,0,chess.board),
    '8'   :  chess.Pawn(0,0,0,chess.board),
    '9'   :  chess.Queen(0,0,0,chess.board),
    '10'   :  chess.King(0,0,0,chess.board),
    '11'   :  chess.Horse(0,0,0,chess.board),
    '12'   :  chess.Horse(0,0,0,chess.board),
    '13'   :  chess.Bishop(0,0,0,chess.board),
    '14'   :  chess.Bishop(0,0,0,chess.board),
    '15'   :  chess.Rook(0,0,0,chess.board),
    '16'   :  chess.Rook(0,0,0,chess.board)
}

Black_Pieces = {
    '17'   :  chess.Pawn(1,0,0,chess.board),
    '18'   :  chess.Pawn(1,0,0,chess.board),
    '19'   :  chess.Pawn(1,0,0,chess.board),
    '20'   :  chess.Pawn(1,0,0,chess.board),
    '21'   :  chess.Pawn(1,0,0,chess.board),
    '22'   :  chess.Pawn(1,0,0,chess.board),
    '23'   :  chess.Pawn(1,0,0,chess.board),
    '24'   :  chess.Pawn(1,0,0,chess.board),
    '25'   :  chess.Queen(1,0,0,chess.board),
    '26'   :  chess.King(1,0,0,chess.board),
    '27'   :  chess.Horse(1,0,0,chess.board),
    '28'   :  chess.Horse(1,0,0,chess.board),
    '29'   :  chess.Bishop(1,0,0,chess.board),
    '30'   :  chess.Bishop(1,0,0,chess.board),
    '31'   :  chess.Rook(1,0,0,chess.board),
    '32'   :  chess.Rook(1,0,0,chess.board)
}

def update_chess_positions(reader_board_mem):
    for i in range (0,8):
        for j in range (0,8):
            if reader_board_mem[i][j] == "" or reader_board_mem[i][j] == "00000000":
                chess.board[i][j] = chess.tile
            elif reader_board_mem[i][j] in White_Pieces:
                chess.move_piece(chess.board, White_Pieces[reader_board_mem[i][j]], (j,i))
            elif reader_board_mem[i][j] in Black_Pieces:
                chess.move_piece(chess.board, Black_Pieces[reader_board_mem[i][j]], (j,i))

ready()
while True:
    print("Reader UIDs")
    for i in range(0,8):
        print(reader_board_mem[i])
    print("\n")
    
    print("Chess board")
    update_chess_positions(reader_board_mem)
    chess.print_board(chess.board)
    print("\n")
    
    time.sleep(0.5)
    

import chess
import serial
import threading
import time
# import queue
import copy

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
        if len(ser_data[i]) < 200:
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
                    reader_board_mem[0][i] = data[i]
                ser1.flushInput()
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            time.sleep(0.1)

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


ready()
while True:
    for i in range(0,8):
        print(reader_board_mem[i])
    print("\n")
    time.sleep(0.5)
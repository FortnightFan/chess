import serial
import time
import platform
import threading

uid = "B8437812"

system = platform.system()
if (system == "Windows"):
    ser1 = serial.Serial('COM4',9600)
    ser2 = serial.Serial('COM7',9600)
elif (system == "Linux"):
    ser1 = serial.Serial('/dev/ttyUSB0',9600)
    ser2 = serial.Serial('/dev/ttyUSB1',9600)
    # ser3 = serial.Serial('/dev/ttyUSB2',9600)
    #/dev/ttyUSB0, /dev/ttyUSB1, top blue port
    #access devices using ls /dev/*USB*
else:
    print("ERROR")
    exit()

def deserialize (serialized_data):
    ser_data = serialized_data.split("/")
    return ser_data[0],ser_data[1]

def read_port_1():
    while True:
        try:
            data = ser1.readline().decode('ascii').strip()
            reader,data = deserialize(data)
            print(f"Reader: {int(reader)+2}\nData: {data}")
            ser1.flushInput()
        except UnicodeDecodeError:
            print("initializing...")

def read_port_2():
    while True:
        try:
            data = ser2.readline().decode('ascii').strip()
            reader,data = deserialize(data)
            print(f"Reader: {int(reader)}\nData: {data}")
            ser2.flushInput()
        except UnicodeDecodeError:
            print("initializing...")

# def read_port_3():
#     while True:
#         try:
#             data = ser3.readline().decode('ascii').strip()
#             reader,data = deserialize(data)
#             print(f"Reader: {int(reader)}\nData: {data}")
#             ser3.flushInput()
#         except UnicodeDecodeError:
#             print("initializing...")

thread1 = threading.Thread(target=read_port_1)
thread2 = threading.Thread(target=read_port_2)
# thread3 = threading.Thread(target=read_port_3)

try:
    # Start threads
    thread1.start()
    thread2.start()
    # thread3.start()
    while True:
        time.sleep(1)
    # Keep the main thread alive


except KeyboardInterrupt:
    thread1.join()
    thread2.join()
    # thread3.join()
    ser1.close()
    ser2.close()
    # ser3.close()
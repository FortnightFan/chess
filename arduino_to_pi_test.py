import serial
import time
import platform
system = platform.system()
if (system == "Windows"):
    ser = serial.Serial('COM3',9600)
elif (system == "Linux"):
    ser = serial.Serial('/dev/ttyACM0',9600)
else:
    print("ERROR")
    exit()



def deserialize (serialized_data):
    if serialized_data[0] == '/':
        return serialized_data[1:]

try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        data = deserialize(data)
        print(data)
        time.sleep(1)
except KeyboardInterrupt:
    ser.close()
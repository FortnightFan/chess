import serial
import time
import platform
system = platform.system()
if (system == "Windows"):
    ser1 = serial.Serial('COM4',9600)
    ser2 = serial.Serial('COM5',9600)
elif (system == "Linux"):
    ser1 = serial.Serial('/dev/ttyUSB0',9600)
    ser2 = serial.Serial('/dev/ttyUSB1',9600)
    #/dev/ttyUSB0, /dev/ttyUSB1, top blue port
    #access devices using ls /dev/*USB*
else:
    print("ERROR")
    exit()

def deserialize (serialized_data):
    if serialized_data[0] == '/':
        return serialized_data[1:]

try:
    while True:
        #Recieve and read data
        # data = ser2.readline().decode('utf-8').strip()
        # data = deserialize(data)
        # print(data)
        # data = ser1.readline().decode('utf-8').strip()
        # data = deserialize(data)
        # print(data)
        # time.sleep(1)

        #Send data
        ser1.write("/turn_off_led".encode())
except KeyboardInterrupt:
    ser1.close()
    ser2.close()
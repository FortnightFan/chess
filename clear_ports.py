import serial.tools.list_ports

def close_all_serial_ports():
    # Get a list of all available serial ports
    ports = serial.tools.list_ports.comports()
    print (ports)
    # Close each serial port
    for port in ports:
        try:
            ser = serial.Serial(port.device)
            ser.close()
            print(f"Closed serial port: {port.device}")
        except serial.SerialException:
            print(f"Failed to close serial port: {port.device}")

# Call the function to close all serial ports
close_all_serial_ports()

import RPi.GPIO as GPIO
import time

# Defines the number of rows and columns in your matrix
numRows = 8
numCols = 8

# Defines the pins on the Raspberry Pi connected to the rows and columns
#I used the gpio pin out from online. Feel free to change the pins (physical pins)
rowPins = [11, 13, 15, 29, 31, 33, 35, 37]
colPins = [12, 16, 18, 22, 32, 36, 38, 40]

# Defines the 2D array representing the current display state
displayMatrix = [
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
]

def setup():
    # Set up GPIO mode and set row pins as OUTPUT and column pins as INPUT
    GPIO.setmode(GPIO.BOARD)
    for row_pin in rowPins:
        GPIO.setup(row_pin, GPIO.OUT)
    for col_pin in colPins:
        GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    try:
        # Loop through each column
        for col in range(numCols):
            # Activate the current column
            GPIO.setup(colPins[col], GPIO.OUT)
            GPIO.output(colPins[col], GPIO.LOW)

            # Loop through each row in the current column
            for row in range(numRows):
                # Turn on or off the LED at the current row and column based on the display matrix
                GPIO.output(rowPins[row], displayMatrix[row][col])
                time.sleep(0)  # Adjust this delay as needed for brightness control (flashes with delay on)

                # Turns off the LED at the current row and column
                GPIO.output(rowPins[row], GPIO.LOW)

            # Deactivate the current column for the next iteration
            GPIO.setup(colPins[col], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    except KeyboardInterrupt:
        # Cleanup GPIO on keyboard interrupt (I saw ctr C should close the program)
        GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        # Cleanup GPIO on keyboard interrupt (I saw ctr C should close the program)
        GPIO.cleanup()

# import RPi.GPIO as GPIO
import GPIO
import time

def update_matrix(led_board):

    # Defines the number of rows and columns in your matrix
    numRows = 8
    numCols = 8

    # Defines the pins on the Raspberry Pi connected to the rows and columns
    rowPins = [4, 17, 27, 22, 5, 6, 13, 19]
    colPins = [26, 21, 20, 16, 12, 25, 24, 23]

    # Set up GPIO
    GPIO.setmode(GPIO.BCM)

    # Sets row pins as OUTPUT and column pins as INPUT
    for row_pin in rowPins:
        GPIO.setup(row_pin, GPIO.OUT)

    for col_pin in colPins:
        GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        while True:
            # Loops through each column
            for col in range(numCols):
                # Activates the current column
                GPIO.setup(colPins[col], GPIO.OUT)
                GPIO.output(colPins[col], GPIO.LOW)

                # Loops through each row in the current column
                for row in range(numRows):
                    # Turn on or off the LED at the current row and column based on the display matrix
                    GPIO.output(rowPins[row], led_board[row][col])
                    time.sleep(0)  # Adjust this sleep as needed for brightness control (flashes with delay on)

                    # Turns off the LED at the current row and column
                    GPIO.output(rowPins[row], GPIO.LOW)

                # Deactivate the current column for the next iteration
                GPIO.setup(colPins[col], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    except Exception as e:
        print (f"ERROR: {e}")
    finally:
        GPIO.cleanup()


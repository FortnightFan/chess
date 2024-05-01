import RPi.GPIO as GPIO
import time
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

# Function to setup GPIO pin for button input
global device
global timer1, timer2, active_timer, last_button_press

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)
timer1 = 60  # Initialize timer1 with 60 seconds
timer2 = 60  # Initialize timer2 with 60 seconds
active_timer = None
last_button_press = time()

    # Callback function for button press
def handle_button_press(channel):
    global timer1, timer2, active_timer, last_button_press
    current_time = time.time()
    if current_time - last_button_press < 0.1:  # Debounce manually
        return
    last_button_press = current_time

    if active_timer is None:
        timer1 = 60
        active_timer = 1
    elif active_timer == 1:
        if timer2 is None:
            timer2 = 60
        active_timer = 2
    else:
        active_timer = 1

def display_message(device, message):
    global timer1, timer2, active_timer, last_button_press, active_timer, last_button_press

    # Determine the width of the message in pixels
    text_width = len(message) * 8  # Each character is 8 pixels wide in the default font

        # Calculate the starting position to center the text
    start_pos = max((device.width - text_width) // 2, 0)

        # Display the centered text
    with canvas(device) as draw:
        text(draw, (start_pos, 0), message, fill="white", font=proportional(LCD_FONT))

def run_chess_timer():
    global timer1, timer2, active_timer
    # Function to setup GPIO pin for button input
    def setup_gpio(button_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Initialize GPIO settings and add event detection
    button_pin = 18  # Use GPIO pin 18 for the button
    setup_gpio(button_pin)

    GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=handle_button_press, bouncetime=300)

    display_message(device, "CHESS")

    # Initialize timer variables


    # Main program loop
    while timer1 > 0 and timer2 > 0:
        time.sleep(1)
        if active_timer == 1:
            timer1 -= 1
            display_message(device, f"W: {timer1}")
        elif active_timer == 2:
            timer2 -= 1
            display_message(device, f"B: {timer2}")
    winner = "B wins!" if timer1 <= 0 else "W wins!"
    display_message(device, winner)
    time.sleep(10)
    GPIO.cleanup()  # Clean up GPIO to ensure a proper shutdown

# Call the function to run the chess timer
run_chess_timer()
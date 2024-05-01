import time
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

def scroll_text(device, text_to_scroll):
    # Define the scroll speed (adjust as needed)
    scroll_speed = 0.1  # Adjust scroll speed (lower value = faster scroll)

    # Calculate the width of the text
    text_width = len(text_to_scroll) * 8  # Each character is 8 pixels wide in the default font

    # Initialize the scroll position
    x = device.width

    # Start scrolling loop
    while True:
        # Clear the canvas
        with canvas(device) as draw:
            # Draw the text at the current position
            text(draw, (x, 0), text_to_scroll, fill="white", font=proportional(LCD_FONT))
        
        # Move the text position to the left
        x -= 1
        
        # If the entire text has scrolled off the display, reset the position to the right
        if x < -text_width:
            x = device.width
        
        # Pause to control the scroll speed
        time.sleep(scroll_speed)

def main():
    # Initialize the MAX7219 LED matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90)

    # Define the text to display
    text_to_display = "Design Day Demo - Team CHESS"

    # Start scrolling the text
    while True:
        scroll_text(device, text_to_display)

if __name__ == "__main__":
    main()

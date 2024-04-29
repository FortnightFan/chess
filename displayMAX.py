import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# Raspberry Pi pin configuration:
CS_PIN = 8
CLK_PIN = 11
DATA_PIN = 10

# Timer duration in seconds (60 seconds)
timer_duration = 60

def display_time(device, remaining_time):
    minutes = remaining_time // 60
    seconds = remaining_time % 60

    time_str = "{:02d}:{:02d}".format(minutes, seconds)

    with canvas(device) as draw:
        draw.text((0, 0), time_str, fill="white")

def main():
    # Initialize SPI connection
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=90)

    # Start the timer
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        remaining_time = max(0, timer_duration - int(elapsed_time))

        if remaining_time == 0:
            with canvas(device) as draw:
                draw.text((0, 0), "Time up", fill="white")
            break

        display_time(device, remaining_time)
        time.sleep(0.5)  # Update display every 0.5 seconds

if __name__ == "__main__":
    main()

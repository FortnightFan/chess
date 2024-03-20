# import GPIO #dummy import for testing
import time
import threading

EASY = 5
NORMAL = 10
HARD = 18

White_AI = {
    'switch'        :   False,
    'difficulty'    :   EASY
}

Black_AI = {
    'switch'        :   False,
    'difficulty'    :   EASY
}

BUTTON = False
SWITCH_TURN = False
import RPi.GPIO as GPIO
def io_control():
    global SWITCH_TURN
    global BUTTON
    global game_state
    GPIO.setmode(GPIO.BCM)
    button_pin = 18  # Example GPIO pin
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    button_pressed_time = None
    difficulty_levels = ["OFF", EASY, NORMAL, HARD]
    black_difficulty = 0    #Index
    white_difficulty = 0    #index
    try:
        while True:
            if GPIO.input(button_pin) == GPIO.LOW:  # Button pressed
                if button_pressed_time is None:
                    button_pressed_time = time.time()
                    print('button_pressed')
            else:
                if button_pressed_time is not None:
                    press_duration = time.time() - button_pressed_time
                    if press_duration < 1:
                        SWITCH_TURN = True
                        print("Turn switch")
                    else:
                        # Long press - change difficulty
                        if game_state == 0 or game_state == 2 or game_state == 4: #If white's turn
                            white_difficulty = (white_difficulty + 1) % len(difficulty_levels)
                            if type(white_difficulty) == int:
                                White_AI['difficulty'] = difficulty_levels[white_difficulty]
                                White_AI['switch'] = True
                                BUTTON = True
                            else:
                                White_AI['switch'] = False
                        elif game_state == 1 or game_state == 3 or game_state == 5: #If black's turn
                            black_difficulty = (black_difficulty + 1) % len(difficulty_levels)
                            if type(black_difficulty) == int:
                                Black_AI['difficulty'] = difficulty_levels[black_difficulty]
                                Black_AI['switch'] = True
                                BUTTON = True
                    button_pressed_time = None  # Reset timer
            time.sleep(0.5)
    finally:
        GPIO.cleanup() 

reader_thread = threading.Thread(target=io_control)
reader_thread.daemon = True
while True:
    if BUTTON:
        BUTTON = False
        pass
    if SWITCH_TURN:
        SWITCH_TURN = False
        pass
    print(f"White\n {White_AI}")
    print(f"Black\n {Black_AI}\n\n")
    time.sleep(1)


# led_board = [[0 for _ in range(8)] for _ in range(8)]   #Variable that stores the values for the 8x8 led matrices.

# def set_leds(tuples_list):
#     global led_board
#     if tuples_list == None:
#         led_board = [[0 for _ in range(8)] for _ in range(8)]
#     else:
#          for i in range (0,len(tuples_list)):
#             x,y = tuples_list[i]    
#             led_board[y][x] = 1 
             
# for i in range(0, len(led_board)):
#     print(led_board[i])
# print('\nSetting led values\n')
# set_leds([(0,1), (2,0), (7,3), (4,4)])

# for i in range(0, len(led_board)):
#     print(led_board[i])

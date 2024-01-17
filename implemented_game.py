from chess import *

"""
Find difficulty values of AI. 
    - OFF
    - EASY      - Skill = 5
    - NORMAL    - Skill = 10
    - HARD      - Skill = 18
"""



#Variable to track current state of the game.
global STATE

"""
Ready function is called once on start-up.

RETURN: void
"""

def ready():
    fish_init()     #Initialize stockfish variables
    pass
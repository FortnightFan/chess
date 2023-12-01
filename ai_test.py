import time
from stockfish import Stockfish
import os
import platform
from chess import *


# Checks OS and executes appropriate executable
system = platform.system()
if (system == "Windows"):
    script_directory = os.path.dirname(os.path.abspath(__name__))
    stockfish_path = os.path.join(script_directory, "stockfish-windows-x86-64-avx2.exe")   
    stockfish = Stockfish(path=stockfish_path)

elif (system == "Linux"):
    stockfish = Stockfish('stockfish')
else:
    print("ERROR")
    exit()
    
stockfish.update_engine_parameters({"Hash": 32})

def ai_testbench(depth):
    stockfish.set_depth(depth)

    start_time = time.time()
    stockfish.set_skill_level(10)
    stockfish.set_fen_position("r1bqk2r/pppp1pp1/2nb1n1p/4p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 0 6")
    #sstockfish.get_best_move()
    print(stockfish.get_best_move())

    end_time = time.time()
    print(f"Depth: {depth}")
    print(f"Execution time: {(end_time - start_time):.5f} seconds")

ai_testbench(1)
ai_testbench(5)
ai_testbench(7)
ai_testbench(9)
ai_testbench(12)
ai_testbench(15)
# ai_testbench(20)
# ai_testbench(25)

def example_ai_move_testbench():
    fen_to_board("4k3/3r4/8/1B6/2p2pP1/5P2/8/4K3 w - - 0 1")
    
    for i, row in enumerate(board):
        print(8-i, end="  ")
        for j in row:
            print(j, end=" ")
        print()
    print("   A  B  C  D  E  F  G  H")

    fish_init()
    get_best_move(board, 0)

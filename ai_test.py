import time
from stockfish import Stockfish
import os
import platform


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
    


start_time = time.time()

stockfish.set_skill_level(1)
stockfish.set_depth(7)
stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
print(stockfish.get_best_move())

end_time = time.time()

print(f"Script execution time: {(end_time - start_time):.2f} seconds")
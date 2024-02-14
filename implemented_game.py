import chess
import serial
import threading
import time
# import queue
import copy

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

Button_Pressed = False

White_Pieces = {
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Pawn(0,0,0,chess.board),
    ''   :  chess.Queen(0,0,0,chess.board),
    ''   :  chess.King(0,0,0,chess.board),
    ''   :  chess.Horse(0,0,0,chess.board),
    ''   :  chess.Horse(0,0,0,chess.board),
    ''   :  chess.Bishop(0,0,0,chess.board),
    ''   :  chess.Bishop(0,0,0,chess.board),
    ''   :  chess.Rook(0,0,0,chess.board),
    ''   :  chess.Rook(0,0,0,chess.board)
}

Black_Pieces = {
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Pawn(1,0,0,chess.board),
    ''   :  chess.Queen(1,0,0,chess.board),
    ''   :  chess.King(1,0,0,chess.board),
    ''   :  chess.Horse(1,0,0,chess.board),
    ''   :  chess.Horse(1,0,0,chess.board),
    ''   :  chess.Bishop(1,0,0,chess.board),
    ''   :  chess.Bishop(1,0,0,chess.board),
    ''   :  chess.Rook(1,0,0,chess.board),
    ''   :  chess.Rook(1,0,0,chess.board)
}

"""
Initialization function
Modifies variables
    -ser1,ser2,ser3
    -reader_thread_1,reader_thread_2,reader_thread_3
"""
ser1,ser2,ser3 = None,None,None
reader_thread_1,reader_thread_2,reader_thread_3 = None,None,None

def ready():
    global ser1,ser2,ser3
    global reader_thread_1,reader_thread_2,reader_thread_3
    
    #Arduino serial ports and threads
    try:
        ser1 = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
        reader_thread_1 = threading.Thread(target=read_port_1)
        reader_thread_1.daemon = True
        print("Serial port 1 successfully connected.")
    # except serial.SerialException:
    #     ser1 = serial.Serial('COM4', 9600,timeout=1)
    #     reader_thread_1 = threading.Thread(target=read_port_1)
    #     reader_thread_1.daemon = True
    #     print("Serial port 1 successfully connected.")
    except:
        print("ERROR: Serial port 1 not found")
    try:
        ser2 = serial.Serial('/dev/ttyUSB1',9600,timeout=1)
        reader_thread_2 = threading.Thread(target=read_port_2)
        reader_thread_2.daemon = True
        print("Serial port 2 successfully connected.")
    except:
        print("ERROR: Serial port 2 not found")
    try:
        ser3 = serial.Serial('/dev/ttyUSB2',9600,timeout=1),
        reader_thread_3 = threading.Thread(target=read_port_3)
        reader_thread_3.daemon = True
        print("Serial port 3 successfully connected.")
    except:
        print("ERROR: Serial port 3 not found")
    
    if reader_thread_1 != None:
        reader_thread_1.start()
    if reader_thread_2 != None:
        reader_thread_2.start()
    if reader_thread_3 != None:
        reader_thread_3.start()
        
    io_thread = threading.Thread(target=io_control)    
    io_thread.daemon = True
    io_thread.start()

def exit():    
    try:
        ser1.close()
        ser2.close()
        ser3.close()
        print("Serial ports successfully closed.")
    except:
        print("ERROR: Port(s) not found") 


"""
Arduino/RFID Reader Functions
Modifies variables:
    -reader_board_mem
"""
reader_board_mem = [["" for _ in range(8)] for _ in range(8)]  #Variable that stores immediate reference data of on-board pieces. Updated constantly.
internal_board_mem = copy.deepcopy(reader_board_mem) #Variable that references the reader board for logic. Updated only on events
def deserialize (serialized_data):
    ret_list = ["","","","","","","",""]
    ser_data = serialized_data.split(" ")
    for i in range (0,len(ser_data)):
        tup = ser_data[i].split("/")
        ret_list[int(tup[0])-1] = tup[1]
    return ret_list

def read_port_1():
    global reader_board_mem
    while True:
        try:
            data = ser1.readline().decode('ascii').strip()    
            if data:   
                data = deserialize(data)
                print(data)
                for i in range (0,8):
                    reader_board_mem[0][i] = data[i]
                ser1.flushInput()
        except UnicodeDecodeError:
            print("ERROR: Unicode decode")
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            time.sleep(0.25)

def read_port_2():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_3():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_4():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_5():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_6():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_7():
    global reader_board_mem
    while True:
        time.sleep(0.25)
def read_port_8():
    global reader_board_mem
    while True:
        time.sleep(0.25)

"""
Controls on-board buttons, switches, etc. 
Modifies variables:
    -White_AI
    -Black_AI
    -game_state
"""
def io_control():
    while True:
        time.sleep(0.25)

# game_state_dict = {
#         "White_turn" : 0,
#         "Black_turn" : 1,
#         "White_turn_check" : 2,
#         "Black_turn_check" : 3,
#         "White_turn_AI" : 4,
#         "Black_turn_AI" : 5,
#         "White_checkmate" : 6,
#         "Black_checkmate" : 7,
#         "Stalemate" : 8
#     }

game_state = 0

#State machine that constantly runs. game_state var must be updated within functions.
def game_control():  
    global internal_board_mem
    global reader_board_mem 
    chess.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")  #Testing, delete later
    chess.init(chess.board)
    while True:
        internal_board_mem = reader_board_mem
        match game_state:
            case 0:
                white_move()
            case 1:
                black_move()
            case 2:
                white_move_check()
            case 3:
                black_move_check()
            case 4:
                white_move_AI()
            case 5:
                black_move_AI()
            case 6:
                white_checkmate()
            case 7:
                black_checkmate()
            case 8:
                stalemate()
    # while(1):
    #     chess.print_board(chess.board)
    #     time.sleep(1)

"""
GAME-LOGIC HELPER FUNCTIONS
"""
#Updates the board within the chess class to reflect the value of the matrix
def update_chess_positions(reader_board_mem):
    for i in range (0,8):
        for j in range (0,8):
            if reader_board_mem[i][j] == "":
                chess.board[i][j] = chess.tile
            elif reader_board_mem[i][j] in White_Pieces:
                chess.move_piece(chess.board, White_Pieces[reader_board_mem[i][j]], (i,j))
            elif reader_board_mem[i][j] in Black_Pieces:
                chess.move_piece(chess.board, Black_Pieces[reader_board_mem[i][j]], (i,j))
                
#Finds all possible moves on the board specifically for a given piece.
def chess_piece_logic(piece, color):
    chess.clear_all_lists(chess.board)
    chess.find_all_poss_moves(chess.board)
    chess.legal_king_moves(chess.board, color)
    chess.check_pin(chess.board, piece)

"""
Game-state functions
"""
def white_move():
    temp_reader_board_mem = reader_board_mem
    internal_board_mem = reader_board_mem
    exit = False
    
    global piece
    piece = chess.tile
    while True: #Update to button inputs
        #if button inputs ai or whatever, update state and return
        while not exit:
            while (temp_reader_board_mem == internal_board_mem):
                temp_reader_board_mem = reader_board_mem
                update_chess_positions(temp_reader_board_mem)
                time.sleep(0.25)

            for i in range (0,8):
                for j in range (0,8):
                    if temp_reader_board_mem[i][j] != internal_board_mem[i][j]:
                        try:
                            piece = White_Pieces[internal_board_mem[i][j]]
                            if piece.color == 0:
                                exit = True
                                chess_piece_logic(piece, 0)
                                print(piece.poss_moves)
                                #Turn on lights
                        except:
                            print("ERROR: Key index not found")
            
            #Wait for piece to return to the board. Turn lights back off.
            #Update internal_board_mem
            
        return
        
def black_move():
    pass

def white_move_check():
    pass

def black_move_check():
    pass

def white_move_AI():
    pass

def black_move_AI():
    pass
    
def white_checkmate():
    pass

def black_checkmate():
    pass

def stalemate():
    pass
  
if __name__ == "__main__":
    
    chess.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    chess.print_board(chess.board)
    chess.init(chess.board)

    reader_board_mem[6][3] = "2109"
    white_move()
    # ready()
    # game_control()
    # time.sleep(20)    
    # exit()
    
    pass


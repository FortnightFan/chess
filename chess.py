import time
from stockfish import Stockfish
import os
import platform

"""
Chess classes
"""   
        
board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
global white_king_pos
global black_king_pos
white_king_pos = (4,7)
black_king_pos = (4,0)

class Piece:
    def __init__(self,color,xpos,ypos,board):
        self.color = color  # 0 = white, 1 = black, 2 = empty(blank tile)
        self.xpos = xpos    #horizontal position
        self.ypos = ypos    #vertical position
        self.board = board  #reference to game board
        self.has_moved = False  # Indicates whether the piece has moved
        self.poss_moves = []
        self.poss_captures = []
        
    def find_poss_moves(self):
        pass
    
    def clear_lists(self):
        self.poss_moves = []
        self.poss_captures = []

class Tile (Piece):
    def __str__ (self):
        return (f"__")

class Pawn(Piece):
    def __init__(self,color,xpos,ypos,board):
        super().__init__(color,xpos,ypos,board)
        self.has_moved = False
        self.poss_moves = []
        self.poss_captures = []        
    
    def __str__(self):  #string formatting
        if self.color == 0:
            return (f"PW")
        elif self.color == 1:
            return (f"PB")
    
    def find_poss_moves(self):   #returns a list of tuples that represent all possible moves.
        x, y = self.xpos, self.ypos
        if self.color == 0: #white
            if not(self.has_moved):                                     #first move can be either 1 or 2 forward
                if self.board[y-2][x] == tile and self.board[y-1][x] == tile:
                    self.poss_moves.append((self.xpos,self.ypos-2))
                    self.poss_moves.append((self.xpos,self.ypos-1))    
            elif self.ypos > 0 and self.board[y-1][x] == tile:
                self.poss_moves.append((self.xpos,self.ypos-1))
            
            if self.xpos == 0 and self.ypos >= 0:               #find possible pawn captures, white
                if self.board[y-1][x+1].color == 1:
                    self.poss_captures.append((x+1,y-1))
            if self.xpos == 7 and self.ypos >= 0:
                if self.board[y-1][x-1].color == 1:
                    self.poss_captures.append((x-1,y-1))           
            elif self.ypos >= 0:
                if self.board[y-1][x-1].color == 1:
                    self.poss_captures.append((x-1,y-1))
                if self.board[y-1][x+1].color == 1:
                    self.poss_captures.append((x+1,y-1))
                
        elif self.color == 1:   #black
            if not(self.has_moved):                                     #first move can be either 1 or 2 forward
                if self.board[y+2][x] == tile and self.board[y+1][x] == tile:
                    self.poss_moves.append((self.xpos,self.ypos+2))
                    self.poss_moves.append((self.xpos,self.ypos+1))
            elif self.ypos < 8 and self.board[y+1][x] == tile:
                self.poss_moves.append((self.xpos,self.ypos+1))
                
            if self.xpos == 0 and self.ypos < 8:                #find possible pawn captures, white
                if self.board[y+1][x+1].color == 0:
                    self.poss_captures.append((x+1,y+1))
            if self.xpos == 7 and self.ypos < 8:
                if self.board[y+1][x-1].color == 0:
                    self.poss_captures.append((x-1,y+1))           
            elif self.ypos < 8:
                if self.board[y+1][x-1].color == 0:
                    self.poss_captures.append((x-1,y+1))
                if self.board[y+1][x+1].color == 0:
                    self.poss_captures.append((x+1,y+1))
        self.poss_captures = list(set(self.poss_captures))    #removes duplicates
        self.poss_moves = list(set(self.poss_moves))    #removes duplicates

    def clear_lists(self):
        self.poss_moves = []
        self.poss_captures = []

class Rook(Piece):
    def __init__(self,color,xpos,ypos,board, has_moved):
        super().__init__(color,xpos,ypos,board)
        self.has_moved = has_moved
        self.poss_moves = []
        self.poss_captures = []      

    def __str__(self):  #string formatting
        if self.color == 0:
            return (f"RW")
        elif self.color == 1:
            return (f"RB")
    
    def find_poss_moves(self):
        if self.color == 0:     #white
            x, y = self.xpos, self.ypos
            while y < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares south
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y += 1

            y = self.ypos
            while y >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares north
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y -= 1

            y = self.ypos
            x = self.xpos
            while x < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares east
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1

            x = self.xpos
            while x >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares west
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
            
        elif self.color == 1:     #black
            x, y = self.xpos, self.ypos
            while y < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares south
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y += 1

            y = self.ypos
            while y >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares north
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y -= 1

            y = self.ypos
            x = self.xpos
            while x < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares east
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1

            x = self.xpos
            while x >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares west
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
            
        self.poss_moves = list(set(self.poss_moves))    #removes duplicates
        if (self.xpos,self.ypos) in self.poss_moves:
            self.poss_moves.remove((self.xpos,self.ypos))

class Bishop(Piece):
    def __str__(self):  #string formatting
        if self.color == 0:
            return (f"BW")
        elif self.color == 1:
            return (f"BB")
    
    def find_poss_moves(self):
        x,y = self.xpos,self.ypos
        if (self.color == 0):       #white
            
            while (x < 8 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  #northeast
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x >= 0 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):   #northwest   
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x < 8 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  #southeast
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y += 1

            x,y = self.xpos,self.ypos
            while (x >= 0 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  #southwest
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y += 1
                
            self.poss_moves = list(set(self.poss_moves))
            self.poss_moves.remove((self.xpos,self.ypos))
            
        elif (self.color == 1):     #black
            
            while (x < 8 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  #northeast
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x >= 0 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):   #northwest   
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x < 8 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  #southeast
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y += 1

            x,y = self.xpos,self.ypos
            while (x >= 0 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  #southwest
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y += 1
                
        self.poss_moves = list(set(self.poss_moves))    
        if (self.xpos,self.ypos) in self.poss_moves:
            self.poss_moves.remove((self.xpos,self.ypos))
        
class Queen(Piece):
    def __str__(self):
        if self.color == 0:
            return "QW"
        elif self.color == 1:
            return "QB"
        
    def find_poss_moves(self):
        x,y = self.xpos,self.ypos
        if (self.color == 0):      
            
            while (x < 8 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  #northeast
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x >= 0 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):   #northwest   
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x < 8 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  #southeast
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y += 1

            x,y = self.xpos,self.ypos
            while (x >= 0 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  #southwest
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y += 1       
                
            x, y = self.xpos, self.ypos
            while y < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares south
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y += 1

            y = self.ypos
            while y >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares north
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y -= 1

            y = self.ypos
            x = self.xpos
            while x < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares east
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1

            x = self.xpos
            while x >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 1):  # checks all squares west
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
            self.poss_moves = list(set(self.poss_moves))  
            self.poss_moves.remove((self.xpos,self.ypos))
        if self.color == 1:
            
            while (x < 8 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  #northeast
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x >= 0 and y >= 0) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):   #northwest   
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y -= 1
                
            x,y = self.xpos,self.ypos
            while (x < 8 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  #southeast
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1
                y += 1

            x,y = self.xpos,self.ypos
            while (x >= 0 and y < 8) and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  #southwest
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                y += 1
            
            x, y = self.xpos, self.ypos
            while y < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares south
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y += 1

            y = self.ypos
            while y >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares north
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y -= 1

            y = self.ypos
            x = self.xpos
            while x < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares east
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x += 1

            x = self.xpos
            while x >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares west
                if self.board[y][x].color == 0:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                
            self.poss_moves = list(set(self.poss_moves))  
            self.poss_moves.remove((self.xpos,self.ypos))
            
class King(Piece):
    def __init__(self,color,xpos,ypos,board, has_moved):
        super().__init__(color,xpos,ypos,board)
        self.has_moved = has_moved
        self.poss_moves = []
        self.poss_captures = []      
        self.can_castle_short = False
        self.can_castle_long = False

    def __str__ (self):
        if self.color == 0:
            return (f"KW")
        elif self.color == 1:
            return (f"KB")
 
    def can_king_castle(self):
        if self.has_moved == True:
            self.can_castle_short = False
            self.can_castle_long = False
        else:
            if self.color == 0:
                if (board[7][5] == tile and board[7][6] == tile and isinstance(board[7][7], Rook)):
                    if (board[7][7].has_moved == False):
                        self.can_castle_short = True
                    else:
                        self.can_castle_short = False
                if (board[7][1] == tile and board[7][2] == tile and board[7][3] == tile and isinstance(board[7][0], Rook)):
                    if (board[7][0].has_moved == False):
                        self.can_castle_long = True
                    else:
                        self.can_castle_long = False
            elif self.color == 1:
                if (board[0][5] == tile and board[0][6] == tile and isinstance(board[0][7], Rook)):
                    if (board[0][7].has_moved == False):
                        self.can_castle_short = True
                    else:
                        self.can_castle_short = False
                if (board[0][1] == tile and board[0][2] == tile and board[0][3] == tile and isinstance(board[0][0], Rook)):
                    if (board[0][0].has_moved == False):
                        self.can_castle_long = True
                    else:
                        self.can_castle_long = False

    def find_poss_moves(self):
        x,y = self.xpos,self.ypos
        temp_poss_moves = [(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y),(x-1,y-1),(x,y-1),(x+1,y-1)]
        
        if self.color == 0:    
            for coord in temp_poss_moves:
                x,y = coord
                if (x < 8 and x >= 0 and y < 8 and y >= 0):    #checking if in bounds
                    if (self.board[y][x] == tile):
                        self.poss_moves.append((x,y))
                    if (self.board[y][x].color == 1):
                        self.poss_captures.append((x,y))
        if self.color == 1:
            for coord in temp_poss_moves:
                x,y = coord
                if (x < 8 and x >= 0 and y < 8 and y >= 0):    #checking if in bounds
                    if (self.board[y][x] == tile):
                        self.poss_moves.append((x,y))
                    if (self.board[y][x].color == 0):
                        self.poss_captures.append((x,y))
                    
class Horse(Piece):
    def __str__ (self):
        if self.color == 0:
            return (f"HW")
        elif self.color == 1:
            return (f"HB")
        
    def find_poss_moves(self):
        x,y = self.xpos,self.ypos
        temp_poss_moves = [(x-2,y+1),(x-2,y-1),(x+2,y+1),(x+2,y-1),(x+1,y+2),(x-1,y+2),(x+1,y-2),(x-1,y-2)]
        
        if self.color == 0:    
            for coord in temp_poss_moves:
                x,y = coord
                if (x < 8 and x >= 0 and y < 8 and y >= 0):    #checking if in bounds
                    if (self.board[y][x] == tile):
                        self.poss_moves.append((x,y))
                    if (self.board[y][x].color == 1):
                        self.poss_captures.append((x,y))
        if self.color == 1:
            for coord in temp_poss_moves:
                x,y = coord
                if (x < 8 and x >= 0 and y < 8 and y >= 0):    #checking if in bounds
                    if (self.board[y][x] == tile):
                        self.poss_moves.append((x,y))
                    if (self.board[y][x].color == 0):
                        self.poss_captures.append((x,y))
                                     
tile = Tile(2,0,0,board)
for i in range (0,8):
    for j in range (0,8):
        board[i][j] = tile

def print_board(board):         #prints status of the board to terminal. 
    print("    0  1  2  3  4  5  6  7")
    for i, row in enumerate(board):
        print(i, end="  ")
        for j in row:
            print(j, end=" ")
        print()
    print()

def add_piece(board, piece):        #adds piece to board. x,y coords are stored inside object
    board[piece.ypos][piece.xpos] = piece

def move_piece(board,piece, pos):  #moves a piece to tuple pos
    global white_king_pos
    global black_king_pos
    ret_val = tile
    x, y = piece.xpos, piece.ypos
    piece.xpos, piece.ypos = pos[0], pos[1]
    
    add_piece(board, piece)
    board[y][x] = tile
    if isinstance(piece, King):
        board[pos[1]][pos[0]].has_moved = True
        if piece.color == 0:
            white_king_pos = (piece.xpos, piece.ypos)
        elif piece.color == 1:
            black_king_pos = (piece.xpos, piece.ypos)
                    
    elif isinstance(piece,(Pawn, Rook)):
        board[pos[1]][pos[0]].has_moved = True

def find_all_poss_moves(board):
    for row in range (0,8):
        for col in range (0,8):
            if not isinstance(board[row][col], Tile):
                board[row][col].find_poss_moves()

def clear_all_lists(board):
    for row in range(0,8):
        for col in range(0,8):
            board[row][col].clear_lists()
            
def piece_testbench(board,piece):       #adds a given piece to the board at location. Board is printed, and possible captures and moves are printed out
    add_piece(board,piece)
    print_board(board)
    print(piece.poss_captures)
    print(piece.poss_moves)

def legal_king_moves(board, color):      #removes illegal king moves
    moves_to_remove = []
    captures_to_remove = []
    
    if (color == 0):
        king = board[white_king_pos[1]][white_king_pos[0]]
        x,y = king.xpos,king.ypos
        for i in range(len(king.poss_moves)):
            move_piece(board,king,king.poss_moves[i])
            if (is_white_in_check(board) == True):
                moves_to_remove.append(i)
            move_piece(board,king, (x,y))
            
        for i in range(len(king.poss_captures)):
            temp = board[king.poss_captures[i][1]][king.poss_captures[i][0]]
            move_piece(board, king, king.poss_captures[i])
            if (is_white_in_check(board) == True):
                captures_to_remove.append(i)     
            move_piece(board, king, (x, y))
            add_piece (board, temp)            

    elif (color == 1):
        king = board[black_king_pos[1]][black_king_pos[0]]
        x,y = king.xpos,king.ypos
        for i in range(len(king.poss_moves)):
            move_piece(board,king,king.poss_moves[i])
            if (is_black_in_check(board) == True):
                moves_to_remove.append(i)
            move_piece(board,king, (x,y))

        for i in range(len(king.poss_captures)):
            temp = board[king.poss_captures[i][1]][king.poss_captures[i][0]]
            move_piece(board, king, king.poss_captures[i])
            if (is_black_in_check(board) == True):
                captures_to_remove.append(i)     
            move_piece(board, king, (x, y))
            add_piece (board, temp)    
                            
    for index in reversed(moves_to_remove):
            king.poss_moves.pop(index)
    if not captures_to_remove == []:
        for index in reversed(captures_to_remove):
            king.poss_captures.pop(index)
                
                
def check_pin(board, piece):    #removes possible moves that will cause their own king to be checked. 
    x, y = piece.xpos, piece.ypos
    moves_to_remove = []
    captures_to_remove = []
    if (piece.color == 0):
        for i in range(len(piece.poss_moves)):
            move_piece(board, piece, piece.poss_moves[i])
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 1:
                        board[row][col].find_poss_moves()
                        if white_king_pos in board[row][col].poss_captures:
                            moves_to_remove.append(i)
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))

        for i in range(len(piece.poss_captures)):
            temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
            move_piece(board, piece, piece.poss_captures[i])
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 1:
                        board[row][col].find_poss_moves()
                        if white_king_pos in board[row][col].poss_captures:
                            captures_to_remove.append(i)
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))
            add_piece (board, temp)

    elif (piece.color == 1):
        for i in range(len(piece.poss_moves)):
            move_piece(board, piece, piece.poss_moves[i])
            
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 0:
                        board[row][col].find_poss_moves()
                        if black_king_pos in board[row][col].poss_captures:
                            moves_to_remove.append(i) 
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))

        for i in range(len(piece.poss_captures)):
            temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
            move_piece(board, piece, piece.poss_captures[i])
            for row in range(0, 8):
                for col in range(0, 8):
                    if board[row][col].color == 0:
                        board[row][col].find_poss_moves()
                        if black_king_pos in board[row][col].poss_captures:
                            captures_to_remove.append(i)
                        board[row][col].clear_lists()        
            move_piece(board, piece, (x, y))
            add_piece (board, temp)

    for index in reversed(moves_to_remove):
        piece.poss_moves.pop(index)
    if not captures_to_remove == []:
        for index in reversed(captures_to_remove):
            piece.poss_captures.pop(index)
        
def can_king_castle(board, color):   #appends coords if king can legally castle without being checked

    if color == 0:
        king = board[white_king_pos[1]][white_king_pos[0]]
        king.can_king_castle()
        if king.can_castle_short == True:
            move_piece(board, king, (5,7))
            if is_white_in_check(board) == False:
                move_piece(board, king, (6,7))
                if is_white_in_check(board) == False:
                    king.poss_moves.append((6,7))
            move_piece(board,king, (4,7))
        elif king.can_castle_long == True:
            move_piece(board, king, (3,7))
            if is_white_in_check(board):
                move_piece(board, king, (2,7))
                if is_white_in_check(board):
                    king.poss_moves.append((2,7))
            move_piece(board,king, (4,7))

    elif color == 1:
        king = board[black_king_pos[1]][black_king_pos[0]]
        if king.can_castle_short == True:
            move_piece(board, king, (5,0))
            if is_white_in_check(board) == False:
                move_piece(board, king, (6,0))
                if is_white_in_check(board) == False:
                    king.poss_moves.append((6,0))
            move_piece(board,king, (4,0))
        elif king.can_castle_long == True:
            move_piece(board, king, (3,0))
            if is_white_in_check(board):
                move_piece(board, king, (2,0))
                if is_white_in_check(board):
                    king.poss_moves.append((2,0))
            move_piece(board,king, (4,0))

def is_white_stalemate(board):
    flag1 = True    #no possible white movements
    flag2 = True
    king = board[white_king_pos[1]][white_king_pos[0]]

    flag1_1 = (king.poss_moves == [] and king.poss_captures == [])  #no possible king moves

    for row in range(0, 8):
        for col in range(0, 8):   
            piece = board[row][col]
            if (piece.color == 0):
                flag1 = False
            if not isinstance(piece, King):
                flag2 = False
    print (flag1,flag1_1,flag2)
    return (flag1 and flag1_1) or flag2
    
        
def is_black_stalemate(board):
    flag1 = True
    flag2 = True
    king = board[black_king_pos[1]][black_king_pos[0]]

    flag1_1 = (king.poss_moves == [] and king.poss_captures == [])

    for row in range(0, 8):
        for col in range(0, 8):   
            piece = board[row][col]
            if (piece.color == 1):
                if (piece.poss_moves != [] or piece.poss_captures != []):
                    flag1 = False
            if not isinstance(piece, King):
                flag2 = False
    print (flag1,flag1_1,flag2)
    return (flag1 and flag1_1) or flag2

def check_promotions(board, color):
    if color == 0:
        for i in range (0,8):
            if isinstance(board[0][i], Pawn):
                add_piece(board,Queen(0,i,0,board))
    elif color == 1:
        for i in range (0,8):
            if isinstance(board[7][i], Pawn):
                add_piece(board,Queen(1,i,7,board))
"""
Functions for when king is in check-state
"""    
def is_black_in_check(board):  #returns a bool, True if in check. 
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col].color == 0:
                board[row][col].find_poss_moves()
                if black_king_pos in board[row][col].poss_captures:
                    board[row][col].clear_lists()
                    return True
                board[row][col].clear_lists()
    return False

def is_white_in_check(board):  #returns a bool, True if in check. 
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col].color == 1:
                board[row][col].find_poss_moves()
                if white_king_pos in board[row][col].poss_captures:
                    board[row][col].clear_lists()
                    return True
                board[row][col].clear_lists()
    return False

def can_white_block(board): #called when white is in check. Corrects piece moves so they have to protect king
    return_val = False
    moves_to_remove = []
    captures_to_remove = []
    for row in range(0,8):
        for col in range(0,8):
            piece = board[row][col]
            if piece.color == 0 and not(isinstance(piece, King)):
                for i in range (len(piece.poss_moves)):
                    move_piece(board, piece, piece.poss_moves[i])
                    if is_white_in_check(board) == True:
                        moves_to_remove.append(i)
                    move_piece(board, piece, (col,row))
                for index in reversed(moves_to_remove):
                    piece.poss_moves.pop(index)
                moves_to_remove = []
                if piece.poss_moves != []:
                    return_val = True
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col].color == 0 and not(isinstance(board[row][col], King)):
                piece = board[row][col]
                for i in range (len(piece.poss_captures)):
                    temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
                    move_piece(board, piece, piece.poss_captures[i])
                    if is_white_in_check(board) == True:
                        captures_to_remove.append(i)
                    move_piece(board, piece, (col,row))
                    add_piece(board, temp)
                if not captures_to_remove == []:
                    for index in reversed(captures_to_remove):
                        piece.poss_captures.pop(index)
                captures_to_remove = []
                if piece.poss_captures != []:
                    return_val = True
    return return_val
                
def can_black_block(board): #called when black is in check. Corrects piece moves so they have to protect king. Returns true/false if there's a move to protect
    return_val = False
    moves_to_remove = []
    captures_to_remove = []
    for row in range(0,8):
        for col in range(0,8):
            piece = board[row][col]
            if piece.color == 1 and not(isinstance(piece, King)):
                for i in range (len(piece.poss_moves)):
                    move_piece(board, piece, piece.poss_moves[i])
                    if is_black_in_check(board) == True:
                        moves_to_remove.append(i)
                    move_piece(board, piece, (col,row))
                for index in reversed(moves_to_remove):
                    piece.poss_moves.pop(index)
                moves_to_remove = []
                if piece.poss_moves != []:
                    return_val = True
    for row in range(0,8):
        for col in range(0,8):
            if board[row][col].color == 1 and not(isinstance(board[row][col], King)):
                piece = board[row][col]
                for i in range (len(piece.poss_captures)):
                    temp = board[piece.poss_captures[i][1]][piece.poss_captures[i][0]]
                    move_piece(board, piece, piece.poss_captures[i])
                    if is_black_in_check(board) == True:
                        captures_to_remove.append(i)
                    move_piece(board, piece, (col,row))
                    add_piece(board, temp)
                if not captures_to_remove == []:
                    for index in reversed(captures_to_remove):
                        piece.poss_captures.pop(index)
                captures_to_remove = []
                if piece.poss_captures != []:
                    return_val = True
    return return_val            
    
def is_white_checkmate(board):
    if is_white_in_check(board) == True:
        king = board[white_king_pos[1]][white_king_pos[0]]
        legal_king_moves(board, king)
        if king.poss_moves == [] and king.poss_captures == [] and (not can_white_block(board)):
            return True
    return False

def is_black_checkmate(board):
    if is_black_in_check(board) == True:
        king = board[black_king_pos[1]][black_king_pos[0]]
        king.find_poss_moves()
        legal_king_moves(board, king)
        if king.poss_moves == [] and king.poss_captures == [] and not(can_black_block(board)):
            return True
    return False

def init(board):    #Corrects the king position variables.
    global white_king_pos, black_king_pos
    for row in range(0,8):
        for col in range(0,8):
            piece = board[row][col]
            if isinstance(piece, King):
                if piece.color == 0:
                    white_king_pos = (piece.xpos,piece.ypos)
                elif piece.color == 1:
                    black_king_pos = (piece.xpos,piece.ypos)
                    
"""
Stockfish initialization
"""

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


def fish_init():
    stockfish.set_depth(10)
    stockfish.update_engine_parameters({"Hash": 32, "Skill Level": 15})

def move_to_tuple(color, move):    #returns piece location, and piece move location.
    ret1 = 0
    ret2 = 0
    ret3 = 0
    ret4 = 0
    
    if isinstance(move, str) and len(move) >= 4 and 'a' <= move[0] <= 'h' and 'a' <= move[2] <= 'h' and '1' <= move[1] <= '8' and '1' <= move[3] <= '8':   
        ret1 = ord(move[0])-ord('a')
        ret3 = ord(move[2])-ord('a')
        ret2 = int(move[1])
        ret4 = int(move[3])
        piece = board[8-ret2][ret1]
        if isinstance(piece,Tile):
            return False
    else:
        return False
    return (ret1,8-ret2), (ret3,8-ret4)

def board_to_fen(board, color):
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            qrook = True
        else:
            qrook = False
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            krook = True
        else:
            krook = False
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            Qrook = True
        else:
            Qrook = False
    if (isinstance(board[0][0], Rook)):
        if board[0][0].has_moved == False:
            Krook = True
        else:
            Krook = False

    str_ret = ""
    temp = 0
    for i in range (0,8):
        for j in range (0,8):
            piece = board[i][j]
            if isinstance(piece, Tile):
                temp += 1

            if isinstance(piece, Pawn):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'p'
                elif piece.color == 0:
                    str_ret += 'P'

            elif isinstance(piece, Horse):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'n'
                elif piece.color == 0:
                    str_ret += 'N'      

            elif isinstance(piece, Bishop):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'b'
                elif piece.color == 0:
                    str_ret += 'B'

            elif isinstance(piece, Rook):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'r'
                elif piece.color == 0:
                    str_ret += 'R'      

            elif isinstance(piece, Queen):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'q'
                elif piece.color == 0:
                    str_ret += 'Q'

            elif isinstance(piece, King):
                if temp != 0:
                    str_ret += str(temp)
                    temp = 0
                if piece.color == 1:
                    str_ret += 'k'
                elif piece.color == 0:
                    str_ret += 'K'   
        if temp != 0:
            str_ret += str(temp)
            temp = 0
        str_ret += '/'
    str_ret = ''.join(str_ret[:-1])
    if color == 0:
        str_ret += " w "
    elif color == 1:
        str_ret += " b "

    str_ret += "-"
    # king = board[white_king_pos[1]][white_king_pos[0]]
    # if king.has_moved == False:
    #     if Krook == True:
    #        str_ret += 'K'
    #     if Qrook == True:
    #         str_ret += 'Q'

    # king = board[black_king_pos[1]][black_king_pos[0]]
    # if king.has_moved == False:
    #     if krook == True:
    #        str_ret += 'k'
    #     if qrook == True:
    #         str_ret += 'q'

    str_ret += " - 0 0"
    return str_ret

def fen_to_board(fen):
    global black_king_pos
    global white_king_pos
    fen = fen.split("/")
    for i,str  in enumerate (fen): 
        new_j = 0
        for j,char in enumerate(str):
            if i < 8 and new_j < 8:
                if '1' <= char <= '8':
                    val = int(char)-1  
                    for h in range(new_j,val):
                        board[i][h] = tile
                    new_j += val
                elif char == 'r':
                    if (j,i) == (0,7) or (j,i) == (0,0):
                        board[i][new_j] = Rook(1,new_j,i,board,False)
                    else:
                        board[i][new_j] = Rook(1,new_j,i,board,True)
                elif char == 'R':
                    if (j,i) == (7,7) or (j,i) == (7,0):
                        board[i][new_j] = Rook(0,new_j,i,board,False)
                    else:
                        board[i][new_j] = Rook(0,new_j,i,board,True)

                elif char == 'p':
                    board[i][new_j] = Pawn(1,new_j,i,board)
                elif char == 'P':
                    board[i][new_j] = Pawn(0,new_j,i,board)

                elif char == 'n':
                    board[i][new_j] = Horse(1,new_j,i,board)
                elif char == 'N':
                    board[i][new_j] = Horse(0,new_j,i,board)

                elif char == 'b':
                    board[i][new_j] = Bishop(1,new_j,i,board)
                elif char == 'B':
                    board[i][new_j] = Bishop(0,new_j,i,board)
            
                elif char == 'k':
                    if (j,i) != (4,0):
                        board[i][new_j] = King(1,new_j,i,board,True)
                    else:
                        board[i][new_j] = King(1,new_j,i,board,False)
                    black_king_pos = (j,i)
                elif char == 'K':
                    if (j,i) != (4,7):
                        board[i][new_j] = King(0,new_j,i,board,True)
                    else:
                        board[i][new_j] = King(0,new_j,i,board,False)
                    white_king_pos = (new_j,i)

                elif char == 'q':
                    board[i][new_j] = Queen(1,new_j,i,board)
                elif char == 'Q':
                    board[i][new_j] = Queen(0,new_j,i,board)
                new_j += 1
    fen = fen[7].split(" ")
    if fen[1] == 'w':
        return 0
    elif fen[1] == 'b':
        return 1                

def get_best_move(board, color):
    fen = board_to_fen(board, color)
    stockfish.set_fen_position(fen)
    move = stockfish.get_best_move()
    print(move)
    return move, move_to_tuple(color, move)
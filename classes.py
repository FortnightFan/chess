global board
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
global tile
        
global white_king_pos
white_king_pos = (3,7)
global black_king_pos
black_king_pos = (3,0)


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
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y += 1

            y = self.ypos
            while y >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares north
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                y -= 1

            y = self.ypos
            x = self.xpos
            while x < 8 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares east
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                    break
                x += 1

            x = self.xpos
            while x >= 0 and (self.board[y][x] == tile or self.board[y][x] == self or self.board[y][x].color == 0):  # checks all squares west
                if self.board[y][x].color == 1:
                    self.poss_captures.append((x,y))
                    break
                else:
                    self.poss_moves.append((x,y))
                x -= 1
                
        self.poss_moves = list(set(self.poss_moves))  
        self.poss_moves.remove((self.xpos,self.ypos))
            
class King(Piece):
    def __str__ (self):
        if self.color == 0:
            return (f"KW")
        elif self.color == 1:
            return (f"KB")
    
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
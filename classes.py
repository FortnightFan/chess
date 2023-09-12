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
        return (f".")

class Pawn(Piece):
    def __str__(self):  #string formatting
        return (f"P")
    
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
            elif self.ypos < 8 and self.board[y][x] == tile:
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
                
    def clear_lists(self):
        self.poss_moves = []
        self.poss_captures = []

class Rook(Piece):
    def __str__(self):  #string formatting
        return (f"R")
    
    def find_poss_moves(self):
        x, y = self.xpos, self.ypos
        while y < 8 and (self.board[y][x] == tile or self.board[y][x] == self):  # checks all squares south
            self.poss_moves.append((x, y))
            y += 1

        y = self.ypos
        while y >= 0 and (self.board[y][x] == tile or self.board[y][x] == self):  # checks all squares north
            self.poss_moves.append((x, y))
            y -= 1

        y = self.ypos
        x = self.xpos
        while x < 8 and (self.board[y][x] == tile or self.board[y][x] == self):  # checks all squares east
            self.poss_moves.append((x, y))
            x += 1

        x = self.xpos
        while x >= 0 and (self.board[y][x] == tile or self.board[y][x] == self):  # checks all squares west
            self.poss_moves.append((x, y))
            x -= 1
            
        self.poss_moves = list(set(self.poss_moves))    #removes duplicates


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
tile = Tile(2,0,0,board)
for i in range (0,8):
    for j in range (0,8):
        board[i][j] = tile

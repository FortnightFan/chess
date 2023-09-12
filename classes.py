class Pawn:
    def __init__(self, color, xpos,ypos,board):
        self.color = color  # 0 = white, 1 = black
        self.xpos = xpos    #horizontal position
        self.ypos = ypos    #vertical position
        self.board = board  #reference to game board
        self.has_moved = False  # Indicates whether the pawn has moved
        self.poss_moves = []
        
    def __str__(self):
        return (f"P")
    
    def possible_moves(self):   #returns a list of tuples that represent all possible moves.
        if self.color == 0:
            if not(self.has_moved):
                self.poss_moves.append((self.xpos,self.ypos-2))
            else:
                self.poss_moves.append((self.xpos,self.ypos-1))
        elif self.color == 1:
            if not(self.has_moved):
                self.poss_moves.append((self.xpos,self.ypos+2))
            else:
                self.poss_moves.append((self.xpos,self.ypos+1))
    def clear_possible_moves(self):
        self.poss_moves = []

class Rook:
    def __init__(self,color,xpos,ypos,board):
        self.color = color  # 0 = white, 1 = black
        self.xpos = xpos    #horizontal position
        self.ypos = ypos    #vertical position
        self.board = board  #reference to game board
        self.poss_moves = []

    def __str__(self):
        return (f"R")
    
    def possible_moves(self):   #returns a list of tuples that represent all possible moves.
        x,y=(self.xpos,self.ypos+1)     #declares temporary x,y variables. ypos+1 is so it does not look at its own square
        while (self.board[y][x] == 0 and y < 8):
            self.poss_moves.append((self.xpos,y))
            y += 1
            
            
    def clear_possible_moves(self):
        self.poss_moves = []
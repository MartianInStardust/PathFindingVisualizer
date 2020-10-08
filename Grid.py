import pygame as pg
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
pathC =  (255,255,0)
cl = (0,0,255)
op = (3,144,255)
red = (255,0,0)
W_WIDTH, W_HEIGHT = 800,600


class Grid:

    def __init__(self,length, W_WIDTH, W_HEIGHT):
        self.length = length
        self.board = [ [ 0 for _ in range(W_WIDTH//length) ] for _ in range(W_HEIGHT//length) ]
        self.board[0][0] = 1
        self.board[-1][-1] = 2
        self.startNode = self.get_node(1)
        self.targetNode = self.get_node(2)
    
    def get_node(self,node):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == node:
                    return (i,j)
        return None
    
    def display(self,win):
        win.fill(white)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                
                color = None
                if self.board[i][j] == 1:
                    color = green
                elif self.board[i][j] == 2:
                    color = red
                elif self.board[i][j] == 3:
                    color = pathC
                elif self.board[i][j] == -1:
                    color = black
                elif self.board[i][j] == 4:
                    color = op
                elif self.board[i][j] == 5:
                    color = cl
                if color:
                    pg.draw.rect(win,color,(self.length*j,self.length*i,self.length,self.length))
                
        # draw horizontal and vertiacal black lines          
        for m in range(len(self.board)):
            pg.draw.line(win,black,(0,self.length*m),(W_WIDTH,self.length*m))
        for n in range(len(self.board[0])):
            pg.draw.line(win,black,(self.length*(n),0),(self.length*(n),W_HEIGHT))
            if n == len(self.board[m]) - 1:
                pg.draw.line(win,black,(self.length*(n+1),0),(self.length*(n+1),W_HEIGHT))
        txt = ("Press space to run","c to clear","mouse click to draw")
        for i in range(3):
            txtTemp = txt[i]

            
            font = pg.font.Font('freesansbold.ttf', 20) 

            text = font.render(txtTemp, True, black, white) 

            textRect = text.get_rect()  
            textRect.center = (900, 20+30*i) 
            win.blit(text, textRect) 

    

    
    def set(self,nBoard):
        self.board = nBoard
    
    def clicked(self,x,y):
        result = (y//self.length,x//self.length)
        if  0 <= result[0] < len(self.board) and 0 <= result[1] < len(self.board[0]):
            return result
        return None
    
    def clear(self,walls=True):
        nums = [-1,3,4,5] if walls else [3,4,5]
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] in nums:
                    self.board[i][j] = 0
    
    def move_node(self,node,toPos):
        if 0 <= toPos[0] < len(self.board) and 0 <= toPos[1] < len(self.board[0]):
            if self.board[toPos[0]][toPos[1]] not in (1,2):
                y,x = self.get_node(node)
                self.board[y][x] = 0
                self.board[toPos[0]][toPos[1]] = node
                self.startNode = self.get_node(1)
                self.targetNode = self.get_node(2)
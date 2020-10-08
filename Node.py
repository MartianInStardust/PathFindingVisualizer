
class Node:
    
    def __init__(self,pos=None,parentNode=None,startPos=None,targetPos=None):
        
        if startPos != None and targetPos != None:
            self.pos = startPos
            self.targetNode = targetPos
            self.g_cost = 0
            self.h_cost = 0
            self.cost = 0
        elif pos != None and parentNode != None:
            self.parent = parentNode
            self.targetNode = parentNode.targetNode
            self.pos = pos
            self.g_cost = parentNode.g_cost + self.distance(self.parent.pos)
            # print(parentNode.g_cost, self.distance(self.parent.pos))
            self.h_cost = self.get_h_val()
            self.cost = self.g_cost+self.h_cost

    def get_h_val(self):
        a = abs(self.pos[0] - self.targetNode[0])
        b = abs(self.pos[1] - self.targetNode[1])
        return a+b
        # dis = ((self.pos[0] - self.targetNode[0])**2+(self.pos[1] - self.targetNode[1])**2)**0.5

        # return dis

    def distance(self,fromPos):
        dis = ((self.pos[0]-fromPos[0])**2+(self.pos[1]-fromPos[1])**2)**0.5
        
        return dis

    def getNeighbors(self,board):
        n = (0,1,2,3,4,5)
        y,x = self.pos
        down = False
        up = False
        left_up = False
        left_down = False
        right_up = False
        right_down = False
        h_len = len(board[0]) # x, pos[1] #
        v_len = len(board) # y, pos[0] #
        neighbors = []
        if y < v_len-1:
            y1 = y+1
            x1 = x
            down = True
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                left_down = True
                right_down = True
                
        if y > 0:
            y1 = y-1
            x1 = x
            up = True
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                left_up = True
                right_up = True

        if x < h_len-1:
            y1 = y
            x1 = x+1
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                right_up = True
                right_down = True

            if right_up and up:
                y1 = y-1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
                    
            if right_down and down:
                y1 = y+1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
        if x > 0:
            y1 = y
            x1 = x-1
            if board[y1][x1] in n:
                neighbors.append(Node(pos=(y1,x1),parentNode=self))
                left_up = True
                left_down = True
                
            if left_up and up:
                y1 = y-1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
            if left_down and down:
                y1 = y+1
                if board[y1][x1] in n:
                    neighbors.append(Node(pos=(y1,x1),parentNode=self))
        return neighbors
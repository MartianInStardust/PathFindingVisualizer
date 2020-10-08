from Node import Node 
class NodeList:
    def __init__(self):
        self.items = []
    
    def contains(self,obj):
        if len(self.items) > 0 :
            for i,node in enumerate(self.items):
                if obj.pos == node.pos:
                    return i
        return -1
    
    def getMin(self):
        if len(self.items) > 0:
            curr = 0
            for i in range(len(self.items)):
                node = self.items[i]
                if node.cost < self.items[curr].cost:
                    curr = i
            return curr
        return -1
    
    def _print(self):
        for node in self.items:
            print(node.pos,end=",")
        print()
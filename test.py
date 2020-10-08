import pygame as pg
from pygame.locals import *
import time
from Node import Node
from Grid import Grid
from NodeList import NodeList

def solve(grid,showSteps=True):
    paused = False
    operations = 0
    av = (0,3,4,5)
    clock = pg.time.Clock()
    openList = NodeList()
    closedList = NodeList()
    board = grid.board
    startNode = Node(startPos=grid.startNode,targetPos=grid.targetNode)
    openList.items.append(startNode)
    abreak = False
    start = grid.startNode
    end = grid.targetNode

    noCount = 0.
    s = time.time()
    # this is the start of path finding and displaying steps process---------------------------------#
    while True:

        # Path searching algorithm starts here 
        if not openList.items:
            print("NoPathException")
            return board

        neighbors = NodeList()
        n = openList.getMin()

        curr = openList.items[n]
        openList.items.pop(n)
        closedList.items.append(curr)
        neighbors = curr.getNeighbors(board)
        # not neccesary condition since if the end node could be found it will always be in the neighbors
        # if curr.pos == end:
        #     break
        for neighbor in neighbors:
            if neighbor.pos == end:
                # setting end reached flag here
                abreak = True
                break
            index1 = openList.contains(neighbor)
            index2 = closedList.contains(neighbor)
            if index1 >= 0 and openList.items[index1].cost > neighbor.cost:
                openList.items.pop(index1)
                openList.items.append(neighbor)
            if index2 >= 0 and closedList.items[index2].cost > neighbor.cost:
                closedList.items.pop(index2)
                # adding this neighbor to openlist isnt necessary, but it might turn out to be shortest path #
                openList.items.append(neighbor)
            if index1 == -1 and index2 == -1:
                openList.items.append(neighbor)
        # one recursion of the path searching ends here

        # begiining the visualiztion step for each recursion so we can visualize this process
        if showSteps:

            startNoCount = time.time()

            for node in closedList.items:
                y,x = node.pos
                if (y,x) != start:
                    grid.board[y][x] = 4
                    
            for node in openList.items:
                y,x = node.pos
                if (y,x) != start:
                    grid.board[y][x] = 5

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return board
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return board
                    if event.key == pg.K_SPACE:
                        paused = True
                        pg.event.clear()
                        break

            while paused:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return board
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            paused = False
                            break
                        elif event.key == pg.K_ESCAPE:
                            return board

            grid.display(win)
            pg.display.flip()
            pg.time.delay(FRAME_RATE)

            noCount += time.time() - startNoCount

        if abreak:
            break

    actualTime = time.time() - s - noCount
    # this is the end of path searching and displaying steps process----------------------------#

    
    # Extracting found path starts here ------------------------------------------------------------------------- #    
    path = NodeList()
    length = 0
    #reverser the path to start it from start node
    curr = closedList.items[-1]

    while curr.pos != start:
        y,x = curr.pos
        if board[y][x] in av and (y,x) != start:
            path.items.append(curr)
            length += curr.g_cost
        curr = curr.parent
    
    length = round(length,3)

    elapsedTime = time.time()-s


    if showSteps:
        print("found path of length",length,"time: ",actualTime,"s")
        
    path.items = reversed(path.items)

    for elem in path.items:
        
        y, x = elem.pos
        board[y][x] = 3
        grid.display(win)
        pg.display.flip()
        pg.time.delay(FRAME_RATE)

    return board

def main(win):
    global startNode, targetNode
    solving = True
    editing = False
    moving = False
    while solving:

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos1 = pg.mouse.get_pos()
                    # send pos1 tuple to clicked function
                    pos1 = grid.clicked(*pos1)
                    if pos1:
                        # pos x y order is different than the board x y which is row and col
                        y,x = pos1
                        k = grid.board[y][x]
                        if k == 0 or k == -1 or k == 3 or k == 4 or k ==5:
                            editing = True
                            if k == -1:
                                grid.board[y][x] = 0
                            else:
                                grid.board[y][x] = -1
                        elif k == 1 or k == 2:
                            moving = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    editing = False
                    moving = False
            if moving or editing:
                pos = pg.mouse.get_pos()
                pos = grid.clicked(*pos)
                if pos:
                    if moving:
                            grid.move_node(k,pos)
                            startNode = grid.get_node(1)
                            targetNode = grid.get_node(2)

                    if pos != pos1:
                        y,x = pos
                        k = grid.board[y][x]
                        if editing:
                            if k == 0 or k == -1 or k == 3 or k == 4 or k ==5:
                                if k == -1:
                                    grid.board[y][x] = 0
                                else:
                                    grid.board[y][x] = -1
                    pos1 = pg.mouse.get_pos()
                    pos1 = grid.clicked(*pos1)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    grid.clear(walls=False)
                elif event.key == pg.K_c:
                    grid.clear()
                elif event.key == pg.K_SPACE:
                    grid.clear(walls=False)
                    grid.set(solve(grid))
                    grid.display(win)
                    pg.event.clear()

                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    return

            elif event.type == pg.QUIT:
                pg.quit()
                return
        
        grid.display(win)
        pg.display.flip()        

if __name__ == "__main__":

    W_WIDTH, W_HEIGHT = 800,600
    win = pg.display.set_mode((W_WIDTH+200,W_HEIGHT))
    FRAME_RATE = 50
    pg.init()
    pg.display.set_caption("Path finding algorithm visualization")
    size = 20
    count = 0
    grid = Grid(size, W_WIDTH, W_HEIGHT)
    startNode = grid.get_node(1)
    targetNode = grid.get_node(2)
    main(win)
    
   
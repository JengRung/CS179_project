import numpy as np
import heapq
import tkinter
from numba import jit, cuda

testGrid= np.asarray([
    [58, 48 , 0,  0,  0,  0 , 0,  0],
    [47 , 0,  0,  0,  0,  0,  0,  0],
    [46 ,58, 13, 42 ,87, 79 , 0 , 0],
    [31 ,98 , 0,  0,  0,  0 , 0 , 0],
    [30 , 0 , 0 , 0 , 0 , 0 , 0,  0],
    [40 ,68, 61, 82 ,13, 12, 51, 74],
    [ 0,  0,  0,  0 , 0,  0,  0 , 0],
    [26 ,11, 48 ,66, 52, 41, 43, 74],
    [32,  0,  0,  0 , 0,  0 , 0 , 0],
    [56 ,47 ,13 ,48 ,74 ,57 ,64 ,42],
    [79, 60 ,65 ,46 , 0 , 0 , 0 , 0],
    [ 1, 67, 111 ,56 , 0 , 0 , 0 , 0]])



leftSum= np.sum(testGrid[0:6])
rightSum= np.sum(testGrid[6:12])
diff= np.abs(leftSum-rightSum)

def display(grid):
    print(grid)
    print("\n  "+ str(leftSum))
    print("- " + str(rightSum))
    print("________________")
    print("= " + str(diff))
    print(grid.shape)


def generate_moves(grid):
    rows= grid.shape[0]
    cols= grid.shape[1]
    topBox = np.empty((0,))
    topSpace = np.empty((0,))
    for y in range(rows):
        for x in range(cols-1):
            if grid[y][x] != 0:
                if grid[y][x+1] == 0:
                    topBox= np.append(topBox, np.array((y,x)), axis= 0)
                    topSpace= np.append(topSpace, np.array((y,x+1)), axis= 0)
                elif x== (cols-1-1):
                    topBox= np.append(topBox, np.array((y,x+1)), axis= 0)
            elif x==0:
                topSpace= np.append(topSpace, np.array((y,x)), axis= 0)
    topBox= topBox.reshape(-1, 2)
    topSpace= topSpace.reshape(-1, 2)
    return topBox, topSpace


def expandNodes(grid, moves, debug=False):
    node = np.copy(grid)
    heuristics= np.empty(0)
    newNodes= np.empty(0)
    heuristics= np.empty(0)
    length= node.shape[0]
    for box in moves[0]:
        boxY= int(box[0])
        boxX= int(box[1])
        for space in moves[1]:
            spaceY= int(space[0])
            spaceX= int(space[1])

            if boxY!= spaceY:
                dist= np.abs(boxX-spaceX) + np.abs(boxY-spaceY)
                leftSum= np.sum(node[0:(length//2)])
                rightSum= np.sum(node[(length//2):length])
                diff= np.abs(leftSum-rightSum)
                heuristics= np.append(heuristics, np.abs(dist+diff))
                if debug: print( str(box)+"-->"+ str(spaceY)+","+ str(spaceX)+" | "+str(np.abs(dist+diff))+"\n")
                
                node[spaceY][spaceX]= node[boxY][boxX]
                node[boxY][boxX]= 0

                dist= np.abs(boxX-spaceX) + np.abs(boxY-spaceY)
                leftSum= np.sum(node[0:(length//2)])
                rightSum= np.sum(node[(length//2):length])
                diff= np.abs(leftSum-rightSum)
                heuristics= np.append(heuristics, np.abs(dist+diff))
                if debug: print( str(box)+"-->"+ str(spaceY)+","+ str(spaceX)+" | "+str(np.abs(dist+diff))+"\n")
                print("-------------------")
    return newNodes, heuristics


display(testGrid)
moves= generate_moves(testGrid)
newNode= expandNodes(testGrid, moves, debug=True)
print("-------")
print(str(moves[0].shape)+"x"+str(moves[1].shape))
print(newNode[1].shape)
print(newNode[1])
print(min(newNode[1]))

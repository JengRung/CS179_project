import queue
import copy
import time
import matplotlib.pyplot as plt
import numpy as np
import container

"""
Classes:
    Node - Class to keep the state of a node in the search que, can be compared to each other by distance
"""
class node:
    #Class to keep the state of a node in the search queue

    def __init__(self, state, depth: int, distance: int) -> None:
        self.state = copy.deepcopy(state)
        self.depth = depth
        self.distance = distance

    def __lt__(self, other):
        if (self.distance + self.depth == other.distance + other.depth):
            return self.depth < other.depth
        else:
            return (self.distance + self.depth) < (other.distance + other.depth)

    def __gt__(self,other):
        return (self.distance + self.depth) > (other.distance + other.depth)


"""
Driver Functions:

make_que() - Function that initializes a priority que given a node

make_node() - Function that creates a node given a state (in our case, a 2d array)

heuristic() - Heuristic function, receives state and a boolean which determines if we will use manhattan distance or simply missing square
    input: state, h_n
    output: heuristic evaluation of state

expand() - Function which expands the children of a given state. The function checks if any of the 4 squares surrounding the 0 tile
can be swapped with the 0 tile, and if its legal it preforms the move in a new state
    input: node
    output: list of child states

For the queing functions, I use a priority que and compare g(n) + h(n) when adding a new node to the queue
queing_function_uniform() - Adds children from expand() into the priority que with the nodes distance using uniform distance
queing_function_missing() - Ques using missing square distance
queing_function_manhattan() - Ques using manhattan distance
    input: node priority que, children from expand(), depth of nodes to que, set of visited nodes
    output: node priority que with children qued

search() - Generic searching function, terminates when goal is found or throws exception if the search fails. 
    input: problem, queing function
    output: the solution node, search statistics
"""
#Initializes a que with a single node
def make_que(node: node) -> queue.Queue:
    Que = queue.PriorityQueue()
    Que.put(node)
    return Que

#Creates a que node for the given state
def make_node(state, depth: int, distance: int) -> node:
    return node(state,depth,distance)

def heuristic(state, use_missing: bool, use_manhattan: bool) -> int:
    #If h_n = False we are using missing tiles
    dist = 0
    dimension = len(state)
    for i in range(dimension):
        for j in range(dimension):
            # f(x,y) = dim * y + x, in the given example dimension = 3
            if (state[i][j] != dimension*i + j + 1):
                if (state[i][j] != pow(dimension,2) and use_missing):
                    dist = dist + 1

                # we don't care about the distance of the empty tile so we exclude it
                if (state[i][j] != pow(dimension,2) and use_manhattan): 
                    goal_j = (state[i][j] - 1) % dimension # f(x,y) % dim = x 
                    goal_i = (state[i][j] - 1) // dimension # floor[f(x,y) / dim] = y

                    # Adding h(n) and not counting blank square, which im leaving as 9 for simplicity
                    dist = dist + abs(i - goal_i) + abs(j - goal_j)
    return dist

#I wasn't sure how to take an operator as an argument so I just made expand fit the square problem
def expand(node: node):
    state = copy.deepcopy(node.state)
    dim = len(state)
    children = []
    for i in range(dim):
        for j in range(dim):
            #Empty square is dim^2
            if state[i][j] == pow(dim,2):
                #We can move the top square down, swap 9 and i,j
                if i > 0:
                    state1 = copy.deepcopy(state)
                    state1[i][j],state1[i-1][j] = state1[i-1][j],state1[i][j]
                    children.append(state1)
                
                #We can move the bottom square up, swap 9 and i,j
                if i < dim - 1:
                    state2 = copy.deepcopy(state)
                    state2[i][j],state2[i+1][j] = state2[i+1][j],state2[i][j]
                    children.append(state2)

                #We can move the left square to the right, swap 9 and i,j
                if j > 0:
                    state3 = copy.deepcopy(state)
                    state3[i][j],state3[i][j-1] = state3[i][j-1],state3[i][j]
                    children.append(state3)

                #We can move the right square to the left, swap 9 and i,j
                if j < dim - 1:
                    state4 = copy.deepcopy(state)
                    state4[i][j],state4[i][j+1] = state4[i][j+1],state4[i][j]
                    children.append(state4)
                return children

#Que's the children passed in to the que
def queing_function_uniform(nodes: queue.PriorityQueue,children,depth: int,visited_nodes: set, trace) -> queue.PriorityQueue:
    for child in children:
        tuple_state = tuple(map(tuple,child))
        if not visited_nodes.__contains__(tuple_state):
            new_node = node(child,depth+1,0)
            nodes.put(new_node)
            visited_nodes.add(tuple_state)
    if trace:
        print(f"The best state to expand with g(n) = {nodes.queue[0].depth} and h(n) = {nodes.queue[0].distance} is \n {np.matrix(nodes.queue[0].state)}\n")
    return nodes

def queing_function_manhattan(nodes: queue.PriorityQueue,children,depth: int, visited_nodes: set, trace) -> queue.PriorityQueue:
    for child in children:
        tuple_state = tuple(map(tuple,child))
        if not visited_nodes.__contains__(tuple_state):
            new_node = node(child,depth+1,heuristic(child,False,True))
            nodes.put(new_node)
            visited_nodes.add(tuple_state)
    if trace:
        print(f"The best state to expand with g(n) = {nodes.queue[0].depth} and h(n) = {nodes.queue[0].distance} is \n {np.matrix(nodes.queue[0].state)}\n")
    return nodes

def queing_function_missing_squares(nodes: queue.PriorityQueue,children,depth: int, visited_nodes: set, trace) -> queue.PriorityQueue:
    for child in children:
        tuple_state = tuple(map(tuple,child))
        if not visited_nodes.__contains__(tuple_state):
            new_node = node(child,depth+1,heuristic(child,True,False))
            nodes.put(new_node)
            visited_nodes.add(tuple_state)
    if trace:
        print(f"The best state to expand with g(n) = {nodes.queue[0].depth} and h(n) = {nodes.queue[0].distance} is \n {np.matrix(nodes.queue[0].state)}\n")
    return nodes

#Our main search; que's based on the passed in queing function
def search(problem,queing_function,trace):
    nodes = make_que(make_node(problem.init_state,0,0))
    i = 0
    max_que = 0
    visited_nodes = {tuple(map(tuple,problem.init_state))}
    while not nodes.empty():
        i = i + 1
        max_que = max(max_que,nodes.qsize())
        node = nodes.get()
        if problem.goal_test(node.state):
            return (node,node.depth,max_que,i)
        nodes = queing_function(nodes,expand(node),node.depth,visited_nodes,trace)
    raise Exception("Search terminated in failure")


def get_array(dimension):
    #Gets a test from the user

    testn = []
    for i in range(int(dimension)):
        temp = [int(i) for i in input(f"Please enter {dimension} values for row {i+1} seperated by spaces: ").split()]
        testn.append(temp)
    for i in range(len(testn)):
        for j in range(len(testn)):
            if testn[i][j] == 0:
                testn[i][j] = pow(int(dimension),2)
    return testn

def generate_goal(dim):
    goal = []
    for i in range(dim):
        temp = []
        for j in range(dim):
            temp.append(dim*i+j+1)
        goal.append(temp)
    return goal
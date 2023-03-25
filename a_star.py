import queue
import copy
import numpy as np
import container as cont

class balance():
    def __init__(self, init_state: cont.ship) -> None:
        self.init_state = copy.deepcopy(init_state)
        self.end_state = None

    def set_end_state(self,end_state: cont.ship) -> None:
        self.end_state = copy.deepcopy(end_state)
    
    def goal_test(self,state: cont.ship) -> bool:
        return state.is_balanced()

class node:
    def __init__(self, state: cont.ship, depth, distance) -> None:
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

#Initializes a que with a single node
def make_que(node: node) -> queue.Queue:
    Que = queue.PriorityQueue()
    Que.put(node)
    return Que

#Creates a que node for the given state
def make_node(state, depth: int, distance: int) -> node:
    return node(state,depth,distance)

def expand(node: node):
    ship = copy.deepcopy(node.state)
    containers = ship.containers
    dim2 = len(containers[0])
    children = []
    for column in range(dim2):
        top_index = ship.get_top_container(column)
        if (top_index != -1):
            for column2 in range(dim2):
                top_new = ship.get_top_free_space(column2)
                if (column2 != column and top_new != -1):
                    ship_temp = copy.deepcopy(ship)
                    ship_temp.set_cost((abs(column-column2)+abs(top_index-top_new)))
                    ship_temp.put_top(column2,top_index,column)
                    ship_temp.append_moves(top_index,column,top_new,column2)
                    children.append(ship_temp)
    return children

#Que's the children passed in to the que
def queing_function(nodes: queue.PriorityQueue, children: list[cont.ship], depth: int, visited_nodes: set, trace) -> queue.PriorityQueue:
    for child in children:
        tuple_state = str(child.containers)
        if not visited_nodes.__contains__(tuple_state):
            new_node = node(child,depth+1,child.heuristic() + child.last_cost)
            nodes.put(new_node)
            visited_nodes.add(tuple_state)
    if trace:
        if not nodes.qsize() == 0:
            print(f"The best state to expand with g(n) = {nodes.queue[0].depth} and h(n) = {nodes.queue[0].distance} is \n {np.matrix(nodes.queue[0].state)}\n")
    return nodes

#Our main search; que's based on the passed in queing function
def search(problem: balance,queing_function = queing_function,trace = False):
    nodes = make_que(make_node(problem.init_state,0,problem.init_state.heuristic()))
    i = 0
    visited_nodes = {str(problem.init_state.containers)}
    while not nodes.empty():
        i = i + 1
        node = nodes.get()
        if problem.goal_test(node.state):
            return (node,node.depth,i)
        nodes = queing_function(nodes,expand(node),node.depth,visited_nodes,trace)
    raise Exception("Search terminated in failure")
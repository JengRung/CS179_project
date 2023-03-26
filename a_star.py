import queue
import copy
import numpy as np
import container as cont

class balance():
    def __init__(self, init_state: cont.ship) -> None:
        self.init_state = copy.deepcopy(init_state)
        self.end_state = None

    def goal_test(self,state: cont.ship) -> bool:
        return state.is_balanced()
    
class sift_problem():
    def __init__(self, init_state: cont.ship) -> None:
        self.init_state = copy.deepcopy(init_state)
        self.end_state = self.get_sift_goal()

    def goal_test(self,state: cont.ship) -> bool:
        return str(state.containers) == str(self.end_state.containers)

    def get_sift_goal(self):
        ship = self.init_state
        goal_ship = copy.deepcopy(ship)
        for i in range(len(goal_ship.containers)):
            for j in range(len(goal_ship.containers[0])):
                if goal_ship.is_container(goal_ship.containers[i][j]):
                    goal_ship.containers[i][j] = 0
        containers = reversed(sorted(list(ship.get_full_set())))
        l = goal_ship.get_top_free_space(5)
        r = goal_ship.get_top_free_space(6)
        l_cord = [l,5]
        r_cord = [r,6]
        parity = 0
        for i in containers:
            if (parity % 2 == 0):
                goal_ship.containers[l_cord[0]][l_cord[1]] = i
                l_cord[1] -= 1
                if (l_cord[1] < 0 or goal_ship.containers[l_cord[0]][l_cord[1]] == -1):
                    l_cord[1] = 5
                    l_cord[0] = goal_ship.get_top_free_space(5)
            else:
                goal_ship.containers[r_cord[0]][r_cord[1]] = i
                r_cord[1] += 1
                if (r_cord[1] > 11 or goal_ship.containers[r_cord[0]][r_cord[1]] == -1):
                    r_cord[1] = 6
                    r_cord[0] = goal_ship.get_top_free_space(6)
            parity += 1
        return goal_ship

class node:
    def __init__(self, state: cont.ship, depth, distance, goal_state = None) -> None:
        self.state = copy.deepcopy(state)
        self.depth = depth
        self.distance = distance
        self.end_state = goal_state

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
def make_node(state, depth: int, distance: int, goal_state = None) -> node:
    return node(state,depth,distance,goal_state)

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
def queing_function(nodes: queue.PriorityQueue, children: list[cont.ship], depth: int, visited_nodes: set, trace, end_state = None) -> queue.PriorityQueue:
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

def queing_function_sift(nodes: queue.PriorityQueue, children: list[cont.ship], depth: int, visited_nodes: set, trace, end_state) -> queue.PriorityQueue:
    for child in children:
        tuple_state = str(child.containers)
        if not visited_nodes.__contains__(tuple_state):
            new_node = node(child,depth+1,child.heuristic_sift(end_state) + child.last_cost)
            nodes.put(new_node)
            visited_nodes.add(tuple_state)
    if trace:
        if not nodes.qsize() == 0:
            print(f"The best state to expand with g(n) = {nodes.queue[0].depth} and h(n) = {nodes.queue[0].distance} is \n {np.matrix(nodes.queue[0].state)}\n")
    return nodes

#Our main search; que's based on the passed in queing function
def search_(problem,queing_function = queing_function,trace = False):
    if type(problem) == sift_problem:
        nodes = make_que(make_node(problem.init_state,0,problem.init_state.heuristic_sift(problem.end_state),problem.end_state))
        print("ok")
    else:
        nodes = make_que(make_node(problem.init_state,0,problem.init_state.heuristic()))
    i = 0
    visited_nodes = {str(problem.init_state.containers)}
    while not nodes.empty():
        i = i + 1
        node = nodes.get()
        if problem.goal_test(node.state):
            print("A* finished successfully")
            return (node,node.depth,i)
        nodes = queing_function(nodes,expand(node),node.depth,visited_nodes,trace,problem.end_state)
    raise Exception("Search terminated in failure")

def search(ship, sift = False, queing_function = queing_function,trace = False):
    if(sift):
        return (search_(sift_problem(ship),queing_function_sift,trace=True))
    else:
        return (search_(balance(ship),trace=True))
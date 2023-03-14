from a_star import all
import copy
import container

class problem:
    #Abstract class

    def __init__(self, init_state, goal_state) -> None:
        self.init_state = copy.deepcopy(init_state)
        self.goal_state = copy.deepcopy(goal_state)
 

class ship(problem):
    # A class for the containers were moving
    def __init__(self, init_state, goal_state, containers) -> None:
        super().__init__(init_state, goal_state)
        self.containers = containers
        #Make containers a np array


    def a_star(self):
        #calls A* search to find optimal path to balance
        pass
    
    def balance(self):
        #balances ship as moves are given
        pass

    def transfer(self):
        #gives sequence of moves for optimal transfer, receives an array of transfers to make
        pass

    def is_balanced(self) -> bool:
        #returns the state of the container, if its balanced or not
        pass
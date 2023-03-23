class container:
    def __init__(self, name: str, mass: int) -> None:
        self.name = name
        self.mass = mass

    def __repr__(self):
        #return "({label} {mass})".format(label = self.name,mass = self.mass)
        return "{m}".format(m = self.mass)

    def __str__(self):
        return "({label} {mass})".format(label = self.name,mass = self.mass)

class move:
    def __init__(self,x1:int,y1:int,x2:int,y2:int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def evaluate():
        #return the manhattan distance of a move
        return 0


class ship():
    def __init__(self,containers: list):
        self.containers = containers

    def balance():
        #Return shortest path to the balanced state
        #[move1,move2,move3,...]
        pass
        #returns shortest path to transfer the given list off the ship.
        #[move1,move2,...]
        #move1.x1 = -1
        #move1.y1 = -1
        pass

    def transfer_list_off(list):
        # expecting an array like this: [ [1,2], [6,9] , ... ]
        #returns shortest path to transfer the given list off the ship.
        pass

    def transfer_list_on(num: int):
        #while (num--): get next container to put on
        #returns shortest path to transfer the given list off the ship.
        pass

    def get_container(cords):
        #return container at those cords
        #for container container.get_weight(), container.get_name()
        pass

    def move(self,move: move):
        self.containers[move.x1][move.y1] , self.containers[move.x2][move.y2] = self.containers[move.x2][move.y2] , self.containers[move.x1][move.y1]

    def swap(self,x1,y1,x2,y2):
        self.containers[x1][y1] , self.containers[x2][y2] = self.containers[x2][y2] , self.containers[x1][y1]

    def get_top(self,x):
        for i in range(len(self.containers)):
            if (self.containers[i][x] != -1):
                return (self.containers[i][x],i)
        return (-1,-1)
            
    def put_top(self,column,x1,y1):
        for i in range(len(self.containers)):
            if (self.containers[i][column] != -1):
                if (i == 0):
                    return False
                else:
                    self.swap(i-1,column,x1,y1)
                    return True
            elif (i == len(self.containers)-1):
                self.swap(i,column,x1,y1)
                return True

    def get_sums(self):
        dim = len(self.containers)
        dim2 = int(len(self.containers[0])/2)
        sum_l = 0
        sum_r = 0
        for i in range(dim):
            for j in range(dim2):
                sum_l += self.containers[i][j].mass
        for i in range(dim):
            for j in range(dim2,len(self.containers[0])):
                sum_r += self.containers[i][j].mass
        return (sum_l,sum_r)
    
    def is_balanced(self) -> bool:
        sum_l,sum_r = self.get_sums(self.containers)
        return (float(max(sum_l,sum_r)/min(sum_l,sum_r))<=1.1)
    
    def heuristic(self):
        return 1

    def __repr__(self):
        return ",\n".join(map(str, self.containers))

    def __str__(self):
        return ",\n".join(map(str, self.containers))

  



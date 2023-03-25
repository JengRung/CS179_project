import multiprocessing
import time

class container:
    def __init__(self, name: str, mass: int, row : int = -1, col : int = -1) -> None:
        self.name = name
        self.mass = mass
        self.row = row
        self.col = col

    def get_cords(self):
        return ((self.row,self.col))
    
    def set_cords(self,x,y):
        self.row = x
        self.col = y

    def __repr__(self):
        return "({label} {mass})".format(label = self.name,mass = self.mass)

    def __str__(self):
        return "({label} {mass})".format(label = self.name,mass = self.mass)
    
    def __lt__(self, other):
        return self.mass < other.mass

    def __gt__(self,other):
        return self.mass > other.mass
    
    def __eq__(self, __o: object) -> bool:
        if (type(__o) == container):
            return self.mass == __o.mass and self.name == __o.name
        else:
            return False
    
    def __hash__(self):
        return hash(str(self))


class Move:
    def __init__(self,x1:int,y1:int,x2:int,y2:int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return "({x1},{y1}) -> ({x2},{y2})".format(x1 = self.x1, y1 = self.y1, x2 = self.x2, y2 = self.y2)

    def __str__(self):
        return "({x1},{y1}) -> ({x2},{y2})".format(x1 = self.x1, y1 = self.y1, x2 = self.x2, y2 = self.y2)


class ship():
    def __init__(self,containers: list[container],last_cost = 0, moves = []):
        self.containers = containers
        self.last_cost = last_cost
        self.left_set = self.get_left_set()
        self.right_set = self.get_right_set()
        self.moves = moves

    def get_worst_case_balance(self):
        sum = 0
        dim = len(self.containers)
        dim2 = len(self.containers[0])
        for i in range(dim):
            for j in range(dim2):
                if (self.is_container(self.containers[i][j])):
                    if (j < dim2/2):
                        sum += abs(j - (dim2/2+1))
                    else:
                        sum += abs(j - dim2/2)
        return sum
    
    def get_closest_spot(self):
        #returns x,y of closest open spot using manhattan distance
        x = 0
        y = 0
        min = len(self.containers) + len(self.containers[0])
        for i in range(len(self.containers[0])):
            dist = self.get_top_free_space(i)
            if dist + i < min:
                x = dist
                y = i
                min = dist+i
        return(x,y)

    def append_moves(self,x1,y1,x2,y2):
        self.moves.append(Move(x1,y1,x2,y2))

    def set_cost(self,cost):
        self.last_cost += cost

    def is_container(self,cont: container) -> bool:
        return (type(cont) == container)

    def get_left_set(self):
        left = set()
        dim = len(self.containers)
        dim2 = int(len(self.containers[0])/2)
        for i in range(dim):
            for j in range(dim2):
                if self.is_container(self.containers[i][j]):
                    self.containers[i][j].set_cords(i,j)
                    left.add(self.containers[i][j])
        return left
    
    def get_right_set(self):
        right = set()
        dim = len(self.containers)
        dim2 = int(len(self.containers[0])/2)
        for i in range(dim):
            for j in range(dim2,len(self.containers[0])):
                if self.is_container(self.containers[i][j]):
                    self.containers[i][j].set_cords(i,j)
                    right.add(self.containers[i][j])
        return right
    
    def can_be_balanced(self) -> bool:
        set_both = self.get_left_set()
        set_both.union(self.get_right_set())
        containers = list(set_both)
        return self._can(containers,0,0,0)
        
    def _can(self,containers,lsum,rsum,i) -> bool:
        if (i == len(containers)-1):
            return (max(lsum,rsum) <= 1.1*min(lsum,rsum))
        for j in range(i,len(containers)):
            return self._can(containers,lsum+containers[j].mass,rsum,i+1) or self._can(containers,lsum,rsum+containers[j].mass,i+1)


    def balance(self,search,problem):
        try:
            node,i,j = search(problem,trace = True)
        except:
            return None
        return node.state

    def transfer_list_off(self,list):
        moves = []
        j = 0
        while(len(list) != 0):
            temp = list[-1]
            for i in list:
                if (not self.is_container(self.containers[i[0]][i[1]])):
                    print("Error: Trying to transfer a container that doesn't exist")
                    return []
                if i[0] == self.get_top_container(i[1]) + j:
                    self.move_off(i[0],i[1],moves)
                    list.remove(i)
                    break
                if (i == temp):
                    j = j + 1
        return moves

    def move_off(self,x,y,moves):
        while self.get_top_container(y) != x:
            self.move_nearest(self.get_top_container(y),y,moves)
        moves.append(Move(x,y,-2,-2))
        self.containers[x][y] = 0

    def move_nearest(self,x,y,moves):
        for i in range(len(self.containers[0])):
            if y-i >= 0 and self.get_top_container(y-i) == -1:
                moves.append(Move(x,y,self.get_top_free_space(y-i),y-i))
                self.swap(x,y,self.get_top_free_space(y-i),y-i)
                return
            if y+i < len(self.containers) and self.get_top_container(y+i) == -1:
                moves.append(Move(x,y,self.get_top_free_space(y+i),y+i))
                self.swap(x,y,self.get_top_free_space(y+i),y+i)
                return
        moves.append(Move(x,y,-3,-3))

    def transfer_list_on(self,cont: container):
        (x,y) = self.get_closest_spot()
        move = Move(0,0,x,y)
        self.containers[x][y] = cont
        return self.shortest_path(move)

    def get_container(self,x,y):
        return self.containers[x][y]

    def move(self,move: Move):
        self.containers[move.x1][move.y1] , self.containers[move.x2][move.y2] = self.containers[move.x2][move.y2] , self.containers[move.x1][move.y1]

    def swap(self,x1,y1,x2,y2):
        self.containers[x1][y1] , self.containers[x2][y2] = self.containers[x2][y2] , self.containers[x1][y1]

    def get_top_free_space(self,x):
        dim = len(self.containers)
        #Returns top container OR the first blocked space, be careful
        for i in range(dim):
            if (self.containers[i][x] != 0):
                if (i != 0):
                    return i - 1
                else:
                    return -1
        if self.containers[dim-1][x] == 0:
            return dim-1
        else:
            return -1
    
    def get_top_container(self,x):
        for i in range(len(self.containers)):
            if (self.containers[i][x] != 0 and self.containers[i][x] != -1):
                return i
        return -1
            
    def put_top(self,column,x1,y1):
        j = self.get_top_free_space(column)
        if j == -1:
            return False
        else:
            self.swap(j,column,x1,y1)
            return True

    def get_sums(self):
        dim = len(self.containers)
        dim2 = int(len(self.containers[0])/2)
        sum_l = 0
        sum_r = 0
        for i in range(dim):
            for j in range(dim2):
                if self.containers[i][j] != -1 and self.containers[i][j] != 0:
                    sum_l += self.containers[i][j].mass
        for i in range(dim):
            for j in range(dim2,len(self.containers[0])):
                if self.containers[i][j] != -1 and self.containers[i][j] != 0:
                    sum_r += self.containers[i][j].mass
        return (sum_l,sum_r)
    
    def is_balanced(self) -> bool:
        sum_l,sum_r = self.get_sums()
        return (
            max(sum_l,sum_r) <= 1.1*min(sum_l,sum_r)
        )
    
    def check_balance(self,left,right) -> bool:
        return(max(left,right) <= 1.1*min(left,right))
    
    def heuristic(self):
        heur = self.last_cost
        dim = len(self.containers)
        dim2 = len(self.containers[0])
        l_sum,r_sum = self.get_sums()
        balanced_mass = float((l_sum + r_sum)/2)
        defecit = float(max(l_sum,r_sum)-balanced_mass)
        if (l_sum < r_sum):
            for i in reversed(sorted(self.right_set)):
                if i.mass <= defecit:
                    heur = heur + abs(i.col - (len(self.containers[0])/2-1))
                    defecit = defecit - i.mass 
        else:
            for i in reversed(sorted(self.left_set)):
                if i.mass <= defecit:
                    heur = heur + abs(i.col - len(self.containers[0])/2)
                    defecit = defecit - i.mass 
        return heur

    def __repr__(self):
        return ",\n".join(map(str, self.containers))

    def __str__(self):
        return ",\n".join(map(str, self.containers))
    
    def shortest_path(self, move: Move)->list:
        if move.x2 == -2:
            move_new = Move(move.x1,move.y1,0,0)
            move_temp = self.shortest_path(move_new)
            move_temp.append([-1,0])
            move_temp.append([-2,-2])
        elif move.x2 == -3:
            move_new = Move(move.x1,move.y1,0,0)
            move_temp = self.shortest_path(move_new)
            move_temp.append([-1,0])
            move_temp.append([-3,-3])
        else:
            move_temp = []
            height_max = min(move.x1,move.x2)
            temp = 0
            for i in range(min(move.y1,move.y2),max(move.y1,move.y2)+1):
                height_max = min(height_max,self.get_top_free_space(i))
            print("MAX:",height_max)
            for i in range(move.x1,height_max,-1):
                move_temp.append([i,move.y1])
            temp = height_max
            if (move.y1 < move.y2):
                for i in range(move.y1,move.y2):
                    move_temp.append([temp,i])
            else:
                for i in range(move.y1,move.y2,-1):
                    move_temp.append([temp,i])
            for i in range(temp,move.x2):
                move_temp.append([i,move.y2])
            move_temp.append([move.x2,move.y2])
        return move_temp
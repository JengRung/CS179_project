#the main py file, still have yet to plan out the interaction between the wrapper/gui and the backend stuff
import container as cont
import a_star as ast


#Example list of containers
containers = [
    [-1,cont.container("Apples",6),-1,-1],
    [-1,cont.container("Oranges",10),cont.container("Cats",4),-1]
]
#print(*containers, sep = "\n")

#Example ship
ship = cont.ship(containers)

#A* would return moves up to n
moves = [cont.move(0,1,0,2),cont.move(1,1,0,1)]
#A move is in the format row,column

#moves can be used like this
#print(ship,'\n')
#ship.move(moves[0])
#print(ship,'\n')
#ship.move(moves[1])
print(ship)

node = ast.node(ship,0,0)
children = ast.expand(node)
for child in children:
    print(child,'\n\n')
print(ship)
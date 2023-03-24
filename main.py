import container as cont
import a_star as ast
import copy

#Test cases given by eamonn
test_blank = [
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
]
test1 = copy.deepcopy(test_blank)
for i in range(test1):
    for j in range(test1[0]):
        if i == 7 and j == 7: 
            test1[i][j] = cont.container("cat",99)
            test1[i][j] = cont.container("dog",100)

#Example ship
containers = test1
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

problem = ast.balance(ship)
ast.search(problem,trace=True)
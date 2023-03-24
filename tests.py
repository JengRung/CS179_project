import container as cont
import a_star as ast
import copy

#Test cases given by eamonn
test_blank = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
]
test1 = copy.deepcopy(test_blank)
for i in range(len(test1)):
    for j in range(len(test1[0])):
        if i == 7 and j == 1: 
            test1[i][j] = cont.container("cat",99)
        if i == 7 and j == 2:
            test1[i][j] = cont.container("dog",100)

test2 = copy.deepcopy(test_blank)
for i in range(len(test2)):
    for j in range(len(test2[0])):
        if i == 5 and j == 0: 
            test2[i][j] = cont.container("cat",99)
        if i == 6 and j == 1:
            test2[i][j] = cont.container("dog",100)
        if i == 7 and j == 3:
            test2[i][j] = cont.container("ram",120)
        if i == 7 and j == 8:
            test2[i][j] = cont.container("owl",100)
        if (i == 6 and j == 0) or (i == 7 and j == 0) or (i == 7 and j == 1) or (i == 7 and j == 2) or (i == 7 and j == 9) or (i == 7 and j == 10) or (i == 7 and j == 11) or (i == 6 and j == 11):
            test2[i][j] = -1

#Example ship
containers = test1
ship = cont.ship(containers)
print(ship.heuristic())
print("------- Start --------")

problem = ast.balance(ship)
node,depth,i = ast.search(problem,trace=True)
print(i)
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
        if i == 6 and j == 1:
            test1[i][j] = cont.container("dog",99)

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

test3 = copy.deepcopy(test_blank)
for i in range(len(test3)):
    for j in range(len(test3[0])):
        if i == 0 and j == 4: 
            test3[i][j] = cont.container("pig",99)
        if i == 1 and j == 4: 
            test3[i][j] = cont.container("doe",99)
        if i == 2 and j == 4: 
            test3[i][j] = cont.container("owl",99)
        if i == 3 and j == 4: 
            test3[i][j] = cont.container("ewe",99)
        if i == 4 and j == 4: 
            test3[i][j] = cont.container("cow",99)
        if i == 5 and j == 4: 
            test3[i][j] = cont.container("dog",99)
        if i == 6 and j == 4: 
            test3[i][j] = cont.container("cat",200)
        if i == 7 or i == 6 and (j == 0 or j == 11):
            test3[i][j] = -1


#Example of balance
print("-----balancing------")
containers = test3
ship = cont.ship(containers)
new_ship = ship.balance(ast.search,ast.balance(ship))
print(ship)
print(new_ship)
if new_ship == []:
    print("Ship can not be balanced")
else:
    print(new_ship.moves)
#print(ship.shortest_path(new_ship.moves[0]),'\n')
m = cont.Move(4,4,-2,-2)
print(new_ship.shortest_path(m))

print("-----Moving------")
moves_new = new_ship.transfer_list_off([[6,6]])
print(moves_new[0])
print(ship.shortest_path(moves_new[0]))
print(ship.shortest_path(moves_new[1]))
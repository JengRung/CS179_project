import numpy as np
import re
import container as cont

SHIP_CONTAINERS = [[None for x in range(12)] for y in range(9)]

container_pattern = r'(\[.*?\]),\s({.*?}),\s(.*)'

with open("manifests/ShipCase5.txt", "r") as file:
    for row in file:
        items = re.match(container_pattern, row)

        container_index, container_weight, container_name= items.groups()
        container_indexs = container_index.strip('[]').split(',')
        container_weight = int(container_weight.strip('{}'))
    
        if container_name.upper() == "NAN":
            SHIP_CONTAINERS[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = -1
        
        elif container_name.upper() == "UNUSED":
            SHIP_CONTAINERS[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = 0
            
        else:
            SHIP_CONTAINERS[int(container_indexs[0]) - 1][int(container_indexs[1]) - 1] = cont.container(container_name, container_weight)

print(SHIP_CONTAINERS)

for i in SHIP_CONTAINERS:
    for item in i:
        if type(item) == cont.container: 
            if item.name == "Cat":
                print("FOUND")
import json

import numpy as np
with open('Input data\level1b.json','r') as f:
    data = json.load(f)


def create_delivery_slots(distances, order_quantity, max_capacity):
    n = len(distances)
    orders = [(i, order_quantity[i]) for i in range(0, n-1)] 
    orders.sort(key=lambda x: x[1], reverse=True)  

    delivery_slots = []
    current_slot = [0]  
    current_capacity = 0

    while orders:
        next_order = orders.pop(0)
        if current_capacity + next_order[1] <= max_capacity:
            current_slot.append(next_order[0])
            current_capacity += next_order[1]
        else:
            current_slot.append(0)  # Return to 0th position
            delivery_slots.append(current_slot)
            current_slot = [0, next_order[0]]
            current_capacity = next_order[1]

    if current_slot:
        current_slot.append(0)  # Return to 0th position
        delivery_slots.append(current_slot)

    return delivery_slots 
  
fromneigh_dist=[]
for i in range (0,50):
    i = str(i)
    tempn = data["neighbourhoods"]["n"+i]["distances"]
    fromneigh_dist.append(tempn)

fromrest_dist = []
tempr = data["restaurants"]["r0"]["neighbourhood_distance"]
fromrest_dist.extend(tempr)

temprest = [0]
temprest.extend(fromrest_dist)

orderquantity = []
for i in range (0,50):
    i = str(i)
    temporder = data["neighbourhoods"]["n"+i]["order_quantity"]
    orderquantity.append(temporder)
#print(orderquantity)

fromneigh_dist.insert(0,fromrest_dist)

matrix = fromneigh_dist


output = [[v, *subl] for v, subl in zip(temprest, matrix)]
#print(output)


distances = np.array(output)

def format_path(slot):
    path = [f"n{neighborhood}" for neighborhood in slot[1:-1]]
    return [f"r{slot[0]}",*path,f"r{slot[-1]}"]
  
max_capacity = 1120

delivery_slots = create_delivery_slots(distances, orderquantity, max_capacity)

for i, slot in enumerate(delivery_slots, 1):
    print(f"Slot{i}: Orders {slot}")

result = {"v0": {}}
for i, slot in enumerate(delivery_slots, 1):
    path_key = f"path{i}"
    nodes = [f"n{node}" if node != 0 else "n0" for node in slot][1:-1]
    result["v0"][path_key] = [f"r0"] + nodes + [f"r0"]

json_output = json.dumps(result, indent=4)
print(json_output)
with open("level1b_output.json", "w") as outfile:
    outfile.write(json_output)

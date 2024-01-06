import json
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment


import numpy as np
with open('Input data\level1a.json','r') as f:
    data = json.load(f)


def create_delivery_slots(distances, order_quantity, max_capacity):
    n = len(distances)
    orders = [(i, order_quantity[i]) for i in range(0, n - 1)]
    orders.sort(key=lambda x: x[1], reverse=True)

    # Kruskal's algorithm for Minimum Spanning Tree
    edges = []
    for i in range(n - 1):
        for j in range(i + 1, n):
            edges.append((i, j, distances[i][j]))

    edges.sort(key=lambda x: x[2])
    parent = [i for i in range(n)]
    rank = [0] * n

    def find_set(x):
        if parent[x] != x:
            parent[x] = find_set(parent[x])
        return parent[x]

    def union_sets(x, y):
        root_x = find_set(x)
        root_y = find_set(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1

    minimum_spanning_tree = []
    for edge in edges:
        u, v, weight = edge
        if find_set(u) != find_set(v):
            union_sets(u, v)
            minimum_spanning_tree.append(edge)

    # Extract paths from the minimum spanning tree
    paths = {i: [] for i in range(n)}
    for edge in minimum_spanning_tree:
        u, v, _ = edge
        paths[u].append(v)
        paths[v].append(u)

    # Generate delivery slots
        """
    delivery_slots = []
    current_capacity = 0
    visited = [False] * n

    def dfs(node, slot):
        if not visited[node]:
            visited[node] = True
            slot.append(node)
            for neighbor in paths[node]:
                dfs(neighbor, slot)

    for i in range(n):
        if not visited[i]:
            current_slot = [0]
            dfs(i, current_slot)
            delivery_slots.append(current_slot)"""
        
    delivery_slots = []
    current_slot = [0]
    current_capacity = 0
    current_path = 1

    def start_new_path():
        nonlocal current_slot, current_capacity, current_path
        current_slot.append(0)  # Return to 0th position
        delivery_slots.append(current_slot)
        current_slot = [0, next_order[0]]
        current_capacity = next_order[1]
        current_path += 1

    while orders:
        next_order = orders.pop(0)
        if current_capacity + next_order[1] <= max_capacity:
            current_slot.append(next_order[0])
            current_capacity += next_order[1]
        else:
            start_new_path()

    if current_slot:
        start_new_path()
    
    return delivery_slots
  
fromneigh_dist=[]
for i in range (0,20):
    i = str(i)
    tempn = data["neighbourhoods"]["n"+i]["distances"]
    fromneigh_dist.append(tempn)

fromrest_dist = []
tempr = data["restaurants"]["r0"]["neighbourhood_distance"]
fromrest_dist.extend(tempr)

temprest = [0]
temprest.extend(fromrest_dist)

orderquantity = []
for i in range (0,20):
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
  

distances = np.array(output)

max_capacity = 600

def calculate_path_cost(path, distances):
    cost = 0
    for i in range(len(path) - 1):
        cost += distances[path[i], path[i + 1]]
    return cost


row_ind, col_ind = linear_sum_assignment(distances)

optimal_order = col_ind.argsort()
delivery_paths = []
current_path = [0]  # Starting point
current_capacity = 0

for i in optimal_order:
    if current_capacity + orderquantity[i] <= max_capacity:
        current_path.append(i + 1)  # +1 to match your node numbering
        current_capacity += orderquantity[i]
    else:
        delivery_paths.append(current_path + [0])  # Return to starting point
        current_path = [0, i + 1]
        current_capacity = orderquantity[i]

if current_path:
    delivery_paths.append(current_path + [0])

# Print or save the optimized paths
for i, path in enumerate(delivery_paths, 1):
    print(f"Path {i}: Orders {path}")

result = {"v0": {}}
for i, path in enumerate(delivery_paths):
    path_key = f"path{i + 1}"
    nodes = [f"n{node}" if node != 0 else "n0" for node in path]
    result["v0"][path_key] = [f"r0"] + nodes + [f"r0"]

json_output = json.dumps(result, indent=4)
print(json_output)

with open("level1a_testoutput1.json", "w") as outfile:
    outfile.write(json_output)
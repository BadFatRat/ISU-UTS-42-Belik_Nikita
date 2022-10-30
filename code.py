import random
from iteration_utilities import deepflatten

def get_adjacent_indices(i, j, m, n):
    adjacent_indices = []
    if i > 0:
        adjacent_indices.append((i-1,j))
    if i+1 < m:
        adjacent_indices.append((i+1,j))
    if j > 0:
        adjacent_indices.append((i,j-1))
    if j+1 < n:
        adjacent_indices.append((i,j+1))
    return adjacent_indices

def list_split(lst, n):
    for i in range(0,len(lst),n):
        yield lst[i:i+n]

def get_all_elements_in_list_of_lists(lst):
    count = 0
    for element in lst:
        count += len(element)
    return count

def bfs(info, start, finish, targets, loop):
    is_finished = False
    queue = [(start)]
    path1 = []
    nodes_checked = 0
    memory = 0
    while queue:
        path = queue.pop(0) ## get the first path from the queue
        node = path[-1] ## get the last node from the path
        if len(list(deepflatten(queue))) > memory:
            memory = len(list(deepflatten(queue)))
        if type(node) == int:
            node = (path[-2],path[-1])
        if info[node[0]][node[1]] == 5:
            info[node[0]][node[1]] = 0
            targets.pop(targets.index(node))
            path1.append(path)
            path.pop(-1)
            path2 = bfs(info, node, finish, targets, 0)
            nodes_checked += path2.pop(-1)
            x = path2.pop(-1)
            if x > memory:
                memory = x
            for item in path2:
                path1.append(item)
            is_finished = True
            node = finish
        if (node == finish and len(targets) == 0) or (is_finished == True):
            path1.append(path)
            path1.append(nodes_checked)
            path1.append(memory)
            return path1
        for adjacent in get_adjacent_indices(node[0],node[1],field_size,field_size):
            nodes_checked += 1
            if info[adjacent[0]][adjacent[1]] != -1: ## check if the path is blocked by obstacle
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)

field_size = 4
nodes = [[0 for i in range(field_size)] for j in range(field_size)] ## contains ccordinates of each node
for i in range(field_size):
    for j in range(field_size):
        nodes[i].pop(j)
        nodes[i].insert(j,(i,j))

rnd, x = 0,0
start, finish = (0,0),(0,0)
targets = []
obstacles = []
nodes_info = [[0 for i in range(field_size)] for j in range(field_size)] ## contains information about each node
while rnd <= 7: ## filling nodes with information
    if rnd == 0: x = 1 ## starting point
    if rnd == 1: x = -1 ## obstacles
    if rnd == 4: x = 5 ## target points
    if rnd == 7: x = 10 ## final point
    i,j = random.randint(0,3), random.randint(0,3)
    if nodes_info[i][j] == 0:
        nodes_info[i][j] = x
        rnd=rnd+1
        if x == 1: start = (i,j)
        if x == -1: obstacles.append((i,j))
        if x == 5: targets.append((i,j))
        if x == 10: finish = (i,j)
print('Nodes information:')
for i in nodes_info: print(i)
print('Nodes coordinates:')
for i in nodes: print(i)
print('start = ',start)
print('obstacles = ',obstacles)
print('targets = ',targets)
print('finish = ',finish)

answer = bfs(nodes_info, start, finish, targets, 1)
max_memory_used = answer.pop(-1)
nodes_pased = answer.pop(-1)
for i in range(3): answer.pop(-1)
answer1 = list_split(list(deepflatten(answer)),2)
answer2 = list_split(list(deepflatten(answer)),2)
visualisation = [['    ' for i in range(field_size)] for j in range(field_size)]
for node in answer1:
    visualisation[node[0]][node[1]] = (node[0], node[1])
print('Path in coordinates list: ',list(answer2))
for i in visualisation: print(i)
print('Nodes pased: ', nodes_pased)
print('Maximum memory used:', max_memory_used)

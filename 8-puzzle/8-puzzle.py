#!/usr/bin/python

import copy
import time

initial_board = [[1, 3, 4], [8, 6, 2], [7, 0, 5]];
#final_board = [[1, 3, 4], [8, 6, 2], [0, 7, 5]];
final_board = [[1, 2, 3], [8, 0, 4], [7, 6, 5]];

def move(node, x, y, dx, dy):
    new_matrix = copy.deepcopy(node.matrix)
    new_matrix[x][y] = new_matrix[x + dx][y + dy]
    new_matrix[x + dx][y + dy] = 0
    return Node(new_matrix, node.depth + 1, node);

class Node:
    def __init__(self, matrix, depth=None, parent=None):
        self.matrix = matrix
        for x in range(3):
            for y in range(3):
                if self.matrix[x][y] == 0:
                    self.blank_tile = (x, y)
        self.parent = parent
        self.depth = depth

    def goal_test(self):
        return self.matrix == final_state.matrix

    def moves(self):
        children = []
        x, y =  self.blank_tile
        if x > 0:
            children.append(move(self, x, y, -1, 0))
        if x < 2:
            children.append(move(self, x, y, +1, 0))
        if y > 0:
            children.append(move(self, x, y, 0, -1))
        if y < 2:
            children.append(move(self, x, y, 0, +1))
        return children

    def if_already_visited(self, visited):
        for node in visited:
            if node.matrix == self.matrix:
                return True
        return False

class Result:
    def __init__(self, node, mem_needed, steps):
        self.node = node
        self.mem_needed = mem_needed
        self.steps = steps

    def update(self, other):
        self.node = other.node
        self.mem_needed = max(self.mem_needed, other.mem_needed)
        self.steps += other.steps

def final_pos(node):
    finalpos = {}
    for x in range(3):
        for y in range(3):
            finalpos[node.matrix[x][y]] = (x,y)
    return finalpos

# Queue - for BFS
def fifo_queue(nodes, new_nodes, depth=None):
    nodes.extend(new_nodes)
    return nodes

#Stack - for DFS
def lifo_queue(nodes, new_nodes, depth=None):
    new_nodes.extend(nodes)
    return new_nodes

#Stack - for IDFS
def lifo_ids_queue(nodes, new_nodes, depth):
    if (new_nodes[0].depth <= depth):
        new_nodes.extend(nodes)
        return new_nodes
    return nodes

#Priority Queue - for Greedy BFS
def pq_greedy(nodes, new_nodes, depth=None):
    nodes.extend(new_nodes)
    sorted(nodes, key = eval_fun_greedy)
    #nodes.sort(cmp)
    return nodes

#Priority Queue - for A-Star
def pq_astar(nodes, new_nodes, depth=None):
    nodes.extend(new_nodes)
    sorted(nodes, key = eval_fun_astar)
    #nodes.sort(cmp)
    return nodes

#Priority Queue - for IDA-Star
def pq_idastar(nodes, new_nodes, depth=None):
    if (new_nodes[0].depth <= depth):
        nodes.extend(new_nodes)
    sorted(nodes, key = eval_fun_astar)
    #nodes.sort(cmp)
    return nodes

def manhattanDist_heur(node):
    cost = 0
    for x in range(3):
        for y in range(3):
            x_final, y_final = finalpos_map[node.matrix[x][y]]
            cost += abs(x_final - x) + (y_final - y)
    return cost

def outOfPlace_heur(node):
    cost = 0
    for x in range(3):
        for y in range(3):
            if (x, y) != finalpos_map[node.matrix[x][y]]:
                cost += 1
    return cost

def heuristic(node):
    return manhattanDist_heur(node)

def eval_fun_greedy(node):
    return heuristic(node)

def eval_fun_astar(node):
    return heuristic(node) + node.depth

def search(initial_state, queue_fn, depth=None):
    max_nodes = 1
    steps = 0
    nodes = [initial_state]
    visited = []
    while nodes:
        node = nodes.pop(0)
        if node.if_already_visited(visited):
            continue
        visited.append(node)
        if node.goal_test():
            print("goal found")
            return Result(node, max_nodes, steps);
        new_nodes = node.moves()
        nodes = queue_fn(nodes, new_nodes, depth)
        max_nodes = max(max_nodes, len(nodes))
        steps += 1
    print("goal not found")
    return Result(None, max_nodes, steps)

def dfs(initial_state):
    return search(initial_state, lifo_queue)

def bfs(initial_state):
    return search(initial_state, fifo_queue)

def ids(initial_state, max_depth):
    result = Result(None, 0, 0)
    for depth in range(max_depth + 1):
        print("Depth : ", depth)
        temp_result = search(initial_state, lifo_ids_queue, depth)
        result.update(temp_result)
        if result.node:
            break
    return result

def greedy_bfs(initial_state):
    return search(initial_state, pq_greedy)

def astar(initial_state):
    return search(initial_state, pq_astar)

def idastar(initial_state, max_depth):
    result = Result(None, 0, 0)
    for depth in range(max_depth + 1):
        print("Depth : ", depth)
        temp_result = search(initial_state, pq_idastar, depth)
        result.update(temp_result)
        if result.node:
            break
    return result

def print_path(node, path):
    if (node == None or node.parent == None):
        return
    print_path(node.parent, path)
    x, y = node.blank_tile
    x1, y1 = node.parent.blank_tile
    if (x == x1 + 1):
        #print("DOWN ")
        path.append("DOWN")
    elif (x == x1 - 1):
        #print("UP ")
        path.append("UP")
    elif (y == y1 + 1):
        #print("RIGHT ")
        path.append("RIGHT")
    else:
        #print("LEFT ")
        path.append("LEFT")

if __name__ == '__main__':
    start = time.time()
    initial_state = Node(initial_board, 0);
    final_state = Node(final_board);
    finalpos_map = final_pos(final_state)

    #DFS
    print("\ndfs ----\n");
    result = dfs(initial_state)
    print("memory needed : ", result.mem_needed, " \nnodes visited : ", result.steps)
    stop = time.time()
    #print("time : ", stop - start)
    path = []
    print_path(result.node, path)
    print("path : ", path)

    #BFS
    print("\nbfs ---- \n");
    result = bfs(initial_state)
    print("memory needed : ", result.mem_needed, " \nnodes visited : ", result.steps)
    stop = time.time()
    #print("time : ", stop - start)
    path = []
    print_path(result.node, path)
    print("path : ", path)

    #IDS
    depth_ids = 3
    print("\nids ---- max depth : ", depth_ids, "\n");
    result = ids(initial_state, depth_ids)
    print("memory needed : ", result.mem_needed, " \nnodes visited : ", result.steps)
    stop = time.time()
    #print("time : ", stop - start)
    path = []
    print_path(result.node, path)
    print("path : ", path)

    #Greedy - BFS
    print("\ng-bfs -----\n");
    result = greedy_bfs(initial_state)
    print("memory needed : ", result.mem_needed, " \nnodes visited : ", result.steps)
    stop = time.time()
    #print("time : ", stop - start)
    path = []
    print_path(result.node, path)
    print("path : ", path)

    #A-STAR
    print("\na-star -----\n");
    result = astar(initial_state)
    print("memory needed : ", result.mem_needed, " \nnodes visited : ", result.steps)
    stop = time.time()
    #print("time : ", stop - start)
    path = []
    print_path(result.node, path)
    print("path : ", path)

    #IDA-STAR
    print("\nida-star ----- max depth : ", depth_ids, "\n")
    depth_ids = 3
    result = idastar(initial_state, depth_ids)
    print("memory needed : ", result.mem_needed, " \nnodes visited : ", result.steps)
    stop = time.time()
    #print("time : ", stop - start)
    path = []
    print_path(result.node, path)
    print("path : ", path)

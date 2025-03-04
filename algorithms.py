import time, math, heapq

class Node:
    __slots__ = ("x", "y", "parent", "g", "h", "f")  # Reduce el uso de memoria

    def __init__(self, x, y, parent=None, g=0, h=0):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = g  # costo acumulado
        self.h = h  # heurística
        self.f = g + h  # costo total

    def __lt__(self, other):
        return self.f < other.f

def manhattan(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def euclidean(node, goal):
    return math.hypot(node.x - goal.x, node.y - goal.y)  # Más eficiente que sqrt

def get_neighbors(node, labyrinth):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = []
    rows, cols = len(labyrinth), len(labyrinth[0])
    for dx, dy in moves:
        nx, ny = node.x + dx, node.y + dy
        if 0 <= nx < rows and 0 <= ny < cols and labyrinth[nx][ny] != 1:
            neighbors.append((nx, ny))  # Se devuelve la tupla (x, y)
    return neighbors

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]

def bfs(labyrinth, start, goals):
    start_time = time.time()
    frontier = [Node(*start)]
    visited = {(start[0], start[1])}  # marcamos al agregar
    nodes_expanded = 0
    total_children = 0
    while frontier:
        node = frontier.pop(0)  # FIFO
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            return node, nodes_expanded, time.time() - start_time, total_children / nodes_expanded
        for nx, ny in get_neighbors(node, labyrinth):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                frontier.append(Node(nx, ny, parent=node))
                total_children += 1
    return None, nodes_expanded, time.time() - start_time, 0

def dfs(labyrinth, start, goals):
    start_time = time.time()
    frontier = [Node(*start)]
    visited = {(start[0], start[1])}  # marcamos al agregar
    nodes_expanded = 0
    total_children = 0
    while frontier:
        node = frontier.pop()  # LIFO
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            return node, nodes_expanded, time.time() - start_time, total_children / nodes_expanded
        for nx, ny in reversed(get_neighbors(node, labyrinth)):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                frontier.append(Node(nx, ny, parent=node))
                total_children += 1
    return None, nodes_expanded, time.time() - start_time, 0

def greedy_best_first(labyrinth, start, goals, heuristic_func):
    start_time = time.time()
    start_node = Node(*start)
    goal_nodes = [Node(g[0], g[1]) for g in goals]
    start_node.h = min(heuristic_func(start_node, g) for g in goal_nodes)
    frontier = [(start_node.h, start_node)]
    visited = {(start_node.x, start_node.y)}
    nodes_expanded = 0
    total_children = 0
    while frontier:
        _, node = heapq.heappop(frontier)
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            return node, nodes_expanded, time.time() - start_time, total_children / nodes_expanded
        for nx, ny in get_neighbors(node, labyrinth):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                neighbor = Node(nx, ny, parent=node)
                neighbor.h = min(heuristic_func(neighbor, g) for g in goal_nodes)
                heapq.heappush(frontier, (neighbor.h, neighbor))
                total_children += 1
    return None, nodes_expanded, time.time() - start_time, 0

def a_star(labyrinth, start, goals, heuristic_func):
    start_time = time.time()
    start_node = Node(*start)
    goal_nodes = [Node(g[0], g[1]) for g in goals]
    start_node.h = min(heuristic_func(start_node, g) for g in goal_nodes)
    start_node.f = start_node.h
    frontier = [(start_node.f, start_node)]
    explored = {}
    nodes_expanded = 0
    total_children = 0
    while frontier:
        _, node = heapq.heappop(frontier)
        # Si ya se expandió este nodo con un costo menor, se descarta sin contar
        if (node.x, node.y) in explored and explored[(node.x, node.y)] <= node.g:
            continue
        # Ahora se cuenta el nodo, ya que no es duplicado
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            return node, nodes_expanded, time.time() - start_time, total_children / nodes_expanded
        explored[(node.x, node.y)] = node.g
        for nx, ny in get_neighbors(node, labyrinth):
            tentative_g = node.g + 1
            if (nx, ny) in explored and explored[(nx, ny)] <= tentative_g:
                continue
            neighbor = Node(nx, ny, parent=node, g=tentative_g)
            neighbor.h = min(heuristic_func(neighbor, g) for g in goal_nodes)
            neighbor.f = neighbor.g + neighbor.h
            heapq.heappush(frontier, (neighbor.f, neighbor))
            total_children += 1
    return None, nodes_expanded, time.time() - start_time, 0

def run_experiment(labyrinth, start, goals):
    results = {}

    # DFS
    sol, n_exp, t_exec, bf = dfs(labyrinth, start, goals)
    results['DFS'] = {
        'path': reconstruct_path(sol) if sol else None,
        'nodes_expanded': n_exp,
        'time': t_exec,
        'branching_factor': bf
    }

    # BFS
    sol, n_exp, t_exec, bf = bfs(labyrinth, start, goals)
    results['BFS'] = {
        'path': reconstruct_path(sol) if sol else None,
        'nodes_expanded': n_exp,
        'time': t_exec,
        'branching_factor': bf
    }

    # Greedy Best First con Manhattan
    sol, n_exp, t_exec, bf = greedy_best_first(labyrinth, start, goals, manhattan)
    results['Greedy_Manhattan'] = {
        'path': reconstruct_path(sol) if sol else None,
        'nodes_expanded': n_exp,
        'time': t_exec,
        'branching_factor': bf
    }

    # Greedy Best First con Euclidiana
    sol, n_exp, t_exec, bf = greedy_best_first(labyrinth, start, goals, euclidean)
    results['Greedy_Euclidean'] = {
        'path': reconstruct_path(sol) if sol else None,
        'nodes_expanded': n_exp,
        'time': t_exec,
        'branching_factor': bf
    }

    # A* con Manhattan
    sol, n_exp, t_exec, bf = a_star(labyrinth, start, goals, manhattan)
    results['A*_Manhattan'] = {
        'path': reconstruct_path(sol) if sol else None,
        'nodes_expanded': n_exp,
        'time': t_exec,
        'branching_factor': bf
    }

    # A* con Euclidiana
    sol, n_exp, t_exec, bf = a_star(labyrinth, start, goals, euclidean)
    results['A*_Euclidean'] = {
        'path': reconstruct_path(sol) if sol else None,
        'nodes_expanded': n_exp,
        'time': t_exec,
        'branching_factor': bf
    }

    return results

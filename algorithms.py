import time, math, heapq, random

# Clase Node y funciones auxiliares
class Node:
    def __init__(self, x, y, parent=None, g=0, h=0):
        self.x = x  # fila
        self.y = y  # columna
        self.parent = parent
        self.g = g  # costo acumulado
        self.h = h  # costo heurístico
        self.f = g + h  # costo total

    def __lt__(self, other):
        return self.f < other.f

def manhattan(node, goal):
    #Heurística de Manhattan
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def euclidean(node, goal):
    #Heurística Euclidiana
    return math.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2)

def get_neighbors(node, labyrinth):
    
    #Jerarquía de movimientos: Arriba, Derecha, Abajo, Izquierda.
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    neighbors = []
    rows = len(labyrinth)
    cols = len(labyrinth[0])
    for dx, dy in moves:
        new_x = node.x + dx
        new_y = node.y + dy
        if 0 <= new_x < rows and 0 <= new_y < cols:
            if labyrinth[new_x][new_y] != 1:
                neighbors.append(Node(new_x, new_y, parent=node))
    return neighbors

def reconstruct_path(node):
    #Reconstruye el camino desde el nodo final hasta el inicial
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]

# Algoritmos de búsqueda 

def bfs(labyrinth, start, goals):
    start_time = time.time()
    frontier = [Node(start[0], start[1])]
    explored = set()
    nodes_expanded = 0
    total_children = 0
    while frontier:
        node = frontier.pop(0)  # FIFO
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            end_time = time.time()
            bf = total_children / nodes_expanded if nodes_expanded else 0
            return node, nodes_expanded, end_time - start_time, bf
        explored.add((node.x, node.y))
        children = []
        for neighbor in get_neighbors(node, labyrinth):
            if (neighbor.x, neighbor.y) not in explored and \
               all(not (n.x == neighbor.x and n.y == neighbor.y) for n in frontier):
                children.append(neighbor)
        total_children += len(children)
        frontier.extend(children)
    end_time = time.time()
    bf = total_children / nodes_expanded if nodes_expanded else 0
    return None, nodes_expanded, end_time - start_time, bf

def dfs(labyrinth, start, goals):
    start_time = time.time()
    frontier = [Node(start[0], start[1])]
    explored = set()
    nodes_expanded = 0
    total_children = 0
    while frontier:
        node = frontier.pop()  # LIFO
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            end_time = time.time()
            bf = total_children / nodes_expanded if nodes_expanded else 0
            return node, nodes_expanded, end_time - start_time, bf
        explored.add((node.x, node.y))
        children = []
        # Usamos reversed para mantener la jerarquía de movimientos
        for neighbor in reversed(get_neighbors(node, labyrinth)):
            if (neighbor.x, neighbor.y) not in explored and \
               all(not (n.x == neighbor.x and n.y == neighbor.y) for n in frontier):
                children.append(neighbor)
        total_children += len(children)
        frontier.extend(children)
    end_time = time.time()
    bf = total_children / nodes_expanded if nodes_expanded else 0
    return None, nodes_expanded, end_time - start_time, bf

def greedy_best_first(labyrinth, start, goals, heuristic_func):
    start_time = time.time()
    start_node = Node(start[0], start[1])
    start_node.h = min(heuristic_func(start_node, Node(g[0], g[1])) for g in goals)
    frontier = []
    heapq.heappush(frontier, (start_node.h, start_node))
    explored = set()
    nodes_expanded = 0
    total_children = 0
    while frontier:
        _, node = heapq.heappop(frontier)
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            end_time = time.time()
            bf = total_children / nodes_expanded if nodes_expanded else 0
            return node, nodes_expanded, end_time - start_time, bf
        explored.add((node.x, node.y))
        children = []
        for neighbor in get_neighbors(node, labyrinth):
            if (neighbor.x, neighbor.y) not in explored:
                neighbor.h = min(heuristic_func(neighbor, Node(g[0], g[1])) for g in goals)
                children.append(neighbor)
                heapq.heappush(frontier, (neighbor.h, neighbor))
        total_children += len(children)
    end_time = time.time()
    bf = total_children / nodes_expanded if nodes_expanded else 0
    return None, nodes_expanded, end_time - start_time, bf

def a_star(labyrinth, start, goals, heuristic_func):
    start_time = time.time()
    start_node = Node(start[0], start[1])
    start_node.g = 0
    start_node.h = min(heuristic_func(start_node, Node(g[0], g[1])) for g in goals)
    start_node.f = start_node.g + start_node.h
    frontier = []
    heapq.heappush(frontier, (start_node.f, start_node))
    explored = {}
    nodes_expanded = 0
    total_children = 0
    while frontier:
        _, node = heapq.heappop(frontier)
        nodes_expanded += 1
        if (node.x, node.y) in goals:
            end_time = time.time()
            bf = total_children / nodes_expanded if nodes_expanded else 0
            return node, nodes_expanded, end_time - start_time, bf
        if (node.x, node.y) in explored and explored[(node.x, node.y)] <= node.g:
            continue
        explored[(node.x, node.y)] = node.g
        children = []
        for neighbor in get_neighbors(node, labyrinth):
            tentative_g = node.g + 1
            if (neighbor.x, neighbor.y) in explored and explored[(neighbor.x, neighbor.y)] <= tentative_g:
                continue
            neighbor.g = tentative_g
            neighbor.h = min(heuristic_func(neighbor, Node(g[0], g[1])) for g in goals)
            neighbor.f = neighbor.g + neighbor.h
            children.append(neighbor)
            heapq.heappush(frontier, (neighbor.f, neighbor))
        total_children += len(children)
    end_time = time.time()
    bf = total_children / nodes_expanded if nodes_expanded else 0
    return None, nodes_expanded, end_time - start_time, bf

def run_experiment(labyrinth, start, goals):
    #Ejecuta todos los algoritmos con un punto de partida dado
    results = {}

    # DFS
    sol, n_exp, t_exec, bf = bfs(labyrinth, start, goals)
    results['DFS'] = {
        'path': reconstruct_path(sol) if sol else None,
        'nodes_expanded': n_exp,
        'time': t_exec,
        'branching_factor': bf
    }

    # BFS
    sol, n_exp, t_exec, bf = dfs(labyrinth, start, goals)
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

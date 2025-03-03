import numpy as np
from matplotlib.colors import ListedColormap

def read_labyrinth(file_path):
    #Lee el laberinto desde un archivo .txt.
    labyrinth = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                row = [int(x) for x in line.split(',') if x != '']
                labyrinth.append(row)
    return labyrinth

def read_labyrinth_from_lines(lines):
    labyrinth = []
    for line in lines:
        line = line.strip()
        if line:
            row = [int(x) for x in line.split(',') if x != '']
            labyrinth.append(row)
    return labyrinth

def find_points(labyrinth):
    #Extrae los puntos de partida y puntos de salida
    start_points = []
    goal_points = []
    for i in range(len(labyrinth)):
        for j in range(len(labyrinth[0])):
            if labyrinth[i][j] == 2:
                start_points.append((i, j))
            elif labyrinth[i][j] == 3:
                goal_points.append((i, j))
    return start_points, goal_points

def get_colormap():
    #Colormap para la visualización:
    #  - 0: camino libre (blanco)
    #  - 1: pared (negro)
    #  - 2: punto de partida (verde)
    #  - 3: punto de salida (rojo)
    cmap = ListedColormap(["white", "black", "green", "red"])
    return cmap

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

from labyrinth import read_labyrinth_from_lines, find_points, get_colormap
from algorithms import run_experiment

st.set_page_config(page_title="Búsqueda en Laberintos", layout="wide")
st.title("Visualización de Algoritmos de Búsqueda en Laberintos")

# Subir archivo del laberinto
lab_file = st.file_uploader("Cargar archivo de laberinto (.txt)", type=["txt"])
if lab_file is not None:
    # Se lee el contenido subido y se procesa
    content = lab_file.read().decode("utf-8").splitlines()
    labyrinth = read_labyrinth_from_lines(content)
else:
    st.warning("Por favor, sube un archivo de laberinto para continuar.")
    st.stop()

# Visualización del laberinto
st.subheader("Laberinto")
fig, ax = plt.subplots(figsize=(6,6))
cmap = get_colormap()
ax.imshow(np.array(labyrinth), cmap=cmap)
ax.set_xticks([]), ax.set_yticks([])
st.pyplot(fig)

# Extraer puntos de partida y de salida
start_points, goal_points = find_points(labyrinth)
if not start_points:
    st.error("No se encontró ningún punto de partida en el laberinto.")
    st.stop()
if not goal_points:
    st.error("No se encontró ningún punto de salida en el laberinto.")
    st.stop()

# Selección del tipo de experimento
experiment_type = st.radio("Selecciona el tipo de experimento", ("Caso Base", "Simulación con puntos de partida aleatorios"))

if experiment_type == "Caso Base":
    st.subheader("Experimento - Caso Base")
    # Permitir seleccionar el punto de partida si hay más de uno
    base_start = st.selectbox("Selecciona el punto de partida", start_points) if len(start_points) > 1 else start_points[0]
    st.write("Punto de partida base:", base_start)
    
    results = run_experiment(labyrinth, base_start, goal_points)
    
    st.markdown("### Resultados de la búsqueda")
    for algo, data in results.items():
        st.write(f"**Algoritmo: {algo}**")
        if data['path']:
            st.write("Longitud del camino:", len(data['path']))
        else:
            st.write("No se encontró solución.")
        st.write("Nodos expandidos:", data['nodes_expanded'])
        st.write("Tiempo de ejecución: {:.6f} s".format(data['time']))
        st.write("Branching Factor: {:.2f}".format(data['branching_factor']))
        st.markdown("---")
    
    selected_algo = st.selectbox("Selecciona el algoritmo para visualizar la solución", list(results.keys()))
    if results[selected_algo]['path']:
        st.subheader(f"Visualización de la solución - {selected_algo}")
        path = results[selected_algo]['path']
        fig2, ax2 = plt.subplots(figsize=(6,6))
        ax2.imshow(np.array(labyrinth), cmap=cmap)
        xs = [p[1] for p in path]
        ys = [p[0] for p in path]
        ax2.plot(xs, ys, color="blue", linewidth=2)
        ax2.set_xticks([]), ax2.set_yticks([])
        st.pyplot(fig2)
    else:
        st.info(f"El algoritmo {selected_algo} no encontró solución.")

elif experiment_type == "Simulación con puntos de partida aleatorios":
    st.subheader("Experimento - Simulación con puntos de partida aleatorios")
    # Obtener celdas libres (valor 0) para elegir puntos de partida aleatorios
    free_cells = [(i, j) for i in range(len(labyrinth)) for j in range(len(labyrinth[0])) if labyrinth[i][j] == 0]
    if not free_cells:
        st.error("No se encontraron celdas libres para puntos de partida aleatorios.")
        st.stop()
    num_points = st.slider("Número de puntos de partida aleatorios", 1, min(10, len(free_cells)), 3)
    random_starts = random.sample(free_cells, num_points)
    
    for start in random_starts:
        st.markdown(f"### Punto de partida: {start}")
        results = run_experiment(labyrinth, start, goal_points)
        for algo, data in results.items():
            st.write(f"**Algoritmo: {algo}**")
            if data['path']:
                st.write("Longitud del camino:", len(data['path']))
            else:
                st.write("No se encontró solución.")
            st.write("Nodos expandidos:", data['nodes_expanded'])
            st.write("Tiempo de ejecución: {:.6f} s".format(data['time']))
            st.write("Branching Factor: {:.2f}".format(data['branching_factor']))
            st.markdown("---")
        st.markdown("===================================")

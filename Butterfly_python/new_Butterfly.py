import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from mpl_toolkits.mplot3d import Axes3D

def generate_surface(subdivisions):
    # Création d'une grille initiale
    grid_size = subdivisions + 1
    vertices = np.zeros((grid_size, grid_size, 3))

    # Calcul des positions des sommets de la grille
    step_size = 1.0 / subdivisions
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * step_size
            y = row * step_size
            z = compute_vertex_position(x, y)
            vertices[row, col] = np.array([x, y, z])

    return vertices.reshape((-1, 3))


def compute_vertex_position(x, y):
    # Fonction de calcul de la position du sommet
    z = np.sin(x * np.pi) * np.cos(y * np.pi)  # Exemple de fonction de surface
    return z


def butterfly_interpolation(vertices, subdivisions):
    # Génération des triangles pour chaque patch
    triangles = []
    for row in range(subdivisions):
        for col in range(subdivisions):
            top_left = row * (subdivisions + 1) + col
            top_right = top_left + 1
            bottom_left = (row + 1) * (subdivisions + 1) + col
            bottom_right = bottom_left + 1

            # Sommets intermédiaires
            mid_top = (vertices[top_left] + vertices[top_right]) / 2.0
            mid_left = (vertices[top_left] + vertices[bottom_left]) / 2.0
            mid_right = (vertices[top_right] + vertices[bottom_right]) / 2.0
            mid_bottom = (vertices[bottom_left] + vertices[bottom_right]) / 2.0

            # Ajout des triangles Butterfly
            triangles.append([top_left, mid_top, mid_left])
            triangles.append([top_right, mid_right, mid_top])
            triangles.append([bottom_left, mid_left, mid_bottom])
            triangles.append([bottom_right, mid_bottom, mid_right])
            triangles.append([mid_top, mid_right, mid_bottom])
            triangles.append([mid_top, mid_bottom, mid_left])

    # Conversion en tableau numpy
    triangles = np.array(triangles)

    return triangles


# Paramètres de subdivision
subdivisions = 20

# Génération de la surface
vertices = generate_surface(subdivisions)

# Interpolation Butterfly
triangles = butterfly_interpolation(vertices, subdivisions)

# Coordonnées des sommets
x = vertices[:, 0]
y = vertices[:, 1]
z = vertices[:, 2]

# Création de l'objet triangulation
triang = mtri.Triangulation(x, y, triangles=triangles)

# Affichage de la surface triangulée en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(triang, z, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
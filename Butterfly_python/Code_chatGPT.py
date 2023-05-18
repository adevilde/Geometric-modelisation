import numpy as np
import matplotlib.pyplot as plt
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
            z = np.sin(x*y)
            vertices[row, col] = np.array([x, y, z])

    # Génération des triangles pour chaque patch
    triangles = []
    for row in range(subdivisions):
        for col in range(subdivisions):
            top_left = row * grid_size + col
            top_right = top_left + 1
            bottom_left = (row + 1) * grid_size + col
            bottom_right = bottom_left + 1

            # Triangle supérieur gauche
            triangles.extend([top_left, bottom_left, top_right])

            # Triangle inférieur droit
            triangles.extend([top_right, bottom_left, bottom_right])

    return vertices.reshape((-1, 3)), np.array(triangles, dtype=np.uint32)


# Exemple d'utilisation
subdivisions = 8
vertices, triangles = generate_surface(subdivisions)

# Affichage des sommets et des triangles
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(vertices[:, 0], vertices[:, 2], vertices[:, 1], triangles=triangles)
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y')
plt.show()

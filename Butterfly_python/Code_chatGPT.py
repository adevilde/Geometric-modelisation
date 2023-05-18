import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

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
            z = np.sin(x * np.pi) * np.cos(y * np.pi)  # Exemple de fonction de surface
            vertices[row, col] = np.array([x, y, z])

    return vertices.reshape((-1, 3))


def triangulate(subdivisions):
    vertices = generate_surface(subdivisions)
    x = vertices[:, 0]
    y = vertices[:, 1]
    z = vertices[:, 2]
    triang = mtri.Triangulation(x, y)
    return triang, z

# Exemple d'utilisation de la fonction triangulate
subdivisions = 20

# Triangularisation
triang, z = triangulate(subdivisions)

# Affichage de la surface triangulée en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(triang, z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

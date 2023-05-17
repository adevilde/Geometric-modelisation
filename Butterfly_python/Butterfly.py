import numpy as np
import matplotlib.pyplot as plt

size = 6

def init_surface(size):

    # Convert polar (radii, angles) coords to cartesian (x, y) coords.
    # (0, 0) is manually added at this stage,  so there will be no duplicate
    # points in the (x, y) plane.
    x = np.array([np.ones(size) * i for i in range(size)]).flatten()
    y = np.array([np.linspace(0, 1, size) for i in range(size)]).flatten()

    # Compute z to make the pringle surface.
    z = np.sin(x+y)
    
    return x, y, z


x, y, z = init_surface()
ax = plt.figure().add_subplot(projection='3d')

ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)

plt.show()





import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

size = 6

def init_surface(size):

    # Convert polar (radii, angles) coords to cartesian (x, y) coords.
    # (0, 0) is manually added at this stage,  so there will be no duplicate
    # points in the (x, y) plane.
    x = np.array([np.ones(size) * i for i in range(size)]).flatten()
    y = np.array([np.linspace(0, 1, size) for i in range(size)]).flatten()

    # Compute z to make the pringle surface.
    z = np.sin(x+y)
    tri = mtri.Triangulation(x, y)

    return x, y, z, tri.triangles

def get_butterfly(s, x, y, t):
    l0 = s
    c1 = [np.any(e == s[0]) & np.any(e == s[1]) for e in t]
    l1 = t[c1]
    c2 = [np.any(e == s[0]) & np.any(e == l1) for e in t]
    l2 = t[c2]
    return l0, l1, l2, c1

def split_triangle(t, x, y, z):

    for i in range(3):
        np.append((x[t[i]] + x[t[(i + 1) % 3]])/2, x)
        np.append((y[t[i]] + y[t[(i + 1) % 3]])/2, y)

    return

x, y, z, tri = init_surface(size)
l0, l1, l2, c = get_butterfly([tri[6, 0], tri[6, 1]],x, y, tri)
print([tri[6, 0], tri[6, 1]])
print(tri)
print(c)
print(l1)

ax = plt.figure().add_subplot(projection='3d')
ax.plot_trisurf(x, y, z, triangles = tri, linewidth=0.2, antialiased=True)

plt.show()





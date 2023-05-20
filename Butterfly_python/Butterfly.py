import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

size = 6
w = 1/16

def init_surface(size):

    x = np.array([np.ones(size) * i for i in range(size)]).flatten()
    y = np.array([np.linspace(0, 1, size) for i in range(size)]).flatten()
    z = np.sin(x+y)
    tri = mtri.Triangulation(x, y)

    return x, y, z, tri.triangles

def init_volume():
    x = np.array([0, 0, 2, 2, 1, 1])
    y = np.array([0, 2, 0, 2, 1, 1])
    z = np.array([5, 5, 5, 5, 0, 10])
    tri = np.array([
        [0, 1, 4],
        [0, 1, 5],
        [0, 2, 4],
        [0, 2, 5],
        [3, 1, 4],
        [3, 1, 5],
        [3, 2, 4],
        [3, 2, 5]
        ])
    return x, y, z, tri


def get_butterfly(s, x, y, tri):
    l0 = np.array(s)

    c1 = [np.any(e == s[0]) & np.any(e == s[1]) for e in tri]
    l01 = tri[c1]
    l1 = l01[np.isin(l01, l0, invert = True)]

    c2 = [np.any(np.isin(e, l0)) & np.any(np.isin(e, l1)) for e in tri]
    l2 = tri[c2]
    l2 = l2[np.isin(l2, l01, invert = True)]
    return l0, l1, l2

def split_triangle(ti, w, x, y, z, tri, refTri):

    t = tri[ti]
    nt = [[t[i]] for i in range(3)]
    nt = nt + [[]]
    for i in range(3):
        l0, l1, l2 = get_butterfly([t[i], t[(i + 1) % 3]], x, y, refTri)
        nx = 0.5 * sum(np.take(x, l0)) + 2 * w * sum(np.take(x, l1)) - w * np.sum(np.take(x, l2))
        ny = 0.5 * sum(np.take(y, l0)) + 2 * w * sum(np.take(y, l1)) - w * np.sum(np.take(y, l2))
        nz = 0.5 * sum(np.take(z, l0)) + 2 * w * sum(np.take(z, l1)) - w * np.sum(np.take(z, l2))
        cond = np.multiply(np.multiply(nx == x, ny == y), nz == z)
        loc = np.where(cond)
        if len(loc[0]) == 0:
            x = np.append(x, nx)
            y = np.append(y, ny)
            z = np.append(z, nz)
            j = len(x) - 1
        else:
            j = loc[0][0]
        nt[3] = nt[3] + [j]
        nt[i] = nt[i] + [j]
        nt[(i + 1) % 3] = nt[(i + 1) % 3] + [j]
    tri[ti] = nt[3]
    tri = np.append(tri, nt[:3], axis = 0)

    return x, y, z, tri

def fly_butterfly(x, y, z, tri, iteration_number):
    for i in range(iteration_number):
        tempTri = np.copy(tri)
        for ti in range(len(tempTri)):
            x, y, z, tri = split_triangle(ti, w, x, y, z, tri, tempTri)
    return x, y, z, tri



if __name__ == '__main__':
    ax = plt.figure().add_subplot(projection='3d')

    x, y, z, tri = init_volume()
    x, y, z, tri = fly_butterfly(x, y, z, tri, 3)

    ax.plot_trisurf(x, y, z, triangles = tri, linewidth=0.2, antialiased=True)

    plt.show()






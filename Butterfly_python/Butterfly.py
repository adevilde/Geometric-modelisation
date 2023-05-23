import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from scipy.spatial import Delaunay

size = 6
w = 1/16

def init_surface(size):

    x = np.array([np.ones(size) * i for i in range(size)]).flatten()
    y = np.array([np.linspace(0, 1, size) for i in range(size)]).flatten()
    # z = np.sin(x+y)
    z = 0 * x
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


def init_cube_KO():
    # Définition des points du cube
    points = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 1.0, 1.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [1.0, 1.0, 1.0],
        [1.0, 0.0, 1.0]
    ])

    x =[0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0]
    y =[0.0,1.0,1.0,0.0,0.0,1.0,1.0,0.0]
    z =[0.0,0.0,1.0,1.0,0.0,0.0,1.0,1.0]
# Définition des triangles du cube
    tri = np.array([
        [0, 1, 2], [0, 2, 3],  # Face avant
        [4, 5, 6], [4, 6, 7],  # Face arrière
        [0, 1, 4], [1, 4, 5],  # Côté gauche
        [2, 3, 6], [3, 6, 7],  # Côté droit
        [0, 3, 4], [3, 4, 7],  # Dessous
        [1, 2, 5], [2, 5, 6]   # Dessus
    ])
    return x, y, z, tri

def init_cube_OK():

    # Définition des points du cube
    x = np.array([0.0, 2.0, 0.0, 2.0, 0.0, 2.0, 0.0, 2.0, 1.0, 2.0, 1.0, 0.0, 1.0, 1.0])
    y = np.array([0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 2.0, 2.0, 0.0, 1.0, 2.0, 1.0, 1.0, 1.0])
    Z = np.array([2.0, 2.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 2.0])

    # Définition des triangles du cube
    tri = np.array([[0,1,8], [1,8,3], [3,8,2], [2,8,0],
                   [3,9,1], [1,9,5], [5,9,7], [7,9,3],
                   [4,10,5], [5,10,7], [7,10,6], [6,10,4],
                   [0,11,4], [4,11,6], [6,11,2], [2,11,0],
                   [2,12,6], [6,12,7], [7,12,3], [3,12,2],
                   [0,13,4], [4,13,5], [5,13,1], [1,13,0]])

    return x, y, Z, tri



def get_butterfly(s, tri):
    l0 = np.array(s)

    c1 = [np.any(e == s[0]) and np.any(e == s[1]) for e in tri]
    l01 = tri[c1]
    l1 = l01[np.isin(l01, l0, invert = True)]

    c2_up = [np.any(np.isin(e, l0)) and np.any(e == l1[0]) for e in tri]
    l2_up = tri[c2_up]
    l2_up = l2_up[np.isin(l2_up, l01, invert = True)]

    c2_down = [np.any(np.isin(e, l0)) and np.any(e == l1[0]) for e in tri]
    l2_down = tri[c2_down]
    l2_down = l2_down[np.isin(l2_down, l01, invert = True)]

    c20 = [np.any(np.isin(e, l0)) and np.any(np.isin(e, l1[0])) for e in tri]
    l20 = tri[c20]
    l20 = l20[np.isin(l20, l01[0], invert = True)]

    if len(l1) > 1:
        c21 = [np.any(np.isin(e, l0)) and np.any(np.isin(e, l1[1])) for e in tri]
        l21 = tri[c21]
        l21 = l21[np.isin(l21, l01[1], invert = True)]
        l2 = np.append(l20, l21)
    else :
        l2 = l20
    
        
    # if len(l2) <= 4:
    #     print(l2)
    #     print(len(l0), len(l1), len(l2))

    return l0, l1, l2, l2_up, l2_down


def calculate_new_point(l0, l1, l2_up, l2_down, w, x, y, z):

    if (len(l2_up) == 0 or len(l2_down) == 2):
        nx = 0.5 * sum(np.take(x, l0)) + 4 * w * x[l1[1]] - 2 * w * np.sum(np.take(x, l2_down))
        ny = 0.5 * sum(np.take(y, l0)) + 4 * w * y[l1[1]] - 2 * w * np.sum(np.take(y, l2_down))
        nz = 0.5 * sum(np.take(z, l0)) + 4 * w * z[l1[1]] - 2 * w * np.sum(np.take(z, l2_down))
    elif (len(l2_down) == 0 or len(l2_up) == 2):
        nx = 0.5 * sum(np.take(x, l0)) + 4 * w * x[l1[0]] - 2 * w * np.sum(np.take(x, l2_up))
        ny = 0.5 * sum(np.take(y, l0)) + 4 * w * y[l1[0]] - 2 * w * np.sum(np.take(y, l2_up))
        nz = 0.5 * sum(np.take(z, l0)) + 4 * w * z[l1[0]] - 2 * w * np.sum(np.take(z, l2_up))
    elif (len(l2_up) <= 1 and len(l2_down) <= 1):
        nx = 0.5 * sum(np.take(x, l0))
        ny = 0.5 * sum(np.take(y, l0))
        nz = 0.5 * sum(np.take(z, l0))
    else:
        nx = 0.5 * sum(np.take(x, l0)) + 2 * w * sum(np.take(x, l1)) - w * np.sum(np.take(x, l2))
        ny = 0.5 * sum(np.take(y, l0)) + 2 * w * sum(np.take(y, l1)) - w * np.sum(np.take(y, l2))
        nz = 0.5 * sum(np.take(z, l0)) + 2 * w * sum(np.take(z, l1)) - w * np.sum(np.take(z, l2))

    return nx, ny, nz


def split_triangle(ti, w, x, y, z, tri, refTri):

    t = tri[ti]
    nt = [[t[i]] for i in range(3)]  # coordonnées du triangle
    nt = nt + [[]]
    for i in range(3):
        s = [t[i], t[(i + 1) % 3]]
        # On restreint la recherche aux triangles qui ont un sommet commun avec le segment s
        # c = [np.any(e == s[0]) and np.any(e == s[1]) for e in refTri]
        # local_tri = refTri[c]

        l0, l1, l2, l2_up, l2_down = get_butterfly(s, refTri) # récupération des points du butterfly

        # nx, ny, nz = calculate_new_point(l0, l1, l2_up, l2_down, w, x, y, z)

        nx = 0.5 * sum(np.take(x, l0)) + 2 * w * sum(np.take(x, l1)) - w * np.sum(np.take(x, l2))
        ny = 0.5 * sum(np.take(y, l0)) + 2 * w * sum(np.take(y, l1)) - w * np.sum(np.take(y, l2))
        nz = 0.5 * sum(np.take(z, l0)) + 2 * w * sum(np.take(z, l1)) - w * np.sum(np.take(z, l2))

        cond = np.multiply(np.multiply(nx == x, ny == y), nz == z)
        loc = np.asarray(cond).nonzero()

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
    bx = plt.figure().add_subplot(projection='3d')

    # x, y, z, tri = init_volume()
    x, y, z, tri = init_cube_OK()
    # x, y, z, tri = init_cube_KO()
    # x, y, z, tri = init_surface(size)

    ax.set_title("Inital")
    ax.plot_trisurf(x, y, z, triangles = tri, linewidth=0.2, antialiased=True, cmap = cm.magma)
    # Adding labels
    ax.set_xlabel('X-axis', fontweight ='bold')
    ax.set_ylabel('Y-axis', fontweight ='bold')
    ax.set_zlabel('Z-axis', fontweight ='bold')

    x, y, z, tri = fly_butterfly(x, y, z, tri, 3)

    bx.set_title("After Buttefly")
    bx.plot_trisurf(x, y, z, triangles = tri, linewidth=0.2, antialiased=True, cmap = cm.magma)
    # Adding labels
    bx.set_xlabel('X-axis', fontweight ='bold')
    bx.set_ylabel('Y-axis', fontweight ='bold')
    bx.set_zlabel('Z-axis', fontweight ='bold')

    plt.show()






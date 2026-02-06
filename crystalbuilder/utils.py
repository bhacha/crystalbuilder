from crystalbuilder import convert
from crystalbuilder import lattice
from crystalbuilder import vectors
from crystalbuilder import bilbao
import trimesh
import vedo
import numpy as np

def MonkhorstPack(size):
    """
    This is a direct copy of the Monkhorst-Pack k-space sampling method in ase (https://iopscience.iop.org/article/10.1088/1361-648X/aa680e)
    
    This way there's no need to import ase. 

    Parameters
    ----------
    size : ndarray
        number of points (kx, ky, kz) to sample reciprocal space. This should only be used in MPB, as it performs the necessary multiplication by the reciprocal lattice vectors 

    """
    if np.less_equal(size, 0).any():
        raise ValueError(f'Illegal size: {list(size)}')
    kpts = np.indices(size).transpose((1, 2, 3, 0)).reshape((-1, 3))
    return (kpts + 0.5) / size - 0.5



if __name__ == "__main__":
    vedo.settings.default_backend= 'vtk'

    cyl1 = vedo.Cylinder().triangulate().clean()
    cyl2 = vedo.Cylinder(pos = (.5, .5, 0), axis = (1, 1, 1), r=.5).triangulate().clean()
    # plt = vedo.Plotter()
    # plt += cyl1
    # plt += cyl2
    # plt.show()
    # objects = plt.get_meshes()
    # print(objects)
    tm1 = vedo.vedo2trimesh(cyl1)
    tm2 = vedo.vedo2trimesh(cyl2)
    merged = trimesh.boolean.boolean_manifold([tm1, tm2], operation='union')
    merged.show(viewer='gl')
    merged.export("testunion.stl")
    # print(tm1)
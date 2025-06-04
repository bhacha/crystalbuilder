from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("crystalbuilder")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["convert", "geometry", "lattice", "vectors","bilbao", "viewer", "lumpy_convert"]






"""
CrystalBuilder allows building triangle and cylinder based photonic crystal lattices for MEEP, MPB, and Tidy3D.

convert.py: methods for converting CrystalBuilder objects to MEEP/MPB/Tidy3D geometries

geometry.py: geometry classes. These are not actually "meshed" structures, but vertices/centers as required by the simulation program. e.g. a "triangle" object is defined by vertices in MEEP and Tidy3D so it is also defined that way in CrystalBuilder.geometry. There are additional methods in the geometry program that allow for defining with a center+size, but under the hood it still just calculates vertices.

lattice.py: the lattice class contains the basis vector information, and the methods for tiling the geometry objects. kekule modulation is also here.

vectors.py: methods for rotating/shifting/scaling vectors defined as numpy arrays or simple lists. This probably won't need to be called by users, but is integral for all the other packages.

bilbao.py: methods for retrieving space group information from Bilbao servers

viewer.py: methods for visualizing structures
"""
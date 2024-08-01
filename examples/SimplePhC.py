
from .. import vectors as vm
from crystalbuilder import geometry as geo
from crystalbuilder import lattice as lat
import numpy as np

# Triangular Unit Cell, Micron Units
amag = 1 # 1 micron magnitude for all lattice vectors

#triangular lattice vectors, plus a general z translation
a1 = [np.sqrt(3)/2, .5, 0 ]
a2 = [np.sqrt(3)/2, -.5, 0]
a3 = [0,0,1]

lattice = lat.Lattice(a1, a2, a3, magnitude=[amag, amag, amag])

### Triangle "atoms"

side_length = .3*amag
height = 1*amag
tri_index = 1.6 #refractive index

triangle_center = [0,0,0] #cartesian basis, NOT lattice basis

triangle1 = geo.eqTriangle(height = height, b=side_length, center=triangle_center) #create equilateral triangle

tiled_structures = lattice.tile_geogeometry(triangle1, 8, 8, 1)

for n in tiled_structures:
    print(n.vertices)

import crystalbuilder as cb
import crystalbuilder.vectors as vm
vm.debug= "off"
import crystalbuilder.lattice as lat
lat.debug = "off"
import crystalbuilder.geometry as geo
geo.debug = "off"
import numpy as np
import crystalbuilder.viewer as view
import vedo 

### Rhombus unit cell ###
### ALL UNITS IN MICRONS ###
a1 = [0, 1, 1]
a2 = [1, 0 ,1]
a3 = [1,1,0]
amag = np.sqrt(.5)
lat1 = lat.Lattice(a1, a2, a3, magnitude=[amag,amag,amag])

### Cylinders in unit cell ###
cylheight = 1*amag
rad = .01*amag
r1 = .15*amag
r2 = .15*amag
cyldr = 0


diamond = [
    ## First the corners
    [0,0,0], #0
    [0,0,1], #1
    [0,1,0], #2
    [1,0,0], #3
    [0,1,1], #4
    [1,0,1], #5
    [1,1,0], #6
    [1,1,1], #7

    ## The faces
    [0,1/2, 1/2], #8
    [1/2, 0, 1/2], #9
    [1/2, 1/2, 0], #10
    [1, 1/2, 1/2], #11
    [1/2, 1, 1/2], #12
    [1/2, 1/2, 1], #13

    ## Tetrahedral sites
    [1/4, 1/4, 1/4], #14
    [1/4, 3/4, 3/4], #15
    [3/4, 1/4, 3/4], #16
    [3/4, 3/4, 1/4] #17
]

### Geometry ###

d= .125*amag

cyl1_verts = (diamond[14], diamond[0])
cyl2_verts = (diamond[14], diamond[10])
cyl3_verts = (diamond[14], diamond[9])
cyl4_verts = (diamond[14], diamond[8])

cyl_1 = geo.Cylinder.from_vertices(cyl1_verts, radius=rad)
cyl_2 = geo.Cylinder.from_vertices(cyl2_verts, radius=rad)
cyl_3 = geo.Cylinder.from_vertices(cyl3_verts, radius=rad)
cyl_4 = geo.Cylinder.from_vertices(cyl4_verts, radius=rad)

cyllist = [cyl_1, cyl_2, cyl_3, cyl_4]

supercell = geo.SuperCell(cyllist)

tiledcells = lat1.tile_geogeometry(supercell,2, 2, 2, style='centered')

### Apply modulation ###
# for n in tiledcells:
#         lat1.modulate_cells(n, 
#                             vortex_radius=3, 
#                             winding_number=-1,
#                             max_modulation=.2*r1,
#         modulation_type='dual',
#         whole_cell=False)
        

test = view.visualize(tiledcells, plotter_style=1)
# test.get_meshes()

# k=0
# for obj in test.objects:
#     k+=1
#     string=f"diamond/object-{k}.obj"
#     vedo.write(obj, string)
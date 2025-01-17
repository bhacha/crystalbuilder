import crystalbuilder.geometry as cbg


#### Diamond Structure ####
"""
The diamond lattice of spheres is basically a tetrahedral unit cell inside of an FCC lattice

"""
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

"""
The nearest-neigbor connections have origins at the tetrahedral sites and connect to the faces and corners
"""
rad = .1
cyl1 = cbg.Cylinder.from_vertices(vertices=[diamond[14], diamond[0]], radius=rad)
cyl2 = cbg.Cylinder.from_vertices(vertices=[diamond[14], diamond[10]], radius=rad)
cyl3 = cbg.Cylinder.from_vertices(vertices=[diamond[14], diamond[8]], radius=rad)
cyl4 = cbg.Cylinder.from_vertices(vertices=[diamond[14], diamond[9]], radius=rad)

cyl5 = cbg.Cylinder.from_vertices(vertices=[diamond[15], diamond[4]], radius=rad)
cyl6 = cbg.Cylinder.from_vertices(vertices=[diamond[15], diamond[13]], radius=rad)
cyl7 = cbg.Cylinder.from_vertices(vertices=[diamond[15], diamond[12]], radius=rad)
cyl8 = cbg.Cylinder.from_vertices(vertices=[diamond[15], diamond[8]], radius=rad)

cyl9 = cbg.Cylinder.from_vertices(vertices=[diamond[16], diamond[5]], radius=rad)
cyl10 = cbg.Cylinder.from_vertices(vertices=[diamond[16], diamond[13]], radius=rad)
cyl11 = cbg.Cylinder.from_vertices(vertices=[diamond[16], diamond[9]], radius=rad)
cyl12 = cbg.Cylinder.from_vertices(vertices=[diamond[16], diamond[11]], radius=rad)

cyl13 = cbg.Cylinder.from_vertices(vertices=[diamond[17], diamond[7]], radius=rad)
cyl14 = cbg.Cylinder.from_vertices(vertices=[diamond[17], diamond[11]], radius=rad)
cyl15 = cbg.Cylinder.from_vertices(vertices=[diamond[17], diamond[12]], radius=rad)
cyl16 = cbg.Cylinder.from_vertices(vertices=[diamond[17], diamond[10]], radius=rad)

cyls = [cyl1, cyl2, cyl3, cyl4, cyl5, cyl6, cyl7, cyl8, cyl9, cyl10, cyl11, cyl12, cyl13, cyl14, cyl15, cyl16]


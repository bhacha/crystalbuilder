import crystalbuilder as cb
import crystalbuilder.vectors as vm
vm.debug= "off"
import crystalbuilder.lattice as lat
lat.debug = "off"
import crystalbuilder.geometry as geo
geo.debug = "off"
import numpy as np


### Rhombus unit cell ###
### ALL UNITS IN MICRONS ###
a1 = [np.sqrt(3)/2, .5, 0]
a2 = [np.sqrt(3)/2, -.5 ,0]
a3 = [0,0,1]
amag = 1
lat1 = lat.Lattice(a1, a2, a3, magnitude=[amag,amag,amag])

### Cylinders in unit cell ###
cylheight = 1.2
rad = .15*amag
r1 = .15*amag
r2 = .15*amag
cyldr = 0



### Geometry ###
d=(1/3)*amag
centc = (0,0,0)
centr = (0, d, 0)
centl = (0, -d, 0)
centbr =(-d/2*np.sqrt(3),  d/2, 0)
centbl =(-d/2*np.sqrt(3), -d/2, 0)
centtl =( d/2*np.sqrt(3),  -d/2, 0)
centtr =( d/2*np.sqrt(3),   d/2, 0)

cylh = cylheight

cyl_r = geo.Cylinder(radius=r2, center=centr, height=cylh) #Top in MEEP
cyl_l = geo.Cylinder(radius=r1, center=centl, height=cylh) # Bottom in MEEP
cyl_br = geo.Cylinder(radius=r1, center=centbr, height=cylh) #Top left in MEEP
cyl_bl = geo.Cylinder(radius=r2, center=centbl, height=cylh) #bottom left in meep
cyl_tl = geo.Cylinder(radius=r2, center=centtl, height=cylh) # bottom right in meep
cyl_tr = geo.Cylinder(radius=r1, center=centtr, height=cylh) #top right in mEEP


cyllist = [cyl_r, cyl_l, cyl_br, cyl_tl, cyl_tr, cyl_bl]

supercell = geo.SuperCell(cyllist)

tiledcells = lat1.tile_geogeometry(supercell,10, 10, 1, style='centered')

### Apply modulation ###
for n in tiledcells:
        lat1.modulate_cells(n, 
                            vortex_radius=3, 
                            winding_number=-1,
                            max_modulation=0,
        modulation_type='dual',
        whole_cell=False)
        

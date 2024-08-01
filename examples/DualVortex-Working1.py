import crystalbuilder as cb
import crystalbuilder.vectors as vm
vm.debug= "off"
import crystalbuilder.lattice as lat
lat.debug = "off"
import crystalbuilder.geometry as geo
geo.debug = "off"
import argparse

import crystalbuilder.meep_methods as mpm
# import tidy3d as td
import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import datetime 
import sys


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
mat1 = mp.Medium(epsilon=9)


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
        

### Convert to MEEP objects ###
newgeo = mpm.geo_to_meep(tiledcells, material=mat1)

### Add sources ###
fcen = 1/1.55
df = fcen*.3
nfreq = 100
dft_nfreq = 20

dftfreqs = np.linspace(fcen-(df/2), fcen+(df/2), dft_nfreq)

sources = [
        mp.Source(mp.GaussianSource(fcen, fwidth=df ),
                component = mp.Ez,
                center=mp.Vector3(0, 0, 0),
                size=mp.Vector3(1,1,.25)
                )
        ]

### Define simulation ###

#symmetry = [mp.Mirror(mp.Z)]
resolution = 20
dpml = 2 #depth of pml
pml_layers = [mp.PML(dpml)]
totcells = 10
outcells = totcells
sx, sy, sz = (dpml+totcells*amag*np.sqrt(3)/2, dpml+totcells*amag*1/2, 10)
cell = mp.Vector3(sx, sy, sz)
outputvolume = mp.Volume(mp.Vector3(), size=mp.Vector3(outcells*amag*np.sqrt(3)/2, outcells*amag*1/2, 3))
vidvolume = mp.Volume(mp.Vector3(), size=mp.Vector3(outcells*amag*np.sqrt(3)/2, outcells*amag*1/2, 3))
outputplane = mp.Volume(mp.Vector3(0,0,.5), size=mp.Vector3(outcells*amag*np.sqrt(3)/2, outcells*amag*1/2, 0))
sideplane = mp.Volume(mp.Vector3(), size=mp.Vector3(outcells*amag*np.sqrt(3)/2, 0, 10))

sim = mp.Simulation(
                cell_size=cell,
                boundary_layers=pml_layers,
                geometry=newgeo,
                resolution=resolution,
                sources=sources,
                filename_prefix='testfilename'
                
)

sim.plot2D(output_plane=outputplane, eps_parameters={'cmap':'binary_r'})
plt.show()
sim.plot2D(output_plane=sideplane, eps_parameters={'cmap':'binary_r'})
plt.show()


flux = sim.add_flux(
        fcen, df, nfreq, mp.FluxRegion(center=mp.Vector3(0,0,4), size=mp.Vector3(outcells*amag*np.sqrt(3)/2, outcells*amag*1/2, 0))
)

dft_fields = sim.add_dft_fields([mp.Ez],
                                dftfreqs,
                                center=mp.Vector3(),
                                where=outputplane,
                                yee_grid=True)

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ez", mp.at_every(5, mp.output_efield_z)),
        until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez, mp.Vector3(0,0,cylheight), 1e-4))

sim.output_dft(dft_fields,'fieldfile')

t_flux = mp.get_fluxes(flux)
flux_freqs = mp.get_flux_freqs(flux)



fluxfile = open("fluxfile.txt", 'a')
for n in range(len(t_flux)):
        fluxfile.write(f'{t_flux[n]}, {flux_freqs[n]} \n')

fluxfile.close()

#First normalization method (no structure)
blanksim = mp.Simulation(
                cell_size=cell,
                boundary_layers=pml_layers,
                geometry=None,
                resolution=resolution,
                sources=sources,
                filename_prefix='testfilename'
                
)

# blanksim.plot2D(output_plane=outputplane, eps_parameters={'cmap':'binary_r'})
# plt.show()
# blanksim.plot2D(output_plane=sideplane, eps_parameters={'cmap':'binary_r'})
# plt.show()

bflux = blanksim.add_flux(
        fcen, df, nfreq, mp.FluxRegion(center=mp.Vector3(0,0,4), size=mp.Vector3(outcells*amag*np.sqrt(3)/2, outcells*amag*1/2, 0))
)

blanksim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Hz, mp.Vector3(0,0,0), 1e-3))

bt_flux = mp.get_fluxes(bflux)
bflux_freqs = mp.get_flux_freqs(bflux)

### Second Normalization Method (just slab)
slab = [mp.Block(mp.Vector3(mp.inf,mp.inf,cylh),
                     center=mp.Vector3(),
                     material=mat1)]


slabsim = mp.Simulation(
                cell_size=cell,
                boundary_layers=pml_layers,
                geometry=slab,
                resolution=resolution,
                sources=sources,
                
)


slabflux = slabsim.add_flux(
        fcen, df, nfreq, mp.FluxRegion(center=mp.Vector3(0,0,4), size=mp.Vector3(outcells*amag*np.sqrt(3)/2, outcells*amag*1/2, 0))
)


slabsim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Hz, mp.Vector3(0,0,0), 1e-3))

slabt_flux = mp.get_fluxes(slabflux)

print(slabt_flux)

#plt.plot(flux_freqs, t_flux)
#%%

fluxdiv1 = np.asarray(t_flux)/np.asarray(bt_flux)
fluxdiv2 = np.asarray(t_flux)/np.asarray(slabt_flux)

plt.figure()
plt.plot(flux_freqs, np.asarray(t_flux)**2)
plt.title("Absolute Flux in Positive Z")

plt.figure()
plt.plot(flux_freqs, fluxdiv1)
plt.title("Relative Flux in Positive Z, Normalized to Vacuum Sim")

plt.figure()
plt.plot(flux_freqs, fluxdiv2)
plt.title("Relative Flux in Positive Z, Normalized to Slab Sim")

# %%

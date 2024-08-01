import numpy as np
import matplotlib.pyplot as plt
import h5py as hpy

fil = hpy.File('fieldfile.h5')
print(fil.keys())
fcen = 1/1.55
df = fcen*.3
nfreq = 100
dft_nfreq = 20

dftfreqs = np.linspace(fcen-(df/2), fcen+(df/2), dft_nfreq)
k = 0
for n in fil.keys():
    
    if '.r' in n:
        dset = fil[n]
        plt.figure()
        nfreq=dftfreqs[k]
        plt.title(f"freq={nfreq}")
        plt.contourf(dset, vmin=-1e-3, vmax=3e-2)
        
    k = k+1

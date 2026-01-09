import numpy as np
from matplotlib import pyplot as plt
import meep as mp
import meep.mpb as mpb
import logging as log


def make_kgrid(kx_range:list[float], ky_range:list[float], n_kx_points:int, n_ky_points:int):
    
    kxmin = min(kx_range)
    kxmax = max(kx_range)
    kymin = min(ky_range)
    kymax = max(ky_range)
    
    kx_arr = np.linspace(kxmin, kxmax, n_kx_points)
    ky_arr = np.linspace(kymin, kymax, n_ky_points)
    kx, ky= np.meshgrid(kx_arr, ky_arr, indexing='xy')
    k_arr = np.stack([kx, ky]).T.reshape(-1, 2)
    vector_list = []
    for k in k_arr:
        vect = create_vector3(k)
        vector_list.append(vect)
        
    return vector_list

def create_vector3(kpoint, order='xyz'):
    if len(kpoint) >= 3:
        vect = mp.Vector3(kpoint[0], kpoint[1], kpoint[2])
    elif len(kpoint) == 2:
        vect = mp.Vector3(kpoint[0], kpoint[1], 0)
    else:
        vect = mp.Vector3(kpoint[0], 0, 0)
    return vect


combined_point_list = []
def _combine_output(ms, which_band):
    current_k = ms.current_k
    freq = ms.freqs[which_band-1]
    combo_point = np.array([current_k[0], current_k[1], current_k[2], freq])
    combined_point_list.append(combo_point)
    return combined_point_list

def search_wavelength(wavelength, lattice_constant, tolerance = 10):
    """
    Given a target `wavelength` and size of the structure (`lattice constant`), identify the points in `points_list` that with frequencies within the `tolerance` range  
    """
    points_list = np.asarray(combined_point_list)

    a_fab = lattice_constant
    wl_targ = wavelength
    freq_target = a_fab/wl_targ

    wl_range = np.array([wavelength+tolerance, wavelength-tolerance]) 
    freq_tol = np.diff(a_fab/wl_range)/freq_target

    print(freq_target, freq_tol)
    selected_points = points_list[np.where(np.isclose(points_list[:, 3], freq_target, freq_tol, atol=0.0001))]
    return selected_points





"""
The ModeSolver object collects all the frequencies that have been solved for, and ms.all_freqs returns an array of size (n_kpoints, n_bands)

It might be better to grab the k vectors and frequencies with a custom run function. This can use current_k and freqs to build an array.

"""






if __name__ == "__main__":

    k_points = make_kgrid([-.4, .4], [-.4, .4], 20,20)
    

    geometry = [mp.Cylinder(0.37, material=mp.Medium(epsilon=1))]
    geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1, 0))

    resolution = 16  # pixels/um


    num_bands = 6
    ms = mpb.ModeSolver(
        k_points=k_points,
        geometry_lattice = geometry_lattice,
        geometry         = geometry,
        resolution       = resolution,
        num_bands        = num_bands,
        default_material=mp.Medium(epsilon=4.3)
    )

    ms.run_te(_combine_output)

    selected_point = search_wavelength(wavelength=670, lattice_constant=490, tolerance=10)


    plt.scatter(selected_point[:, 0], selected_point[:, 1])



    # #     ### Plotting Band Structure ###
    crysfreqs = ms.all_freqs
    plt.figure()
    
    x = range(len(crysfreqs))
    plt.plot(crysfreqs)
    
    plt.figure()
    md = mpb.MPBData(rectify=True, periods=1, resolution=64)
    eps = ms.get_epsilon()
    converted_eps = md.convert(eps)
    layer_slice = 22
    plt.imshow(converted_eps, interpolation='spline36', cmap='binary_r')
    plt.axis('off')
    plt.show()
    
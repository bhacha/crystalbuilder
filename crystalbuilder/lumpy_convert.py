import numpy as np
from crystalbuilder import lattice as lat
from crystalbuilder import geometry as geo

try:
    import lumpy.simobjects as so
except ModuleNotFoundError:
    print("Error: Lumpy and/or the Lumerical API were not found.")


debug = 'trace'   #trace = 3, debug = 2, info = 1, none = 0

def debug_msg(string, level):
    debug_levels = {'trace':3, 'debug':2, 'info': 1, 'none':0}
    req_deb = debug_levels[debug]
    if level <= req_deb:
        print(string)
        
def flatten(list):
    """ Some of these methods can accidentally create nested lists, so this function can be used in try statements to correct those """
    try:
        flat_list = [item for sublist in list for item in sublist]
    except:
        flat_list = list
    return flat_list

def convert_cylinder(Cylinder, material='dielectric', index=1.5):    
    axis = Cylinder.axis
    lumCyl = so.Cylinder(radius=Cylinder.radius, height=Cylinder.height, center=tuple(flatten(Cylinder.center)), material=material, index=index, orientation=axis)
    debug_msg(lumCyl.out(), 3)
    return lumCyl

def convert_prism(Prism, material='dielectric', index=1.5):
    verts = Prism.vertices[:, 0:2]
    lumPrism = so.Prism(vertices=verts, z_span=Prism.height, center=tuple(flatten(Prism.center)), material=material, index=index)
    return lumPrism
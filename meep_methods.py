import numpy as np
from matplotlib import pyplot as plt
from . import vectors as vm
from . import lattice as lat
from . import geometry as geo
import meep as mp

debug = "off"

if vm.debug == "on":
    debug = "on"
else:
    debug = 'off'


def unpack_supercell(supercell):
    structures = supercell.structures
    return structures

def _geo_to_meep(geometry_object, material):
    geom_list = []
    try:
        for m in geometry_object:
            if isinstance(m, geo.SuperCell):
                if debug=="on": print("This is running the iterable Supercell")
                innerlist = _geo_to_meep(m, material)
                geom_list.append(innerlist)

            elif isinstance(m, geo.Cylinder):
                if debug=="on": print("This is running the iterable cylinder")
                item = mp.Cylinder(radius=m.radius, axis= m.axis, height=m.height, center=flatten(m.center), material=material)
                geom_list.append(item)

    except TypeError:
            if isinstance(geometry_object, geo.SuperCell):
                if debug=="on": print("This is running the single Supercell")
                structs = unpack_supercell(geometry_object)
                m = structs
                newlist = _geo_to_meep(m, material)
                geom_list.append(newlist)

            elif isinstance(geometry_object, geo.Cylinder):
                m = geometry_object
                if debug=="on": print("This is running the single cylinder")
                geom_list.append(mp.Cylinder(radius=m.radius, axis= m.axis, height=m.height, center=m.center, material=material))


    return geom_list

def geo_to_meep(geometry_object, material):
    geom_list = _geo_to_meep(geometry_object, material)
    newlist = flatten(geom_list)
    newlist = flatten(newlist)
    return newlist

def flatten(list):
    try:
        flat_list = [item for sublist in list for item in sublist]
    except:
        flat_list = list
    return flat_list


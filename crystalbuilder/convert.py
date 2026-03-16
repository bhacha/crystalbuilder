import numpy as np
from crystalbuilder.conversions.t3d import geo_to_tidy3d
from crystalbuilder import lattice as lat
from crystalbuilder import geometry as geo
from crystalbuilder.conversions import lumc as lc



"""
The real conversion methods are found in crystalbuilder/conversions/

This module provides an easy access to all of them while also letting you use the lumerical and tidy3d conversions without needing MEEP/MPB ones (e.g. if you're on windows)

"""

#Check if MEEP/MPB is available and load the conversion functions
try:
    from crystalbuilder.conversions.meep import *
except Exception as e:
    print(e)
    from crystalbuilder.conversions.meep import unpack_supercell



#Check if Lumerical is available and load the conversion functions    
try:
    import lumpy.simobjects as so
except ModuleNotFoundError:
    pass

debug = 'on'

def _geo_to_lumerical(geometry_object, material):
    """
    Converts Geometry object to list of lumerical objects

    ## IN PROGRESS ##

    """

    #get index from meep material, but treat it as a dielectric constant otherwise
    try:
        if isinstance(material, mp.Medium): #type:ignore
            index = np.sqrt(material.epsilon_diag[0])
        else:
            index = material
    except NameError:
        index = material
        
    geom_list = []
    try:
        for m in geometry_object:
            if isinstance(m, geo.SuperCell):
                if debug=="on": print("This is running the iterable Supercell")
                innerlist = _geo_to_lumerical(m, material)
                geom_list.append(innerlist)

            elif isinstance(m, geo.Cylinder):
                if debug=="on": print("This is running the iterable cylinder")
                lmgeom = lc.convert_cylinder(m, material='dielectric', index=index)
                geom_list.append(lmgeom)

            elif isinstance(m, geo.Triangle):
                if debug=="on": print("This is running the iterable Triangle")
                lmgeom = lc.convert_prism(m, material='dielectric', index=index)
                geom_list.append(lmgeom)

    except TypeError:
            if isinstance(geometry_object, geo.SuperCell):
                if debug=="on": print("This is running the single Supercell")
                structs = unpack_supercell(geometry_object)
                m = structs
                newlist = _geo_to_lumerical(m, material)
                geom_list.append(newlist)

            elif isinstance(geometry_object, geo.Cylinder):
                m = geometry_object
                if debug=="on": print("This is creating a single cylinder named")
                lmgeom = lmgeom = lc.convert_cylinder(m, material='dielectric', index=index)
                geom_list.append(lmgeom)

            elif isinstance(geometry_object, geo.Triangle):
                m = geometry_object
                if debug=="on": print("This is running the single Triangle")
                lmgeom = lc.convert_prism(m, material='dielectric', index=index)
                geom_list.append(lmgeom)



    return geom_list

if __name__ == '__main__':
    """testing code"""

    # mat1 = mp.Medium(epsilon=4)
    # geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1),
    #                     basis1=mp.Vector3(np.sqrt(3) / 2, 0.5),
    #                     basis2=mp.Vector3(0,0.5))

    # tri = geo.eqTriangle(1, .5)
    # print(tri.vertices.shape)
    # print(type(tri))
    
    # newgeo = _geo_to_lumerical(tri, mat1)

    # print(newgeo[0].out())

    
    cylinder = geo.Cylinder.from_vertices([[0,0,0], [1,1,1]], radius=.2)
    cylinder2 = geo.Cylinder(center=[1,1,0], radius=.1, height=3, axis=2)
    newgeo = geo_to_tidy3d([cylinder, cylinder2], material=3)
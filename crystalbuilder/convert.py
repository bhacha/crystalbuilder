import numpy as np
from crystalbuilder import lattice as lat
from crystalbuilder import geometry as geo
from crystalbuilder import lumpy_convert as lc
import platform
if platform.system() == 'Windows':
    pass
else:
    import meep as mp

#import tidy3d as td
try:
    import lumpy.simobjects as so
except ModuleNotFoundError:
    pass
debug = "off"

def vectorize(list):
    """Converts list of x,y,z coordinates to mp.Vector3 object

    This simply assigns the first 3 indices to 'x','y','z' and returns the mp.Vector3('x','y','z'). 
    Thus it will also work for any index-able data format (e.g. numpy arrays and existing mp.Vector3 objects)

    Parameters
    ----------
    list : ArrayLike
        an ArrayLike object of length 3 (anything beyond will be ignored)

    Returns
    -------
    mp.Vector3()
        mp.Vector3 object mp.Vector3(x,y,z)

    """
    x = list[0]
    y = list[1]
    z = list[2]
    return mp.Vector3(x,y,z)

def unpack_supercell(supercell):
    """Turns supercell into a list of geometry objects

    Parameters
    ----------
    supercell : gm.SuperCell()
        A SuperCell object from geometry.py

    Returns
    -------
    [structures]: list
        list of the geometry objects in SuperCell

    """

    structures = supercell.structures
    return structures

def flatten(list):
    """ Some of these methods can accidentally create nested lists, so this function can be used in try statements to correct those """
    try:
        flat_list = [item for sublist in list for item in sublist]
    except:
        flat_list = list
    return flat_list

def _geo_to_meep(geometry_object, material, ismpb = False, **kwargs):
    """ Lower-level function to convert Geometries into MEEP objects. It's recommended to call the geo_to_meep function instead.

    Parameters
    -----------
    geometry_object : list or Geometry
        an object or list of objects from geometry.py

    material : mp.Material()
        MEEP material for the converted object

    ismpb : bool
        MPB is a MEEP submodule that works for photonic crystals. The coordinate space is different than conventional MEEP. This arg determines if the resulting objects will use MPB coordinates or the MEEP ones (default)

    **kwargs : string
        lattice: mpb.lattice()
            lattice for building MPB geometry, only necessary if mpb_mode is True. This is handled automatically by the higher level geo_to_mpb function
              
        
    Returns
    -------
    [geom_list] : list
        list of MEEP objects
    
    """

    mpb_mode = ismpb
    #print("MPB Mode is ", str(mpb_mode))
    geom_list = []
    if mpb_mode == True:
        geo_lattice = kwargs.get("lattice", None)
    

    try:
        for m in geometry_object:
            if isinstance(m, geo.SuperCell):
                if debug=="on": print("This is running the iterable Supercell")
                if ismpb == True: 
                    innerlist = _geo_to_meep(m, material, ismpb=mpb_mode, lattice=geo_lattice)
                    geom_list.append(innerlist)
                else:
                    innerlist = _geo_to_meep(m, material, ismpb=mpb_mode)
                    geom_list.append(innerlist)

            elif isinstance(m, geo.Cylinder):
                if debug=="on": print("This is running the iterable cylinder")
                
                if ismpb == True: 
                    k = vectorize(m.center)
                    newcent = mp.cartesian_to_lattice(k, geo_lattice)
                else:
                    newcent = vectorize(m.center)

                item = mp.Cylinder(radius=m.radius, axis= m.axis, height=m.height, center=newcent, material=material)
                geom_list.append(item)

            elif isinstance(m, geo.Triangle):
                if debug=="on": print("This is running the iterable triangle")
                
                newverts = []
                for k in m.vertlist:
                    k = vectorize(k)
                    if mpb_mode == True:
                        newverts.append(mp.cartesian_to_lattice(k, geo_lattice))
                    elif mpb_mode == False:
                        newverts.append(k)

                item = mp.Prism(vertices = newverts, axis = vectorize(m.axis), height = m.height, material=material)
                geom_list.append(item)

            elif isinstance(m, geo.Sphere):
                if ismpb == True: 
                    k = vectorize(m.center)
                    newcent = mp.cartesian_to_lattice(k, geo_lattice)
                else:
                    newcent = vectorize(m.center)

                item = mp.Sphere(radius=m.radius,center=newcent, material=material)
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
                if ismpb == True: 
                    k = vectorize(m.center)
                    newcent = mp.cartesian_to_lattice(k, geo_lattice)
                else:
                    newcent = vectorize(m.center)
                geom_list.append(mp.Cylinder(radius=m.radius, axis= m.axis, height=m.height, center=newcent, material=material))

            elif isinstance(geometry_object, geo.Triangle):
                if debug=="on": print("This is running the single triangle")
                m = geometry_object
                if ismpb == True:
                    newverts = []
                    for k in m.verttuple:
                        k = vectorize(k)
                        newverts.append(mp.cartesian_to_lattice(k, geo_lattice))
                else:
                    newverts = vectorize(m.verttuple)
                geom_list.append(mp.Prism(vertices = newverts, axis = vectorize(m.axis), height = m.height, material=material))

            elif isinstance(geometry_object, geo.Sphere):
                m = geometry_object
                if ismpb == True: 
                    k = vectorize(m.center)
                    newcent = mp.cartesian_to_lattice(k, geo_lattice)
                else:
                    newcent = vectorize(m.center)

                item = mp.Cylinder(radius=m.radius, center=newcent, material=material)
                geom_list.append(item)



    return geom_list

def geo_to_meep(geometry_object, material):
    """Converts CrystalBuilder geometry object(s) to the corresponding MEEP object(s) with defined material.

    This is a higher level wrapper of the _geo_to_meep function, which I have yet to document. 
    This simplifies the calling, as it only takes two arguments. 

    Parameters
    ----------
    geometry_object : list or Geometry
        an object or list of objects geometry.py
    
    material : mp.Material()
        MEEP material 

    Returns
    -------
    [meep_list]: list
        list of MEEP objects

    """
    geom_list = _geo_to_meep(geometry_object, material)
    newlist = flatten(geom_list)
    meep_list = flatten(newlist)
    return meep_list

def geo_to_mpb(geometry_object, material, lattice):
    """Converts CrystalBuilder geometry object(s) to the corresponding MPB object(s) with defined material.

    This is a higher level wrapper of the _geo_to_meep function, which I have yet to document. 
    MPB defines geometry on an arbitrary basis determined by the simulation's lattice. This requires an extra parameter, 'lattice'.

    Parameters
    ----------
    geometry_object : Geometry or list of Geometry
        an object or list of objects
    material : mp.Material()
        MPB material
    lattice : mpb.lattice()
        lattice for MPB simulation, usually assigned to geometry_lattice


    Returns
    -------
    [mpb_list]: list
        list of mpb objects

    """


    geom_list = _geo_to_meep(geometry_object, material, ismpb=True, lattice=lattice)
    newlist = flatten(geom_list)
    mpb_list = flatten(newlist)
    return mpb_list

def _geo_to_tidy3d(geometry_object, material, **kwargs):
    """Converts geometry object (or supercell) to the Tidy3D equivalent. Note that Tidy3D values always include units (microns by default).

    Tidy3D geometries are combined with a specified medium to create a Tidy3D structure object, which can be given a unique name. For now, the naming will be systematic. This might be changed in the future via kwargs.

    The material assignment will occur after all of the geometries have been made. This means a td.GeometryGroup object will be created and made into a structure.
     """

    geom_list = []
    try:
        for m in geometry_object:
            if isinstance(m, geo.SuperCell):
                if debug=="on": print("This is running the iterable Supercell")
                innerlist = _geo_to_tidy3d(m, material)
                geom_list.append(innerlist)

            elif isinstance(m, geo.Cylinder):
                if debug=="on": print("This is running the iterable cylinder")
                tdgeom = td.Cylinder(radius=m.radius, axis= 2, length=m.height, center=tuple(flatten(m.center)))
                geom_list.append(tdgeom)

    except TypeError:
            if isinstance(geometry_object, geo.SuperCell):
                if debug=="on": print("This is running the single Supercell")
                structs = unpack_supercell(geometry_object)
                m = structs
                newlist = _geo_to_tidy3d(m, material)
                geom_list.append(newlist)

            elif isinstance(geometry_object, geo.Cylinder):
                m = geometry_object
                if debug=="on": print("This is creating a single cylinder named")
                tdgeom = td.Cylinder(radius=m.radius, axis= 2, length=m.height, center=tuple(flatten(m.center)))
                geom_list.append(tdgeom)


    return geom_list

def geo_to_tidy3d(geometry_object, material):
    """Converts CrystalBuilder geometry object(s) to the corresponding Tidy3D object(s) with defined medium. 
    
    
    `material` can be either a td.Medium() object or a float corresponding to the refractive index of the desired Medium.

    This is a higher level wrapper of the _geo_to_tidy3d function, which I have yet to document

    Parameters
    ------------
    geometry_object : Geometry or list of Geometry
        an object or list of objects
    material : td.Medium() or float
        Tidy3D Medium or the refractive index that will be assigned to the material.



    Returns
    ------------
    td.Structure()
        a Tidy3D structure group with defined Medium

    """

    geometry_list = flatten(flatten(_geo_to_tidy3d(geometry_object, material)))
    print(geometry_list)
    geometry_group = td.GeometryGroup(geometries = tuple(geometry_list))

    if isinstance(material, td.Medium):
        medium = material
    else:
        medium = td.Medium(permittivity = material**2, name="DielectricMaterial")
    return td.Structure(geometry=geometry_group, medium=medium, name="Structure Group")


def _geo_to_lumerical(geometry_object, material):
    """
    Converts Geometry object to list of lumerical objects

    ## IN PROGRESS ##

    """

    #get index from meep material, but treat it as a dielectric constant otherwise
    try:
        if isinstance(material, mp.Medium):
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

def to_geo_lattice(mpblattice):
    """converts mpb's `Lattice` to the CrystalBuilder Lattice

    Parameters
    ----------
    mpblattice : mp.Lattice()
        mpb/MEEP lattice object


    Returns
    -------
    lat.Lattice()
        CrystalBuilder lattice object
        

    """

    if isinstance(mpblattice, mp.Lattice):
        magnitude = np.asarray(mpblattice.size)
        basis1 = np.asarray(mpblattice.basis1)
        basis2 = np.asarray(mpblattice.basis2)
        basis3 = np.asarray(mpblattice.basis3)
        lattice = lat.Lattice(a1=basis1, a2=basis2, a3=basis3, magnitude=magnitude)
        return lattice 
    else:
        print("Error: Please pass a MEEP lattice object as the argument")

def to_mpb_lattice(geolattice):
    """converts crystalbuilder Lattice to the mpb lattice

    Parameters
    ----------
    lat.Lattice() 
        CrystalBuilder lattice object
        

    Returns
    -------
    mpblattice : mp.Lattice()
        mpb/MEEP lattice object
    """

    if isinstance(geolattice, lat.Lattice):
        magnitude = np.asarray(geolattice.magnitude)
        basis1 = np.asarray(geolattice.a1)
        basis2 = np.asarray(geolattice.a2)
        basis3 = np.asarray(geolattice.a3)
        lattice = mp.Lattice(size = magnitude, basis1 = basis1, basis2 = basis2, basis3=basis3)
        return lattice 
    else:
        print("Error: Please pass a crystalbuilder lattice object as the argument")

if __name__ == '__main__':
    """testing code"""

    mat1 = mp.Medium(epsilon=4)
    geometry_lattice = mp.Lattice(size=mp.Vector3(1, 1),
                        basis1=mp.Vector3(np.sqrt(3) / 2, 0.5),
                        basis2=mp.Vector3(0,0.5))

    tri = geo.eqTriangle(1, .5)
    print(tri.vertices.shape)
    print(type(tri))
    
    newgeo = _geo_to_lumerical(tri, mat1)

    print(newgeo[0].out())

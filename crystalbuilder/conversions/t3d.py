
import numpy as np
try:
    from tidy3d import Transformed, Structure, GeometryGroup, Cylinder, Medium, Simulation, PointDipole, C_0, GridSpec, GaussianPulse
except ModuleNotFoundError:
    pass

from crystalbuilder import geometry as geo
debug = "off"

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
        if isinstance(list, list):
            flat_list = [item for sublist in list for item in sublist]
    except:
        flat_list = list
    return flat_list

def rotate_to(orientation, v1 = [0,0,1]):
    """
    Create a quaternion to rotate the original vector to the specified `orientation`. By default, use a Z unit vector
    """

    orientation = np.asarray(orientation)/np.linalg.norm(orientation)
    v1 = np.asarray(v1)/np.linalg.norm(v1)
    eyemat = np.identity(3)
    
    
    rot_axis_unnorm = np.cross(orientation, v1)
    s_angle = np.linalg.norm(rot_axis_unnorm)
    rot_axis = rot_axis_unnorm/s_angle
    c_angle = np.dot(orientation, v1)

    # print(s_angle)
    # print(c_angle)

    skew_mat = np.array(
        ((0, -rot_axis[2], rot_axis[1]), 
        (rot_axis[2], 0, -rot_axis[0]), 
        (-rot_axis[1], rot_axis[0], 0))
    )

    rot_mat = eyemat + (s_angle * skew_mat) + ((1-c_angle)*(skew_mat@skew_mat))
    print(f"{(s_angle * skew_mat)}\n")

    print(f"{(1-c_angle)*(skew_mat@skew_mat)}\n")

    print(f"Determinant: {np.linalg.det(rot_mat)}")
    #Tidy3D takes an affine transformation matrix, but we won't use this method for doing translations. So we're going to hard-code this.

    rot_mat = np.pad(rot_mat, (0,1))
    rot_mat[3,3] = 1
    return rot_mat

def _convert_cyl(geometry_object, material):
    m = geometry_object
    rot_mat = rotate_to(m.axis)
    tdgeom = Transformed(geometry = Cylinder(radius=m.radius, axis= 1, length=m.height, center=tuple(flatten(m.center))), transform=rot_mat)
    return tdgeom

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
                tdgeom = _convert_cyl(m, material)
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
                tdgeom = _convert_cyl(m, material)
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
    geometry_list_raw = _geo_to_tidy3d(geometry_object, material)
    geometry_list =geometry_list_raw
    geometry_group = GeometryGroup(geometries = tuple(geometry_list))
    print(geometry_group)
    if isinstance(material, Medium):
        medium = material
    else:
        medium = Medium(permittivity = material**2, name="DielectricMaterial")

    return Structure(geometry=geometry_group, medium=medium, name="Structure Group")

if __name__ == '__main__':
    """testing code"""

    cylinder = geo.Cylinder.from_vertices([[0,0,0], [1,0,0]], radius=.1)
    cylinder2 = geo.Cylinder.from_vertices([[0,0,0], [1,1,1]], radius=.2)
    newgeo = geo_to_tidy3d([cylinder, cylinder2], material=3)

    def view_structures(geometry):
        # create source
        lda0 = 0.75  # wavelength of interest (length scales are micrometers in Tidy3D)
        freq0 = C_0 / lda0  # frequency of interest
        source = PointDipole(
            center=(-1.5, 0, 0),  # position of the dipole
            source_time=GaussianPulse(freq0=freq0, fwidth=freq0 / 10.0),  # time profile of the source
            polarization="Ey",  # polarization of the dipole
    )

        sim = Simulation(
            size=(5, 5, 5),  # simulation domain size
            grid_spec=GridSpec.auto(
                min_steps_per_wvl=25
            ),  # automatic nonuniform FDTD grid with 25 grids per wavelength in the material
            structures=[geometry],
            sources=[source],
            run_time=3e-13,  # physical simulation time in second
        )
        sim.plot_3d()

    view_structures(newgeo)
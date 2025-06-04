#Geometry File
import numpy as np
from matplotlib import pyplot as plt
from crystalbuilder import vectors as vm
import copy
import scipy.spatial as scs

debug = 'off'

class Structure():
    def __init__(
            self,
            **kwargs
    ):
        pass

    

class SuperCell():
    """
    Takes other geometry objects and groups them into one supercell object (akin to list) that can be passed to the methods in lattice.py
    Advantage of this over simple list is the addition of rotation and translation options to alter the supercell.

     ...

    Attributes
    ----------
    geometries : geo.object or list of geo_objects
        geometries in supercell
    
    center : list or ArrayLike
        center of supercell

    radius : float or list of float
        'radius' or size of all structures

    

    Methods
    -------
    rotatecell(deg)
        create 360/deg total copies of the unit cell in the supercell

    add_structure(structure)
        adds a structure to the supercell

    """
    def __init__(self, 
                 geometries,
                 point='center',
                 shift = False,
                 **kwargs
                 ):
        """
        Parameters
        -----------
        geometries (list): geo.geometry objects

        
        Keyword Arguments
        ------------------
        'center'    : ArrayLike, default: None unless rotation or translation is defined then (0,0,0)
            defines center for operations. 

        'rotation'  : int
            specifies copy+rotation of geometries in degrees. Rotates about center. Creates 360/value number of repetitions.

        'translation': 
            specifies copy+translation by vector. Relative to center.

        """
    
        self.point_style = point
        self.structures = []
        self._instructures = geometries
        self.input_center = kwargs.get('center', None)
        self.rotation = kwargs.get('rotation', None)
        self.translation = kwargs.get('translation', None)
        self.unit = kwargs.get('unit', 'degrees')
        self.shiftcell = shift
        self.default_center = kwargs.get('relative_center', [0,0,0])

        if self.input_center == None:
            self.cellcenter = self.default_center
        else:
            self.cellcenter = self.input_center

        if self.rotation != None:
            if debug == "on": print("geo: center is ", self.cellcenter)
            deg = np.degrees(vm.angle_check(self.rotation, self.unit))
            self.rotatecell(deg)
        else:
            self.structures = self._instructures

        if self.shiftcell == True:
            self.center = self.cellcenter

    def __iter__(self):
        return iter(self.structures)
                   
    def rotatecell(self, deg, copy=True):
            """
            Rotation method for rotating a unit cell by deg around the supercell center. Unfortunately it only copies the cell for the moment, giving 360/deg numbers of the cell.

            Parameters
            ------------
            deg : float
                desired angle of rotation, in degrees

            """
            if copy == True:
                print("Angle is " , deg, " degrees")
                numrot = round(360/deg)
                for m in self._instructures:
                    for n in range(0, numrot):
                        if self.point_style == 'center':
                            newpoints = vm.rotate([m.center], theta=(n*deg), relative_point=self.cellcenter, unit='degrees')
                            #print("Newpoints: ", newpoints)
                            self.structures.append(m.copy(center=newpoints))
                        elif self.point_style == 'vertices':    
                            newpoints = vm.rotate(m.vertices, theta=(n*deg), relative_point=self.cellcenter, unit='degrees')
                            #print("Newpoints: ", newpoints)
                            self.structures.append(m.copy(vertices=newpoints))
            else:
                print("Sorry, this method is only made to rotate and make new copies. Hopefully this will be fixed soon.")

    def translatecell(self, shiftvec):
        """
        Translate the entire unit cell by some vector

        Parameters
        ------------
        shiftvec : list
            vector with length/direction determining the shift

        Returns
        -------
        None

        """
        if debug == "on": print("geo: translating cell by ", shiftvec, "\n")
        for n in self.structures:
            if debug == "on":print("geo: the structure's original center is ", n.ogcenter)
            newcenter = np.asarray(n.original_center) + shiftvec
            if debug == "on":print("geo: the structure's new center is ", newcenter)
            n.center = newcenter

    def _shift_center(self, oldcenter, newcenter):
        """ Shift cell to specified center. This creates a shift vector and passes it to translatecell
        
        Parameters
        -----------
        oldcenter: list
            current center point of supercell
        newcenter: list
            desired center point of supercell
        
        """
        shiftvec = vm.get_shift_vector(oldcenter, newcenter)
        self.translatecell(shiftvec)

    def copy(self, **kwargs):
        """
        Makes a deep copy of the supercell.
        
        Create a supercell, then call this method to update and copy the parameters.
        
        """
        memodict = {}
        center = kwargs.get('center', self.cellcenter)
        geos = kwargs.get('structures', self.structures)

        newcopy = SuperCell(geometries=geos, center=center)
        newcopy.__dict__.update(self.__dict__)

        newcopy.structures=copy.deepcopy(geos, memodict)
        newcopy.center = copy.deepcopy(center, memodict)

        
        return newcopy
    
    def identify_structures(self):
        """
        Print the types and positions of all the structures in the cell.

        Parameters
        ----------
        None

        Returns
        -------
        stdout

        """
        k = 0
        for n in self.structures:
            k = k+1
            print("Object %s is %s, with center at %s" % (k, type(n), n.center))

    def add_structure(self, structure):
        self.structures.append(structure)

    @property
    def center(self):
        cent = self.cellcenter
        return cent
    
    @center.setter
    def center(self, newcent):
        self.cellcenter = newcent
        if debug=='on': print("geo: newcenter ", newcent)
        self._shift_center(self.default_center, newcent)
        
    @property
    def radius(self):
        rads = []
        for n in self.structures:
            rads.append(n.radius)
        return rads
    
    @radius.setter
    def radius(self, newrad):
        for n in self.structures:
            n.radius= newrad
       
class CylinderVortexCell(SuperCell):

    def __init__(
                self,
                lattice,
                center,
                radius_1,
                R_max,
                height = 10,
                vort_center = [0,0,0],
                vort_radius = 1,
                winding_number=1,
                radius_2 = None,
                scale = 0,
                **kwargs
        ):
            """
            Constructs a Dirac Vortex SuperCell based on a hexagonal cell of cylinders (also called Majorana Zero Mode cavity)
        
            Parameters
            -----------
            lattice (lattice object): lattice defining basis vectors and such
            center (array-like): center of supercell
            radius_1 (float): radius of cylinders. By default, both sublattices but radius_2 (below) can override this
            R_max(float): maximum value of delta R term
            
            vort_center (array-like): determines the vortex center position that is used for calculating phi and r (default zero)
            vort_radius (float): number of unit cells defining the vortex radius
            winding_number (int): w term reflecting topology of arctan function. Positive or Negative.

            radius_2 (float): radius of cylinders in sublattice B. This is the same radius that is is modulated by the delta R term. If None, will default to radius_1
            scale (float): experimental; scales the position of the cylinders in the unit cell by stretching or shrinking the distance from the cell's origin.

            Keyword Arguments
            ------------------
    
            """
            self.lattice = lattice
            self.cellcenter = center
            self.rad1 = radius_1
            if radius_2 == None:
                self.rad2 = radius_1
            else:
                self.rad2 = radius_2 
            self.height = height
            self.rmax = R_max
            self.vortcenter = vort_center
            self.vortrad_cells = vort_radius
            self.winding = winding_number
            self.scaling = scale
            self.latt_const = self.lattice.magnitude[0]

            self.vortrad = self.vortrad_cells * self.latt_const

            #Building Geometries

            cyl1_position = self.lattice.lat_to_cart((1-self.scaling)*[1/3, 1/3, 0])
            cyl2_position = self.lattice.lat_to_cart((1+self.scaling)*[2/3, 2/3, 0])

            cyl1 = Cylinder(cyl1_position, radius=radius_1, height = self.height)
            cyl2 = Cylinder(cyl2_position, radius=radius_2, height = self.height)

            unitcell = [cyl1, cyl2]

            super().__init__(unitcell, center=self.cellcenter, rotation=120, unit='degrees', point='center')

    def calculate_modulation(self):
        self.rho, self.theta = self.calculate_radial_position()
        delR_term = self.rmax*np.tanh(self.rho/self.vortrad)
        KPlus = np.array(4*np.pi/(3*self.latt_const), 0)
        KMinus = np.array(-4*np.pi/(3*self.latt_const), 0)
        Ktot = KPlus - KMinus
        costerm = np.cos(np.dot(Ktot, self.rho) + (self.winding*self.theta))
        RMod = delR_term * costerm
        return RMod

    def calculate_radial_position(self):
        x, y ,z = self.cellcenter
        theta= np.arctan2(y, x)
        hypotenuse = np.hypot(x, y)
        return [hypotenuse, theta]

class HexagonalVortexCell(SuperCell):
    def __init__(
            self,
            lattice,
            center,
            side_length,
            m,
            m_max,
            phi,
            scale = 1,
            **kwargs
    ):
        """
        Constructs a Dirac Vortex SuperCell based on a hexagonal cell of triangles (see Ling Lu work mentioned above)


        Parameters
        -----------
        lattice (lattice object): lattice defining basis vectors and such

        center (array-like): center of supercell

        side_length (float): length of triangle sides. sqrt(3)/2 times Ling Lu's "r".

        m (float): local modulation value, calculated from the tanh potential equation

        m_max (float): global maximum modulation amplitude. Should be constant for a given system (i.e. don't change when copying cell)

        phi (float): position dependent phase term, given in radians. Should vary depending on angle of cell relative to center of the vortex structure

        scale (float): experimental; scales the position of the triangles in the unit cell by stretching or shrinking the distance from the cell's origin.



        Keyword Arguments
        ------------------
        'center'    : defines center for operations. default: None, unless rotation or translation is defined, then (0,0,0)

        'rotation'  : specifies copy+rotation of geometries in degrees. Rotates about center. Creates 360/value number of repetitions. default:None

        'translation': specifies copy+translation by vector. Relative to center. default:None

        
        
        
        """

        self.lattice = lattice
        self.diraccenter=center
        self.m = m
        self.m0 = m_max
        self.phi = phi
        tri1 = lattice.lat_to_cart(scale*[1/3, 1/3, 0])
        tri2 = lattice.lat_to_cart(scale*[2/3, 2/3, 0])

        self._side_length = side_length
        self._r = (2/np.sqrt(3))*self._side_length

        tri1new = vm.shift_angle(tri1, self.phi, self.m)

        tri1 = eqTriangle(1,self._side_length, center=tri1new, theta=-30) #left
        tri2 = eqTriangle(1,self._side_length, center=tri2, theta=30) #right
        #Build unit cell
        unitcell = [tri1, tri2]
        
        #initialize parent supercell, specifying the center of the supercell and creating the structures by rotating the unit cell 3 times about the center
        super().__init__(unitcell, center=self.diraccenter, rotation=120, unit='degrees', point='center' )

    @property
    def center(self):
        return self.diraccenter
    
    @center.setter
    def center(self, center):
        self.diraccenter = center

    def copy(self, **kwargs):
        """
        Makes a copy of the supercell. I don't know how center works since it also determines the center of the rotation. I might have to change that and implement a shift function.
        
        Create a supercell, then call this method to update and copy the parameters.
        
        """
        center = kwargs.get('center')
        phi = kwargs.get('phi')
        m = kwargs.get('m')
        print("copying: with m = ", m)
        print("copying: with phi = ", phi)

        newcopy = HexagonalVortexCell(self.lattice, center, self._side_length, m, self.m0, phi)

        return newcopy

class Cylinder(Structure):
    def __init__(
            self,
            center,
            radius,
            height,
            axis=2,
            **kwargs
    ):
        super().__init__()
        self.center = center
        self.original_center = kwargs.get("original_center", center)
        self.ogcenter = self.original_center
        self.radius = radius
        self.height = height      
        self.inaxis = axis
        self.axis = axis
        
        try: 
            if self.axis==2:
                self.axis=np.array([0, 0, 1])
            elif self.axis==1:
                self.axis=np.array([0, 1, 0])
            elif self.axis==0:
                self.axis=np.array([1, 0, 0])
            else:
                pass
        except ValueError:
            pass

    @classmethod
    def from_vertices(cls, vertices, radius, height_padding=False):
        """     
        Create a cylinder using the start and end points (vertices) and a specified radius

        
        Parameters
        -----------

        vertices : list of iterables
            starting and ending points. Should be in the form of [ (x,y,z), (x,y,z)]

        radius : float
            radius of cylinder
        
        """
        vert1 = np.asarray(vertices[0])
        vert2 = np.asarray(vertices[1])
        if height_padding == False:
            height = np.linalg.norm((vert2 - vert1))
        else:
            height = np.linalg.norm((vert2 - vert1))+height_padding

        
        center = np.mean((vert1, vert2), axis=0)
        axis = vert2 - vert1
        return cls(center=center, radius=radius, height=height, axis=axis)
    
    @classmethod
    def towards_point(cls, center, endpoint, radius,height):
        """Create a cylinder based on its start and end vertices"""
        center = np.asarray(center)
        endpoint = np.asarray(endpoint)
        axis = endpoint-center
        return cls(center=center, radius=radius, height=height, axis=axis)

    def copy(self, **kwargs):
        """
         kwargs
        -----------
        'center' : 3-list of new center for copied object
        'radius' : float of new radius for copied object        

        """
        cent = kwargs.get('center')
        rad = kwargs.get('radius')
  

        if 'radius' in kwargs: 
            if debug==True:print("Making Structure with radius: ", rad)
        else:
            newrad = self.radius


        if 'center' in kwargs:
            if debug==True:print("Making Structure with Center: ", cent)
            newcent = cent
        else:
            newcent = self.center
        newcopy = Cylinder(newcent, newrad, self.height, self.inaxis, original_center=self.ogcenter)
        
        return newcopy

class Sphere(Structure):

    def __init__(
        self,
        center,
        radius,
        **kwargs
    ):
        self.center = center
        self.original_center = kwargs.get("original_center", center)
        self.ogcenter = self.original_center
        self.radius = radius
        

    def copy(self, **kwargs):
        """
            kwargs
        -----------
        center : 3-list of new center for copied object
        radius : float of new radius for copied object        

        """
        cent = kwargs.get('center')
        rad = kwargs.get('radius')


        if 'radius' in kwargs: 
            if debug==True:print("Making Structure with radius: ", rad)
        else:
            newrad = self.radius


        if 'center' in kwargs:
            if debug==True:print("Making Structure with Center: ", cent)
            newcent = cent
        else:
            newcent = self.center
        newcopy = Sphere(newcent, newrad, original_center=self.ogcenter)
        
        return newcopy

class Triangle(Structure):
    """
    Class for triangular structures. Defines vertices, height, and center (centroid).
    Vertices are defined relative to centroid if center != None

    Note: Centroid is used for the definition instead of circumcenter. This was chosen to guarantee the center is inside
    the triangle. This might change in the future as the positions of the two are different. 

    """

    def __init__(
        self,
        vertices,
        height,
        axis=2,
        center=None,
        **kwargs
    ):
        """
        creates triangle

        Parameters:
            vertices (list of 3-tuples, array_like): the Cartesian x,y,z coordinates of each vertex with zero as origin
            height (float): The height of the triangular prism
            axis (0,1,2): Direction in which triangle is oriented. X = 0, Y = 1, Z = 2
            center (array_like or None): Center of triangle, shifts vertices if not None
            
        """
        
        self.height = height
        self._ogverts = np.asarray(vertices)
        self._centroid = kwargs.get("original_center", center)
        self.invertices = vertices
        self.inaxis = axis
        if axis==2:
            self.axis=np.array([0, 0, 1])
        elif axis==1:
            self.axis=np.array([0, 1, 0])
        elif axis==0:
            self.axis=np.array([1, 0, 0])
        else:
            print("Error: Axis not Found")

        self._centroid = np.asarray(np.sum(self.invertices, axis=(0))/np.size(self.invertices, 1))

        newvertices = self.invertices
        if center is not None and len(vertices):
            self.center = np.asarray(center)
            shift = center-self._centroid
            newvertices = self.invertices + shift
            self.shiftedcentroid = np.asarray(np.sum(newvertices, axis=(0))/np.size(newvertices, 1))
        else:
            self.shiftedcentroid = self._centroid

        self.vertices = newvertices
        self.vertlist = self.vertices.tolist()

        ## Temporary setting of center to centroid. Probs not good long-term
        self.center = self.centroid

    @property
    def original_centroid(self):
        """Access to centroid before shifting. Not same as center."""
        return self._centroid
    
    @property
    def original_center(self):
        """Someday this will be fixed for center vs centroid, but for now, it's an alias for the original_centroid command"""
        return self._centroid
    
    
    @property
    def centroid(self):
        return self.shiftedcentroid
    
    @property
    def original_vertices(self):
        """Access to original vertices before scaling and shifting. """
        return self._ogverts

    @property
    def verttuple(self):
        newlist = []
        for n in self.vertlist:
            tuppoint = tuple(n)
            newlist.append(tuppoint)
        return newlist

    @property
    def bounds(self):
        if self.inaxis==0:
            extent = [self.centroid[0]-self.height/2, self.centroid[0]+self.height/2]
        elif self.inaxis==1:
            extent = [self.centroid[1]-self.height/2, self.centroid[1]+self.height/2]
        elif self.inaxis==2:
            extent = [self.centroid[2]-self.height/2, self.centroid[2]+self.height/2]
        return extent
    
    def calc_circumcenter(self):
        """The circumcenter calculations are more involved than the centroid ones
        This function exists in case I need to do those calculations at some point"""
        return
    
    def copy(self, **kwargs):
        """
        create new instance of the structure with the same parameters but different center
        This might be changed in the future to incorporate more kwargs and allow for more control in copying

        kwargs
        -----------
        'center' : 3-list of new center for copied object
         

        """
        cent = kwargs.get('center')
        verts = kwargs.get('vertices')
  

        if 'vertices' in kwargs: 
            if debug==True: print("Making Structure with Vertices: ", verts)
            newverts = verts
            newcopy = Triangle(newverts, self.height, self.inaxis)
        else:
            newverts = self.vertices

        if 'center' in kwargs:
            if debug==True: print("Making Structure with Center: ", cent)
            newcent = cent
            newcopy = Triangle(self.vertices, self.height, self.inaxis, newcent)
        else:
            newcent = self.center
        
        if 'center' in kwargs and 'vertices' in kwargs:
            print("Center and Vertices Both Defined. This may not shift like you expect. Please check results.")
            newcopy = Triangle(newverts, self.height, self.inaxis, newcent)
        
        return newcopy

class eqTriangle(Triangle):
    """

    this creates an equilateral triangle centered at zero with side length b,
    oriented with 0 degrees being pointing up

    """
    def __init__(
        self,
        height,
        b=1,
        axis=2,
        center=None,
        theta = 0,
        **kwargs):

        """
        Parameters:
            height (float): height of triangle
            b (float): length of sides
            axis (0,1,2): axis normal to face 0-X, 1-Y, 2-Z
            center (None, array_like): center position that all vertices are shifted to
            theta (degrees): ccw angle of rotation (0 is pointing up)  
        """

        self.b = b
        self.scaled_verts = np.array([[0, np.sqrt(3)/3, 0],
                                    [1/2, -1/(2*np.sqrt(3)), 0], 
                                    [-1/2, -1/(2*np.sqrt(3)), 0]
                                    ])*self.b
        

        self.vertices = vm.rotate(self.scaled_verts, theta, axis=2, unit='degrees', toarray=True)
        
        @property
        def vertlist(self):
            return self.vertices.tolist()

        @property
        def verttuple(self):
            newlist = []
            for n in self.vertlist:
                tuppoint = tuple(n)
                newlist.append(tuppoint)
            return newlist


        Triangle.__init__(self, vertices=self.vertices, height=height, axis=axis, center=center)


def NearestNeighbors(points, radius, neighborhood_range):
    """
    Connect nearest neighbors in a list of points with cylinders

    Parameters
    -----------

    points : list of (x,y,z) tuples
        Positions to search for neighbors within
        
    radius : float
        radius of connecting rods
        
    neighborhood : float
        distance to define neighbors

    """
    pointarr = np.asarray(points)
    kdtree = scs.KDTree(pointarr, leafsize=15, compact_nodes=True)
    neighbors = kdtree.query_pairs(r=neighborhood_range, p=2)
    structure_list = []
    for pair in neighbors:
        point = pointarr[pair[0]]
        neighbor = pointarr[pair[1]]
        structure_list.append(Cylinder.from_vertices([point, neighbor], radius=radius))
    return structure_list




if __name__ == "__main__":
    rng = np.random.default_rng()
    points = rng.random((15, 3))

    test = NearestNeighbors(points, radius=.5, neighborhood_range=.3)

import numpy as np
import ast
from matplotlib import pyplot as plt
from crystalbuilder import vectors as vm
import copy
from crystalbuilder import geometry as geometry

debug='off'
scattersizes = 1/72

def check_numbound(point:list, bound1:list, bound2:list, bound3:list):
    if  (bound1[0] <= point[0] <= bound1[1]) == False:
        return False
    elif (bound2[0] <= point[1] <= bound2[1]) == False:
        return False
    elif (bound3[0] <= point[2] <= bound3[1]) == False:
        return False
    else:
        return True
    
def _plot_modulation(modulation_output, **kwargs):
    """
    Makes a scatter plot of each point, color coded by its modulation, on a scale of -maxmod to maxmod

    Returns nothing. Simply plots. 

    point sizes are determined by global variable scattersizes, which can be changed after import.
    """
    ax = kwargs.get("ax")
    position = modulation_output[0]
    mod = modulation_output[1]
    maxmod = modulation_output[2][0]
    if debug=='on': print("The inputs are position[0]: {}, position[1]: {} \n mod:{}, maxmod: {}".format(position[0], position[1], mod, maxmod))
    if ax == None:
        plt.scatter(position[0], position[1], c=mod, vmin=-maxmod, vmax=maxmod, cmap='Spectral', s=scattersizes, linewidths=0)
    else:
        ax.scatter(position[0], position[1], c=mod, vmin=-maxmod, vmax=maxmod, cmap='Spectral',  s=scattersizes, linewidths=0)

class Lattice:
    """
    This class handles defining and building the lattice itself, but also includes the functions for making
    repeats of geometries. 
    
    """

    def __init__(
            self,
            a1 = np.array([1,0,0]),
            a2 = np.array([0,1,0]),
            a3 = np.array([0,0,1]),
            magnitude = np.array([1,1,1]),
            **kwargs):
        """
        The Lattice class can be initialized with specified a1, a2, a3 vectors and magnitude

        Parameters:
            a1 (3-array, asarray-compatible object): first lattice vector - defaults to 1,0,0 (Cartesian X)
            a2 (3-array, asarray-compatible object): second lattice vector - defaults to 0,1,0 (Cartesian Y)
            a3 (3-array, asarray-compatible object): third lattice vector - defaults to 0,0,1 (Cartesian Z)
            magnitude (3-array, asarray-compatible object): lattice vector lengths - defaults to 1,1,1 (unit vectors)

        Properties
        -----------
        basis : array of vectors scaled to magnitudes

        """
        self.a1 = np.asarray(a1)
        self.a2 = np.asarray(a2)
        self.a3 = np.asarray(a3)
        self.magnitude = np.asarray(magnitude)
        self.array = kwargs.get("a_array", None)
        self.latt_const = self.magnitude[0]

        if self.array != None:
            self.a1 = self.array[0]
            self.a2 = self.array[1]
            self.a3 = self.array[2]

    
        self.a1_scaled = ((self.a1/np.sqrt(self.a1.dot(self.a1)))*self.magnitude[0])
        self.a2_scaled = ((self.a2/np.sqrt(self.a2.dot(self.a2)))*self.magnitude[1])
        self.a3_scaled = ((self.a3/np.sqrt(self.a3.dot(self.a3)))*self.magnitude[2])

        self.basis = np.concatenate([[self.a1_scaled],[self.a2_scaled], [self.a3_scaled]], axis=0)

### Basis Manipulation ###
    def rotate_basis(self, theta, axis = 2, unit='degrees'):
        origin = (0,0,0)
        self.basis[0] = vm.rotate([self.a1_scaled], theta, origin, axis=axis, unit=unit, toarray=True)
        self.basis[1] = vm.rotate([self.a2_scaled], theta, origin, axis=axis, unit=unit, toarray=True)
        self.basis[2] = vm.rotate([self.a3_scaled], theta, origin, axis=axis, unit=unit, toarray=True)

### Convenience Methods ###
    def lat_to_cart(self, point):
        newpoint= vm.basis_change(self.basis, 'cartesian', point)
        return newpoint

    def cart_to_lat(self, point):
        newpoint = vm.basis_change('cartesian', self.basis, point)
        return newpoint
    
    def cart_to_polar(self, point):
        newpoint = vm.cart_to_pol(point)
        return newpoint
    

### Tiling Methods ###
    def tile_mpgeometry(self, VerticesList:list, a1reps:int, a2reps:int, a3reps:int, style='centered'):
        """
        INCOMPLETE - RETURNS COORDINATES, NOT NEW OBJECTS;
        For MEEP/MPB
        Accepts a structure defined by VerticesList, then adds various combinations of basis vectors to
        repeat the structures a1reps * a2reps times. Style determines if reps are formed from adding and subtracting
        or just adding the basis vectors (e.g. if the first point is the bottom left or center of final tiling)

        Parameters
        ----------
            VerticesList: list of lists, Vector3, or array_like
                vertices of geometry object(s)
            a1reps, a2reps, a3reps: int
                number of repetitions along a1, a2, a3 lattice vectors respectively
            style: str 
                "centered" or "positive" to tile in all directions or in +x only. 
        Returns
        -------
            newpos: list
                List of lists with [x,y,z] coordinates of the lattice sites


        """
        
        #All points are going to be 3-tuples or 3-lists. Varying number of vertices in each geometry. 
        geolist = []
        newpos = []
        #print(type(VerticesList))
        #print(isinstance(VerticesList, Triangle))
        if isinstance(VerticesList, geometry.Triangle):
            VerticesList = VerticesList.vertlist

        for geometry in VerticesList:
            #iterate through the list of geometry objects
            if isinstance(geometry, list):
                #print(geometry)
                xcen = geometry[0]
                ycen = geometry[1]
                zcen = geometry[2]

                
                geolist.append([xcen, ycen, zcen])
                for n in range(a1reps):
                    if style == 'centered':
                        n+= -(a1reps//2)
                    for m in range(a2reps):
                        if style == 'centered':
                            m+= -(a2reps//2)
                        for k in range(0,a3reps):
                            if style == 'centered':
                                k+= -(a3reps//2)

                            newx = xcen+(n*self.basis[0][0] + m*self.basis[1][0] + k*self.basis[2][0])
                            newy = ycen+(n*self.basis[0][1] + m*self.basis[1][1] + k*self.basis[2][1])
                            newz = zcen+(n*self.basis[0][2] + m*self.basis[1][2] + k*self.basis[2][2])

                            newpos.append([newx, newy, newz])

                            
                
            else:
                print("This is a", type(geometry), '\n')
            
        return newpos

    def tile_tdgeometry(self, Geometry, a1reps:int, a2reps:int, a3reps: int, style='centered', **kwargs):
        import tidy3d as td
        
        """
        Tiles Tidy3D Geometry
        Similar to tile_mpgeometry, but meant for tidy3d classes. Can accept either Geometry or GeometryGroup

        Parameters
        ------
        Geometry : Tidy3D Geometry Object
            Geometry or list of geometries to tile
        a1reps : int
            number of repetitions in a1 direction
        a2reps : int
            number of repetitions in a2 direction
        a3reps : int
            number of repetitions in a3 direction
        style :  'centered', 'positive', 'bounded', 'numbounded'
            bounded options require kwargs

        Keyword Arguments
        -----------------
        a1bounds: list
            start and end bounds in a1 direction. 
            If style is 'bounded', a1bounds should be [int, int] to define starting and stopping lattice sites
            if style is 'numbounded', a1bounds should be [float, float] to define starting and stopping coordinates

        a2bounds: list
            start and end bounds in a2 direction. 
            If style is 'bounded', a2bounds should be [int, int] to define starting and stopping lattice sites
            if style is 'numbounded', a2bounds should be [float, float] to define starting and stopping coordinates
        
        a3bounds: list
            start and end bounds in a3 direction. 
            If style is 'bounded', a3bounds should be [int, int] to define starting and stopping lattice sites
            if style is 'numbounded', a3bounds should be [float, float] to define starting and stopping coordinates

        """
        newgeom = []
        if isinstance(Geometry, td.GeometryGroup):
            print("It's a Geometry Group")
            for n in Geometry.geometries:
                if isinstance(n, td.PolySlab):
                    print("Polyslab has no center attribute")

                else:
                    xcen = n.center[0]
                    ycen = n.center[1]
                    zcen = n.center[2]
                
                tiledpoints = self.tiling([xcen, ycen,zcen], a1reps, a2reps, a3reps, style=style)
                
                for m in range(0,len(tiledpoints)):
                    newgeom.append(n.updated_copy(center=tiledpoints[m]))
                    
                
        elif isinstance(Geometry, (td.components.geometry.Box, td.components.geometry.Sphere, td.components.geometry.Cylinder, td.components.geometry.PolySlab, td.components.geometry.TriangleMesh)):
            print("It's a ", type(Geometry))
        
        else:
            print("Geometry must be a td.Geometry object, not ", type(Geometry))

        return td.GeometryGroup(geometries=newgeom)

    def tile_geogeometry(self, Geometry, a1reps:int, a2reps:int, a3reps: int, style='centered', **kwargs):
        """
        Tiles CrystalBuilder.geometry object and outputs new lists of vertices.

        This method is recommended for all new structures. the conversion_methods module can be used to convert the output to MPB or Tidy3D. it's recommended to only use the other methods if there is an existing MPB or Tidy3D structure you are trying to tile.
    
        Parameters
        ------
        Geometry : CrystalBuilder.geometry object
            Geometry or list of geometries to tile
        a1reps : int
            number of repetitions in a1 direction
        a2reps : int
            number of repetitions in a2 direction
        a3reps : int
            number of repetitions in a3 direction
        style :  'centered', 'positive', 'bounded', 'numbounded', 'radial'
            bounded options require kwargs

        Keyword Arguments
        -----------------
        a1bounds: list
            start and end bounds in a1 direction. 
            If style is 'bounded', a1bounds should be [int, int] to define starting and stopping lattice sites
            if style is 'numbounded', a1bounds should be [float, float] to define starting and stopping coordinates

        a2bounds: list
            start and end bounds in a2 direction. 
            If style is 'bounded', a2bounds should be [int, int] to define starting and stopping lattice sites
            if style is 'numbounded', a2bounds should be [float, float] to define starting and stopping coordinates
        
        a3bounds: list
            start and end bounds in a3 direction. 
            If style is 'bounded', a3bounds should be [int, int] to define starting and stopping lattice sites
            if style is 'numbounded', a3bounds should be [float, float] to define starting and stopping coordinates

        """
   
        newgeom = []
        if isinstance(Geometry, geometry.Triangle):
            if vm.debug == 'on': print("Lat: Geometry is a Triangle")
            xcen = Geometry.center[0]
            ycen = Geometry.center[1]
            zcen = Geometry.center[2]
            if vm.debug == 'on': print("Lat: ", [xcen, ycen, zcen])

            tiledpoints = self.tiling([xcen, ycen,zcen], a1reps, a2reps, a3reps, style=style)
            if vm.debug == 'on': print("Lat: ", tiledpoints)

            for m in range(0,len(tiledpoints)):
                if vm.debug == 'on': print("Lat: the center is: \n", tiledpoints[m], "\n")
                newstruct = Geometry.copy(center=tiledpoints[m])
                newgeom.append(newstruct)
            
            if vm.debug == 'on':
                print("Lat: ", "newgeom = ", newgeom[0].center, "   ", newgeom[1].center)
    
        elif isinstance(Geometry, geometry.Sphere):
            if vm.debug == 'on': print("Lat: Geometry is a Sphere")
            xcen = Geometry.center[0]
            ycen = Geometry.center[1]
            zcen = Geometry.center[2]
            if vm.debug == 'on': print("Lat: ", [xcen, ycen, zcen])

            tiledpoints = self.tiling([xcen, ycen,zcen], a1reps, a2reps, a3reps, style=style)
            if vm.debug == 'on': print("Lat: ", tiledpoints)

            for m in range(0,len(tiledpoints)):
                if vm.debug == 'on': print("Lat: the center is: \n", tiledpoints[m], "\n")
                newstruct = Geometry.copy(center=tiledpoints[m])
                newgeom.append(newstruct)
            
            if vm.debug == 'on':
                print("Lat: ", "newgeom = ", newgeom[0].center, "   ", newgeom[1].center)

        elif isinstance(Geometry, list):
            if vm.debug == 'on': print("Lat: Geometry is a list")
            for n in Geometry:
                xcen = n.center[0]
                ycen = n.center[1]
                zcen = n.center[2]
            
                tiledpoints = self.tiling([xcen, ycen,zcen], a1reps, a2reps, a3reps, style=style)
            
                for m in range(0,len(tiledpoints)):
                    newstruct = n.copy(center=tiledpoints[m])
                    newgeom.append(newstruct)

        elif isinstance(Geometry, geometry.SuperCell):
            if debug == 'on': print("Lat: Geometry is a SuperCell")
            xcen = Geometry.center[0]
            ycen = Geometry.center[1]
            zcen = Geometry.center[2]
            if debug == 'on': print("Lat: Cell Center is ", str([xcen, ycen, zcen]))

            tiledpoints = self.tiling([xcen, ycen,zcen], a1reps, a2reps, a3reps, style=style)
            if debug == 'on': print("Lat: The Tiled Points are at ", tiledpoints)

            for m in range(0,len(tiledpoints)):
                if debug == 'on': print("Lat: the center is: \n", tiledpoints[m], "\n")
                newstruct = Geometry.copy(center=tiledpoints[m], relative_center=[xcen, ycen, zcen])
                newgeom.append(newstruct)
            
            if debug == 'on':
                print("Lat: newgeom = ", newgeom[0].center, "   ", newgeom[1].center)

        else:
            print("Geometry must be a CrystalBuilder.geometry object, not ", type(Geometry))
        
        return newgeom

    def _radial_tiling(self, centers, radius:int, startrad=0):
        """
        Tiles in 2D radially from [startrad] to [radius] unit cells

        Should be called by passing "radial" as the style for tile_geogeometry()
        """
        xcen = centers[0]
        ycen = centers[1]
        zcen = centers[2]

        krange = range(int(np.ceil(-5)), int(np.ceil(5))) 
        mrange = range(int(np.ceil(-5)), int(np.ceil(5))) 
        prange = range(int(np.ceil(-2)), int(np.ceil(2)))

        newpoints = []
        for k in krange: #a1 loop
            for m in mrange: # a2 loop
                for p in prange: # a3 loop
                    if (abs(k) <= radius) and (abs(m) <= radius) and (abs(k) >= startrad) and (abs(m) >= startrad) :
                        newx = xcen+(k*self.basis[0][0] + m*self.basis[1][0] + p*self.basis[2][0])
                        newy = ycen+(k*self.basis[0][1] + m*self.basis[1][1] + p*self.basis[2][1])
                        newz = zcen+(k*self.basis[0][2] + m*self.basis[1][2] + p*self.basis[2][2])                 
                        newvert = [newx, newy, newz]
                    # if check_radbound(newvert, a1lims, a2lims, a3lims) == True:
                        newpoints.append(newvert)

        
        return newpoints

    def tiling(self,centers:list, a1reps:int, a2reps:int, a3reps:int, style='centered', **kwargs):
        """
        Tiling function called by Tidy3D and Meep methods. Accepts [xcen, ycen, zcen] for structures with centers.
        Else, idk yet. Not sure how I want to do triangles.

        Parameters
        ----------
        centers : list
            X,Y,Z center in order
        a1reps : int
            number of repetitions in basis direction a1
        a2reps : int
            number of repetitions in basis direction a2
        a3reps : int
            number of repetitions in basis direction a3
        style : str
            "centered" to shift tiling center to 0,0,0.
            
            'positive' to tile from 0,0,0 in the positive directions
            
            'bounded' tile from a1bounds[0] to a1bounds[1] (and a2bounds, a3bounds), given in lattice units
            
            'numbounded' tile from a1bounds[0] to a1bounds[1] given in raw coordinates
            
            'radial' to tile a circular-ish region
            
        
        """
        
        if (style=='centered'):
            krange = range(int(np.ceil(-a1reps/2)), int(np.ceil(a1reps/2))) 
            mrange = range(int(np.ceil(-a2reps/2)), int(np.ceil(a2reps/2))) 
            prange = range(int(np.ceil(-a3reps/2)), int(np.ceil(a3reps/2))) 

        elif style=='positive':
            krange = range(a1reps)
            mrange = range(a2reps)
            prange = range(a3reps)
        
        elif style=='bounded':
            a1lims = kwargs.get("a1bounds", [0,a1reps])
            a2lims = kwargs.get("a2bounds", [0,a2reps])
            a3lims = kwargs.get("a3bounds", [0,a3reps])

            krange = range(a1lims[0], a1lims[1])
            mrange = range(a2lims[0], a2lims[1])
            prange = range(a3lims[0], a3lims[1])

        elif style=='numbounded':
            #defcut defines number of unit cells numerically. 
            a1lims = kwargs.get("a1bounds", [0, a1reps * self.magnitude[0]])
            a2lims = kwargs.get("a2bounds", [0, a2reps * self.magnitude[1]])
            a3lims = kwargs.get("a3bounds", [0, a3reps * self.magnitude[2]])

            #Condition bounds
            """
            Round up the number of lattice vectors to reach the max value, round down the number required for the minimum.
            Then add 2 and subtract 2 respectively to add 2 unit cell of padding for the bounds. There will
            be a second step that checks the coordinates themselves, so this is just to tell the for
            loop how long to go.
            """
            maxa1 = int(np.ceil(a1lims[1]/self.magnitude[0]))
            maxa2 = int(np.ceil(a2lims[1]/self.magnitude[1]))
            maxa3 = int(np.ceil(a3lims[1]/self.magnitude[2]))

            mina1 = int(np.floor(a1lims[0]/self.magnitude[0]))
            mina2 = int(np.floor(a2lims[0]/self.magnitude[1]))
            mina3 = int(np.floor(a3lims[0]/self.magnitude[2]))

            krange = range(mina1, maxa1)
            mrange = range(mina2, maxa2)
            prange = range(mina3, maxa3)

        elif style=='radial':
            krange = range(int(np.ceil(-a1reps)), int(np.ceil(a1reps))) 
            mrange = range(int(np.ceil(-a2reps)), int(np.ceil(a2reps))) 
            prange = range(int(np.ceil(-a3reps)), int(np.ceil(a3reps))) 
            startrad = kwargs.get("start_radius", 0)
            radius = kwargs.get("radius", max(a1reps, a2reps))
        else:
            pass


        xcen = centers[0]
        ycen = centers[1]
        zcen = centers[2]

        newpoints = []
        if style !='radial':
            for k in krange: #a1 loop
                for m in mrange: # a2 loop
                    for p in prange: # a3 loop
                        newx = xcen+(k*self.basis[0][0] + m*self.basis[1][0] + p*self.basis[2][0])
                        newy = ycen+(k*self.basis[0][1] + m*self.basis[1][1] + p*self.basis[2][1])
                        newz = zcen+(k*self.basis[0][2] + m*self.basis[1][2] + p*self.basis[2][2])
                                            
                        newvert = [newx, newy, newz]
                        
                        if style != 'numbounded':
                            newpoints.append(newvert)

                        elif style == "numbounded":
                            if check_numbound(newvert, a1lims, a2lims, a3lims) == True:
                                newpoints.append(newvert)
                            else:
                                pass
                            
                        else:
                            pass
        
        return newpoints

    def cubic_tiling(self, centers:list, a1reps:int, a2reps:int, a3reps:int, **kwargs):
        """
        Tile unit cells in a way that gives a cubic or semi-cubic structure by limiting bounds.
        """
        

        
        pass
     

### Tiling Modifications ###
    """ These are functions that apply the below modulations to the tiled lattice"""

    def modulate_cells(self, structure, vortex_radius, winding_number, max_modulation, modulation_type='radius', whole_cell=True, plot_modulation = False, **kwargs ):
        if debug == "on": print("Modulating Cells for %s" %(structure))
        poslist = []
        modlist = []
        ax = kwargs.get("ax")
        if (modulation_type=="radius") or (modulation_type=="balanced"):
            if whole_cell == True:
                """This does discrete modifications of each supercell, not a continuous overlaid modulation"""
                modulation = self.kekule_modulation(geo_object=structure, vortex_radius=vortex_radius, winding_number=winding_number, max_modulation=max_modulation, modulation_type=modulation_type,output_modulation= plot_modulation)
                if modulation != None:
                    if plot_modulation == True:
                        if ax != None:
                            _plot_modulation(modulation, ax=ax)
                        else:
                            _plot_modulation(modulation)
                    poslist.append(modulation[0])
                    modlist.append(modulation[1])
                    print(modulation)
                    modlist.append(modulation)
                

            else:
                """This applies a gradient modification"""
                cellcenter = structure.center
                for n in structure.structures:
                    modulation = self.kekule_modulation(geo_object=n, vortex_radius=vortex_radius, winding_number=winding_number, max_modulation=max_modulation, modulation_type=modulation_type, cell_center = cellcenter, output_modulation= plot_modulation)
                    if modulation != None:
                        if plot_modulation == True:
                            if ax != None:
                                _plot_modulation(modulation, ax=ax)
                            else:
                                _plot_modulation(modulation)
                        poslist.append(modulation[0])
                        modlist.append(modulation[1])
        
        elif modulation_type=="dual":
            cellcenter = structure.center
            for n in structure.structures:
                modulation = self.dual_modulation(geo_object=n, vortex_radius=vortex_radius, winding_number=winding_number, max_modulation=max_modulation, cell_center = cellcenter, output_modulation= plot_modulation)
                if modulation != None:
                    if plot_modulation == True:
                        if ax != None:
                            _plot_modulation(modulation, ax=ax)
                        else:
                            _plot_modulation(modulation)
                    poslist.append(modulation[0])
                    modlist.append(modulation[1])


### Modulation Methods ###
    """These should all act on a single object in a single position! This keeps them modular and easily integrated to tiling methods"""

    def kekule_modulation(self, geo_object, vortex_radius, winding_number, max_modulation, modulation_type = 'radius', normalize = True, **kwargs):
        position = geo_object.center
        winding = winding_number

        #this only matters for the case in which all modulations are radial only (e.g. r is constant)
        cellcenter = kwargs.get("cell_center", None)

        output_rmod = kwargs.get("output_modulation", False)

        if normalize == True:
            maxmod = max_modulation * self.magnitude
            vortrad = vortex_radius * self.magnitude

        else:   
            maxmod = max_modulation   
            vortrad = vortex_radius
  
        if modulation_type == 'radius':
            rmod = self._kekule_radius_mod(position, vortrad, winding, maxmod)
            oldrad = geo_object.radius
            newrad = oldrad + rmod
            if newrad > 0:
                geo_object.radius = newrad
            elif newrad <= 0: 
                geo_object.radius = 0
                print("negative radius calculated. Check Units!")
            if debug == "on": print(geo_object, " is now radius ", newrad)

        if modulation_type == 'balanced':
            absolute_position = geo_object.center.tolist()
            in_cell_position = np.asarray(geo_object.center) - np.asarray(cellcenter)
            if debug == 'on': print("The relative position of the structure is", position)

            rmod = self._kekule_radius_mod(position, vortrad, winding, maxmod, in_cell_pos = in_cell_position)
            oldrad = geo_object.radius
            newrad = oldrad + rmod
            if newrad > 0:
                geo_object.radius = newrad
            elif newrad <= 0: 
                geo_object.radius = 0
                print("negative radius calculated. Check Units!")
            if debug == "on": print(geo_object, " is now radius ", newrad)


        elif modulation_type == 'position':
            print("Error: position modulation is not implemented yet.")

        if output_rmod == True:
            return (absolute_position, rmod, maxmod)

    def dual_modulation(self, geo_object, vortex_radius,
                        winding_number, max_modulation, normalize=True, **kwargs):
        position = geo_object.center
        winding = winding_number
        if normalize == True:
            maxmod = max_modulation * self.magnitude
            vortrad = vortex_radius * self.magnitude

        else:   
            maxmod = max_modulation   
            vortrad = vortex_radius
        #this only matters for the case in which all modulations are radial only (e.g. r is constant)
        cellcenter = kwargs.get("cell_center", None)
        output_rmod = kwargs.get("output_modulation", False)

        absolute_position = geo_object.center.tolist()
        in_cell_position = np.asarray(geo_object.center) - np.asarray(cellcenter)

        center_distance = np.linalg.norm(in_cell_position)


        if debug == 'on': print("The relative position of the structure is", position)

        posmod, rmod = self._dual_symmetry_mod(position, vortrad, winding, maxmod, in_cell_pos = in_cell_position)


        #Will need to do this for position, but the delta affects d, which isn't carried by the geometry object. So I might have to recalculate it. The effect of the modulation is "d= a0/3 - delta_t" That's the same as subtracting that delta t term from my existing d term. Since these objects won't inherit the d term, I need to reformulate this w.r.t. their coordinates. A little distributive property shows that a positive or negative delta_t*(x,y)/(a0/3) could be added or subtracted. 

        oldrad = geo_object.radius
        newrad = oldrad + rmod
        oldpos = np.asarray(geo_object.center)
        newpos = in_cell_position + (posmod/center_distance)*in_cell_position + np.asarray(cellcenter)
        if debug == 'on':
            print("The new position would be: ", newpos)
            print("The old position was: ", oldpos)
            print("\n")
            
        if newrad > 0:
            geo_object.radius = newrad
            geo_object.center = newpos

        elif newrad <= 0: 
            geo_object.radius = 0
            geo_object.center = newpos
            print("negative radius calculated. Check Units!")

        if debug == "on": print(geo_object, " is now radius ", newrad)

        if output_rmod == True:
            return (absolute_position, rmod, maxmod)


### Modulation Core Methods ###
    """
    These are the actual equations for performing the modulation. They should return some parameter that gets passed to the above Modulation Methods, which will then apply that parameter to the structure. 

    e.g. _kekule_radius_mod returns a delta radius term, that kekule_modulation adds to the radius of a cylinder.
    """
    def _kekule_radius_mod(self, position, vortrad, winding, maxmod, **kwargs):
        cellpos = kwargs.get("in_cell_pos", None) #position of structure relative to cell center
        
        #Next, check if the structure's cartesian position will be specified relative to the center of the supercell or be set to the same as the absolute positition (relative to center of vortex at 0,0)
        try:
            if cellpos.any != None:
                cartpos = cellpos[:2]
                print("Using in-cell-position: ", cartpos)
            else:
                cartpos = position[:2]
        except AttributeError:
            if cellpos != None:
                cartpos = cellpos[:2]
                print("Using in-cell-position: ", cartpos)
            else:
                cartpos = position[:2]

        if debug == "on": print("cartpos = ", cartpos)
        #Generate the polar coordinates of the absolute position
        polpos = vm.cart_to_pol(position)
        rho, theta = polpos[0], polpos[1]

        #Create delta R modulation term from rho (polar distance)
        delR_term = maxmod*np.tanh(rho/vortrad)
        if debug == "on": print("delR_term = ", delR_term)
        #The K+ and K - points get summed to Ktot, whose dot product with the cartesian coordinate (relative or absolute) selects for the two sublattices or the center pillar (+, -, 0). 
        KPlus = np.array([4*np.pi/(3*self.latt_const), 0])
        KMinus = np.array([-4*np.pi/(3*self.latt_const), 0])
        Ktot = KPlus - KMinus
        if debug == "on": print("lat: Ktot = ", Ktot)
        costerm = np.cos(np.dot(Ktot, cartpos) + (winding*theta))
        if debug == "only_dot": print(f"lat: dot product = {np.dot(Ktot, cartpos)}" )
        if debug == "on": print("costerm = ", costerm)
        RMod = delR_term[0] * costerm
        if debug == "on": print("RMod = ", RMod)
        return RMod
    
    def _dual_symmetry_mod(self, position, vortrad, winding, maxmod, alpha=4, **kwargs):
        """
        This is a low-level modulation function using the scheme of Jingwen Ma et al. The modulation is basically a simultaneous spin-hall and valley-hall perturbation, where the lattice is contracted/expanded while the C6 symmetry is broken to two C3 sublattices. 

        The paper defines two modulation terms: delta_t and delta_i (dt, di) with some magnitude d0. These terms come from d0(alpha*sin(theta), cos(theta)). The alpha gets set to .65 for positive dt and .33 for negative dt. 


        """

        cellpos = kwargs.get("in_cell_pos", None)
        
        try:
            if cellpos.any != None:
                cartpos = cellpos[:2]
            else:
                cartpos = position[:2]
        except AttributeError:
            if cellpos != None:
                cartpos = cellpos[:2]
            else:
                cartpos = position[:2]

        pos_alpha = .65
        neg_alpha = .33
        polpos = vm.cart_to_pol(position)


        rho, theta = polpos[0], polpos[1]

        delta_0 = maxmod*(np.tanh(rho/vortrad)**alpha)

       
        """
        There needs to be a way to select the two sublattices. 
        Sublattice 1:
        [0, -d]
        [-d*sqrt(3)/2, d/2]
        [d*sqrt(3)/2, d/2]

        Sublattice 2:
        [0, d]
        [d*sqrt(3)/2, -d/2]
        [-d*sqrt(3)/2, -d/2]

        if x = 0 and y = - ...

        
        """
        
        if (cartpos[0] > 0) and (cartpos[1] >= 0):
            lattice_selector = 1
        elif (cartpos[0] < 0) and (cartpos[1] >= 0):
            lattice_selector = 1
        elif (np.isclose(cartpos[0], 0)) and (cartpos[1] < 0):
            lattice_selector = 1
        elif (np.isclose(cartpos[0], 0)) and (cartpos[1] > 0):
            lattice_selector = -1
        elif (cartpos[0] > 0) and (cartpos[1] < 0):
            lattice_selector = -1
        elif (cartpos[0] < 0) and (cartpos[1] < 0):
            lattice_selector = -1
        else:
            print(cartpos)



        delta_t_pre = delta_0[0]*np.sin((winding*theta))

        if delta_t_pre <= 0:
            delta_t = delta_t_pre*neg_alpha
        elif delta_t_pre >=0:
            delta_t = delta_t_pre*pos_alpha

        delta_i = delta_0[0] * np.cos((winding*theta))

        if lattice_selector >= 0:
            sizemod = delta_i

        elif lattice_selector < 0:
            sizemod = -1*delta_i


        return [delta_t, sizemod]

            









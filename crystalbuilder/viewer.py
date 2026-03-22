import vedo
import crystalbuilder
import crystalbuilder.geometry as geo
import crystalbuilder.lattice as lat

vedo.settings.default_backend='vtk'

class Plot(vedo.Plotter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def add_to_visualizer(self, structures, **kwargs):
        add_to_visualizer(structures, self, **kwargs )
        
    def show_cell(self, lattice):
        origin = [0,0,0]
        vectors = lattice.basis
        self.lines = []
        for v in vectors:
            _line = vedo.Line(origin, v)
            self.lines.append(_line)
        self.add(self.lines)
        
    def intersect_geometry(self):
        objects = self.get_meshes()
        main_obj = objects[0]
        for n in range(1, len(objects)):
            main_obj = main_obj.boolean('plus',objects[n]).c("blue")
        return main_obj

def add_to_visualizer(structures, plot, **kwargs):
    for object in structures:     
        if isinstance(object, vedo.Mesh):
            print("vedo mesh")
            plot += object
        elif isinstance(object, vedo.Cylinder):
            print("vedo cylinder")
            plot += object
        elif isinstance(object, geo.Cylinder):
            plot += visualize_cylinder(object, **kwargs)
        elif isinstance(object, geo.Sphere):
            plot += visualize_sphere(object, **kwargs)
        elif isinstance(object, geo.SuperCell):
            plot += visualize_supercell(object, **kwargs)


def visualize(structures, plotter_style=3, **kwargs):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    
    plot = Plot(axes=plotter_style)

    add_to_visualizer(structures, plot, **kwargs)
    
    # for object in structures:
    #     if isinstance(object, geo.Structure):
    #         if isinstance(object, geo.Cylinder):
    #             obj  = visualize_cylinder(object, **kwargs)
    #             plot += obj
    #         elif isinstance(object, geo.SuperCell):
    #             obj  = visualize_supercell(object, **kwargs)
    #             plot += obj
    #         elif isinstance(object, geo.Sphere):
    #             obj = visualize_sphere(object, **kwargs)
    #             plot += obj
    #     elif isinstance(object, list):
    #         for n in object:
                
            
    return plot

def visualize_cylinder(cylinder, **kwargs):
    center = cylinder.center
    radius = cylinder.radius
    height = cylinder.height
    axis = cylinder.axis
    name = str(cylinder.center)
    obj = vedo.Cylinder(pos=center, r=radius, height=height, axis=axis, **kwargs).legend(name)
    obj.name = name
    return obj

def visualize_sphere(sphere, **kwargs):
    center = sphere.center
    radius = sphere.radius
    name = str(sphere.center)
    obj = vedo.Sphere(pos=center, r=radius, **kwargs).legend(name)
    obj.name = name
    return obj

def visualize_supercell(SuperCell, **kwargs):
    objects = []
    for structure in SuperCell:
        if isinstance(structure, geo.Cylinder):
            objects.append(visualize_cylinder(structure, **kwargs))
        elif isinstance(structure, geo.Sphere):
            objects.append(visualize_sphere(structure, **kwargs))
    return objects




if __name__ == "__main__":
    cylinder1 = geo.Cylinder(center=(0,0,0), radius=.05, height=.2, axis=2)
    cylinder2 = geo.Cylinder(center=(0,0,0), radius=.05, height=.2, axis=1)
    cylinder3 = geo.Cylinder(center=(0,0,0), radius=.05, height=.2, axis=0)
    
    
    a1 = [0, 1, 1]
    a2 = [1, 0 ,1]
    a3 = [1, 1, 0]

    a_mag = 1


    geo_lattice = lat.Lattice(a1, a2, a3, magnitude = [a_mag, a_mag, a_mag])

    plot = visualize([cylinder1, cylinder2, cylinder3])

    cyl1 = vedo.Cylinder(r=.1, height=.2, axis=(1,0,0))
    cyl2 = vedo.Cylinder(r=.1, height=.2, axis=(0,0,1))

    combo = cyl1.boolean(operation="minus", mesh2 = cyl2, method=0)
    print(combo)
    plot2 = vedo.Plotter(shape=(1,1), axes=3)
    plot2.show(combo)
    # plot.show_cell(geo_lattice)
    
    
    # combine = plot.intersect_geometry()
    # print(combine)
    # plot2 = visualize([combine])


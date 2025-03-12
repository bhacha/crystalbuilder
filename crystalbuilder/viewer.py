import vedo
import crystalbuilder
import crystalbuilder.geometry as geo

vedo.settings.default_backend='vtk'


def visualize(structures, plotter_style=9, **kwargs):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    
    plot = vedo.Plotter(axes=plotter_style)


    for object in structures:
        
        if isinstance(object, geo.Cylinder):
            obj  = visualize_cylinder(object, **kwargs)
            plot += obj
        elif isinstance(object, geo.SuperCell):
            obj  = visualize_supercell(object, **kwargs)
            plot += obj
        elif isinstance(object, geo.Sphere):
            obj = visualize_sphere(object, **kwargs)
            plot += obj
            
    return plot

def add_to_visualizer(structures, plot, **kwargs):
    for object in structures:       
        if isinstance(object, geo.Cylinder):
            plot += visualize_cylinder(object, **kwargs)
        elif isinstance(object, geo.Sphere):
            plot += visualize_sphere(object, **kwargs)
        elif isinstance(object, geo.SuperCell):
            plot += visualize_supercell(object, **kwargs)


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
    cylinder1 = geo.Cylinder(center=(0,0,0), radius=1, height=3, axis=2)
    cylinder2 = geo.Cylinder(center=(5,5,0), radius=2, height=6, axis=1)
    visualize([cylinder1, cylinder2])
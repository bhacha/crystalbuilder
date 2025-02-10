import vedo
import crystalbuilder
import crystalbuilder.geometry as geo

vedo.settings.default_backend='vtk'


def visualize(structures, plotter_style=9):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    
    plot = vedo.Plotter(axes=plotter_style)


    for object in structures:
        
        if isinstance(object, geo.Cylinder):
            plot += visualize_cylinder(object)
        
        elif isinstance(object, geo.Sphere):
            plot += visualize_sphere(object)

        elif isinstance(object, geo.SuperCell):
            plot += visualize_supercell(object)


    plot.show().close()
    return plot

def visualize_cylinder(cylinder):
    center = cylinder.center
    radius = cylinder.radius
    height = cylinder.height
    axis = cylinder.axis
    return vedo.Cylinder(pos=center, r=radius, height=height, axis=axis)

def visualize_sphere(sphere):
    center = sphere.center
    radius = sphere.radius
    return vedo.Sphere(pos=center, r=radius)

def visualize_supercell(SuperCell):
    objects = []
    for structure in SuperCell:
        if isinstance(structure, geo.Cylinder):
            objects.append(visualize_cylinder(structure))
    return objects




if __name__ == "__main__":
    cylinder1 = geo.Cylinder(center=(0,0,0), radius=1, height=3, axis=2)
    cylinder2 = geo.Cylinder(center=(5,5,0), radius=2, height=6, axis=1)
    visualize([cylinder1, cylinder2])
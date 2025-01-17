import vedo
import crystalbuilder
import crystalbuilder.geometry as geo

vedo.settings.default_backend='vtk'


def visualize(structures):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    plot = vedo.Plotter(axes=2)


    for object in structures:

        if isinstance(object, geo.Cylinder):
            print("cylinder")
            plot += visualize_cylinder(object)


    plot.show().close()

def visualize_cylinder(cylinder):
    center = cylinder.center
    radius = cylinder.radius
    height = cylinder.height
    axis = cylinder.axis
    return vedo.Cylinder(pos=center, r=radius, height=height, axis=axis)



if __name__ == "__main__":
    cylinder1 = geo.Cylinder(center=(0,0,0), radius=1, height=3, axis=2)
    cylinder2 = geo.Cylinder(center=(5,5,0), radius=2, height=6, axis=1)
    visualize([cylinder1, cylinder2])
import crystalbuilder
import crystalbuilder.geometry as geo
from crystalbuilder.utils import TransformationMatrix as tmat
import trimesh as tm


def add_to_visualizer(structures, plot, **kwargs):
    for object in structures:       
        if isinstance(object, geo.Cylinder):
            plot.add_geometry(_visualize_cylinder(object, **kwargs))
        elif isinstance(object, geo.Sphere):
            plot.add_geometry(_visualize_sphere(object, **kwargs))
        elif isinstance(object, geo.SuperCell):
            plot.add_geometry(_visualize_supercell(object, **kwargs))


def visualize(structures, **kwargs):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    
    plot = tm.Scene()

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

def _visualize_cylinder(cylinder, **kwargs):
    center = cylinder.center
    radius = cylinder.radius
    height = cylinder.height
    axis = cylinder.axis
    transform = tmat.shift_and_rotate(new_position=center, axis_vector=axis)
    obj = tm.primitives.Cylinder(radius=radius, height=height, transform=transform, **kwargs)
    return obj

def _visualize_sphere(sphere, **kwargs):
    center = sphere.center
    radius = sphere.radius
    transform = tmat.shift_and_rotate(new_position=center, axis_vector=[0,0,1])
    obj = tm.primitives.Sphere(radius=radius, transform=transform, **kwargs)
    return obj

def _visualize_supercell(SuperCell, **kwargs):
    objects = []
    for structure in SuperCell:
        if isinstance(structure, geo.Cylinder):
            objects.append(_visualize_cylinder(structure, **kwargs))
        elif isinstance(structure, geo.Sphere):
            objects.append(_visualize_sphere(structure, **kwargs))
    return objects




if __name__ == "__main__":
    cylinder1 = geo.Cylinder(center=(0,1,0), radius=.5, height=3, axis=1)
    cylinder2 = geo.Cylinder(center=(0,0,0), radius=.5, height=6, axis=0)
    sphere = geo.Sphere(center=[1,1,1], radius=.25)
    plot=visualize([cylinder1, cylinder2, sphere])
    plot.show(viewer='gl')
    plot.strip_visuals()
import vedo
import crystalbuilder.geometry as geo
from crystalbuilder.utilities.utils import TransformationMatrix
from vedo import write

vedo.settings.default_backend='vtk'

class CustomScene(vedo.Plotter):
    
    def __init__(self, axes, **kwargs):
        super().__init__(self, axes, **kwargs)

def add_to_visualizer(structures, plot, **kwargs):
    try:
        for object in structures:       
            if isinstance(object, geo.Cylinder):
                plot += _visualize_cylinder(object, **kwargs)
            elif isinstance(object, geo.Sphere):
                plot += _visualize_sphere(object, **kwargs)
            elif isinstance(object, geo.Block):
                plot += _visualize_block(object, **kwargs)
            elif isinstance(object, geo.SuperCell):
                plot += _visualize_supercell(object, **kwargs)
            else:
                print(f"Error with type {type(object)}")
    except TypeError: # Raised if the input isn't a list
        print("Not a list, but I'll fix it")
        add_to_visualizer([structures], plot, **kwargs) #I'll put it in a list for you :)

def visualize(structures, plotter_style=3, **kwargs):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    
    plot = vedo.Plotter(axes=plotter_style)

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
    name = str(cylinder.center)
    obj = vedo.Cylinder(pos=center, r=radius, height=height, axis=axis, **kwargs).legend(name)
    obj.name = name
    return obj

def _visualize_sphere(sphere, **kwargs):
    center = sphere.center
    radius = sphere.radius
    name = str(sphere.center)
    obj = vedo.Sphere(pos=center, r=radius, **kwargs).legend(name)
    # obj.name = name
    return obj

def _visualize_supercell(SuperCell, **kwargs):
    objects = []
    for structure in SuperCell:
        if isinstance(structure, geo.Cylinder):
            objects.append(_visualize_cylinder(structure, **kwargs))
        elif isinstance(structure, geo.Sphere):
            objects.append(_visualize_sphere(structure, **kwargs))
        elif isinstance(structure, geo.Block):
            objects.append(_visualize_block(block, **kwargs))
    return objects

def _visualize_block(block,**kwargs):
    center = block.center
    size = block.extents
    # vectors = block.normalized_vecs
    # transform = TransformationMatrix.transform_in_place(origin=block.center, desired_vectors=vectors)
    obj = vedo.Box(pos=center, size=size)
    # obj.apply_transform(transform)
    return obj


    

if __name__ == "__main__":
    # cylinder1 = geo.Cylinder(center=(0,0,0), radius=1, height=3, axis=2)
    # cylinder2 = geo.Cylinder(center=(5,5,0), radius=2, height=6, axis=1)
    # visualize([cylinder1, cylinder2])
    block = geo.Block(center=[2,0,0], vectors=[[1,1,0], [0,1,1], [1,0,1]], size=[1,1,1])
    block2 = geo.Block(center=[10, 0, 0],vectors=[[1,1,0], [0,1,1], [1,0,1]], size=[1,1,1])
    plot = visualize([block, block2])
    plot.show(axes={"xrange":(0,5)} )
    geometry = plot.get_actors()
    print(geometry[0].bounds)
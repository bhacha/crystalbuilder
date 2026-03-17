from crystalbuilder.configuration import viewer_mode
from typing import Literal
from typing import TYPE_CHECKING
from crystalbuilder.utilities.utils import TransformationMatrix
import crystalbuilder.geometry as geo
import crystalbuilder.lattice 
from importlib import import_module
view_mode = viewer_mode


if view_mode == 'vedo':
    from crystalbuilder.viewers.vedo_viewer import *
   
elif view_mode == 'trimesh':
    from crystalbuilder.viewers.trimesh_viewer import *
    
else: 
    print("No view mode specified in config. Using Vedo.")
    from crystalbuilder.viewers.vedo_viewer import *


class Scene:
    """
    This will provide a somewhat standard interface for manipulating scenes, irrespective of viewer choice
    """
    
    def __init__(self,
                 backend,
                 **kwargs):
        if backend == 'trimesh':
            self.viewer = import_module("crystalbuilder.viewers.trimesh_viewer")
        else:
            self.viewer = import_module("crystalbuilder.viewers.vedo_viewer")

    def visualize(self, structure):
        plot = self.viewer.visualize(structure)
        return plot
    
    def output(self):
        pass
    

if __name__ == "__main__":
    import crystalbuilder.geometry as geo 
    tmshape = geo.Sphere(radius=1, center=[1,0,0])
    
    test = Scene(backend='trimesh')
    view = test.visualize([tmshape])
    view.show()
from crystalbuilder.configuration import viewer_mode as config_viewer_mode
from typing import Literal
from typing import TYPE_CHECKING
from crystalbuilder.utilities.utils import TransformationMatrix
import crystalbuilder.geometry as geo
import crystalbuilder.lattice 
from importlib import import_module

"""
This doesn't work and I don't know if there's a good way to have this module work as I want it to. It's imported immediately as part of importing CrystalBuilder, which means that it's imported with the default view_mode. 

If I take it out of the crystalbuilder __init__, then it's going to cause breaking changes in existing notebooks/code. That's worse than simply importing both and having to specify vedo.visualizer or whatever

"""

config_view_mode = config_viewer_mode
print(f"Viewer sees config as: {config_view_mode}")

if config_view_mode == 'vedo':
    from crystalbuilder.viewers.vedo_viewer import *
   
elif config_view_mode == 'trimesh':
    from crystalbuilder.viewers.trimesh_viewer import *
    
else: 
    print("No view mode specified in config. Using Vedo.")
    from crystalbuilder.viewers.vedo_viewer import *


class Scene:
    """
    This will provide a somewhat standard interface for manipulating scenes, irrespective of viewer choice
    """
    
    def __init__(self,
                 backend:Literal['vedo', 'trimesh'],
                 **kwargs):
        self.backend = backend
        
        if self.backend == 'trimesh':
            import trimesh
            self.viewer = import_module("crystalbuilder.viewers.trimesh_viewer")
        else:
            import vedo
            self.viewer = import_module("crystalbuilder.viewers.vedo_viewer")

    def visualize(self, structure):
        self.plot = self.viewer.visualize(structure)
        return self.plot
    
    def output(self,filename):
        """
        Output the scene to a series of OBJ files (Vedo) or a single STL (Trimesh)
        """
        new_filename = self.adjust_filename(filename)
        if self.backend == 'trimesh':
            import crystalbuilder.conversions.outputs as cbo
            cbo.merge_and_output(self.plot,new_filename)
        
        else:
            objects = self.plot.get_meshes()
            k=0
            for obj in objects:
                k+=1
                string=f"{new_filename}/object-{k}.obj"
                self.viewer.write(obj, string)

    
    def adjust_filename(self, filename:str):
        if filename.endswith((".stl", ".obj", "/")):
            filename = filename.removesuffix('/')
            filename = filename.split(".")[0]
        else:
            filename = filename       
        
        if self.backend == 'trimesh':
            filename = filename+'.stl'
        else:
            filename = filename
        return filename

    

# if __name__ == "__main__":
#     import crystalbuilder.geometry as geo 
#     tmshape = geo.Sphere(radius=1, center=[1,0,0])
    
#     test = Scene(backend='trimesh')
#     view = test.visualize([tmshape])
#     view.show()
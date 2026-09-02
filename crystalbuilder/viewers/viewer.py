from crystalbuilder.configuration import viewer_mode as config_viewer_mode
from typing import Literal
from typing import TYPE_CHECKING
from crystalbuilder.utilities.utils import TransformationMatrix
import crystalbuilder.geometry as geo
import crystalbuilder.lattice 
from importlib import import_module
import crystalbuilder.viewers.vedo_viewer as vv
import crystalbuilder.viewers.trimesh_viewer as tv

config_view_mode = config_viewer_mode


class WrapScene:
    def __init__(self, plot_object):
        self.plot = plot_object

    def show(self):
        return self.plot.show()
    
    def close(self):
        if type(self.plot).__name__ == 'Plotter':
            # print(type(self.plot).__name__)
            self.plot.close()
        else:
            # print(type(self.plot).__name__)
            pass
        

def visualize(structures, mode='vedo', **kwargs):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    if mode == 'trimesh':
        plot = tv.visualize(structures=structures)
        tv.add_to_visualizer(structures, plot)
    else:
        print(f"mode:{mode}")
        plot = vv.visualize(structures=structures, plotter_style=3, **kwargs)
        vv.add_to_visualizer(structures, plot, **kwargs)
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
    
    plot_object = WrapScene(plot)            
            
    return plot_object

def add_to_visualizer(structures, plot, **kwargs):
    if type(plot.plot).__name__ == 'Plotter':
        # print(type(plot).__name__)
        vv.add_to_visualizer(structures, plot.plot, **kwargs)
    else:
        # Only Vedo works right now for this.
        pass
        # print(type(plot).__name__)
    


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
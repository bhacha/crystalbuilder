from typing import Literal
from crystalbuilder.utilities.utils import TransformationMatrix as tmat
import crystalbuilder.conversions.trimesh_outputs as tmout
import crystalbuilder.geometry as geo, crystalbuilder.lattice as lattice
import logging
import warnings

logger = logging.getLogger(__name__)


try:
    import IPython.display as ipd
    ipd_found = True
except ModuleNotFoundError:
    ipd_found = False
    warnings.warn("IPython was not found. You may not be able to use all the visualization features.")
    

import vedo 
vedo.settings.default_backend='vtk'
import trimesh as tm
import trimesh.viewer.notebook as tmn
viewer_mode = 'vedo'

# def add_to_visualizer(structures, plot, **kwargs):
#     if type(plot.plot).__name__ == 'Plotter':
#         # print(type(plot).__name__)
#         vv.add_to_visualizer(structures, plot.plot, **kwargs)
#     else:
#         # Only Vedo works right now for this.
#         pass
#         # print(type(plot).__name__)
    

class TrimeshScene:
    def __init__(self, structures, **kwargs):
        self.plot = tm.Scene(**kwargs)
        self._make_plot(initial_structures=structures)
        
    def scene(self):
        return self.plot
    
    def show(self):
        if tmn.in_notebook() is not False and ipd_found is True:
            htmlscene = tmn.scene_to_notebook(self.plot)
            ipd.display(htmlscene) #type:ignore #The ipd_found flag ensures that this only runs if ipd is bound
        else:
            self.plot.show()
    
    def close(self):
        """ Trimesh has no close function, just close the window"""
        pass
        
    def _make_plot(self, initial_structures, **kwargs):
        self.add_to_visualizer(initial_structures)
        
    def add_to_visualizer(self, structures, **kwargs):
        for object in structures:       
            if isinstance(object, geo.Cylinder):
                self.plot.add_geometry(self._visualize_cylinder(object, **kwargs))
            elif isinstance(object, geo.Sphere):
                self.plot.add_geometry(self._visualize_sphere(object, **kwargs))
            elif isinstance(object, geo.Block):
                self.plot.add_geometry(self._visualize_block(object, **kwargs))
            elif isinstance(object, geo.SuperCell):
                self.plot.add_geometry(self._visualize_supercell(object, **kwargs))
            else:
                print(f"Object of type {type(object)} not currently supported for visualizing in Trimesh with CrystalBuilder.")
    
    def output(self,filename):
        """
        Output the scene to a series of OBJ files (Vedo) or a single STL (Trimesh)
        """
        new_filename = self.adjust_filename(filename)
        tmout.merge_and_output(self.plot,new_filename)
             
    def adjust_filename(self, filename:str):
        if filename.endswith((".stl", ".obj", "/")):
            filename = filename.removesuffix('/')
            filename = filename.split(".")[0]
        else:
            filename = filename

        filename = filename+'.stl'
        return filename

    def _visualize_cylinder(self, cylinder:geo.Cylinder, **kwargs):
        center = cylinder.center
        radius = cylinder.radius
        height = cylinder.height
        axis = cylinder.axis
        transform = tmat.shift_and_rotate(new_position=center, axis_vector=axis)
        obj = tm.primitives.Cylinder(radius=radius, height=height, transform=transform, sections=8, **kwargs)
        return obj

    def _visualize_sphere(self, sphere:geo.Sphere, **kwargs):
        center = sphere.center
        radius = sphere.radius
        transform = tmat.shift_and_rotate(new_position=center, axis_vector=[0,0,1])
        obj = tm.primitives.Sphere(radius=radius, transform=transform, **kwargs)
        return obj

    def _visualize_block(self, block:geo.Block, **kwargs):
        center = block.center
        extents = block.extents
        vectors = block.normalized_vecs
        linear_transform = tmat.transform(vectors)
        translate = tmat.shift_to(new_position=center)
        transform = translate @ linear_transform
        obj = tm.primitives.Box(extents=extents, transform=transform, **kwargs)
        return obj

    def _visualize_supercell(self, supercell: geo.SuperCell, **kwargs):
        objects = []
        for structure in supercell:
            if isinstance(structure, geo.Cylinder):
                objects.append(self._visualize_cylinder(structure, **kwargs))
            elif isinstance(structure, geo.Sphere):
                objects.append(self._visualize_sphere(structure, **kwargs))
            elif isinstance(structure, geo.Block):
                objects.append(self._visualize_block(structure, **kwargs))
            else:
                print(f"Object of type {type(structure)} not currently supported for visualizing in Trimesh with CrystalBuilder.")
        return objects

class VedoScene:
    
    def __init__(self, structures, **kwargs): 
        plotter_style = kwargs.get("plotter_style", 3)
        self.plot = vedo.Plotter(axes=plotter_style)
        self.add_to_visualizer(structures, **kwargs)
    
    def scene(self):
        return self.plot
    
    def show(self):
        self.plot.show()
    
    def close(self):
        self.plot.close()
                
    def add_to_visualizer(self, structures, **kwargs):
        try:
            for object in structures:       
                if isinstance(object, geo.Cylinder):
                    self.plot += self._visualize_cylinder(object, **kwargs)
                elif isinstance(object, geo.Sphere):
                    self.plot += self._visualize_sphere(object, **kwargs)
                elif isinstance(object, geo.Block):
                    self.plot += self._visualize_block(object, **kwargs)
                elif isinstance(object, geo.SuperCell):
                    self.plot += self._visualize_supercell(object, **kwargs)
                else:
                    print(f"Error with type {type(object)}")
        except TypeError: # Raised if the input isn't a list
            print("Not a list, but I'll fix it")
            self.add_to_visualizer([structures], **kwargs) #I'll put it in a list for you :)
        
    def _visualize_cylinder(self, cylinder:geo.Cylinder, **kwargs):
        center = cylinder.center
        radius = cylinder.radius
        height = cylinder.height
        axis = cylinder.axis
        name = str(cylinder.center)
        obj = vedo.Cylinder(pos=center, r=radius, height=height, axis=axis, **kwargs).legend(name)
        obj.name = name
        return obj

    def _visualize_sphere(self, sphere:geo.Sphere, **kwargs):
        center = sphere.center
        radius = sphere.radius
        name = str(sphere.center)
        obj = vedo.Sphere(pos=center, r=radius, **kwargs).legend(name)
        # obj.name = name
        return obj

    def _visualize_block(self, block:geo.Block, **kwargs):
        center = block.center
        size = block.extents
        # vectors = block.normalized_vecs
        # transform = TransformationMatrix.transform_in_place(origin=block.center, desired_vectors=vectors)
        obj = vedo.Box(pos=center, size=size)
        # obj.apply_transform(transform)
        return obj

    def _visualize_supercell(self, supercell:geo.SuperCell, **kwargs):
        objects = []
        for structure in supercell:
            if isinstance(structure, geo.Cylinder):
                objects.append(self._visualize_cylinder(structure, **kwargs))
            elif isinstance(structure, geo.Sphere):
                objects.append(self._visualize_sphere(structure, **kwargs))
            elif isinstance(structure, geo.Block):
                objects.append(self._visualize_block(structure, **kwargs))
            else:
                print(f"Object of type {type(structure)} not currently supported for visualizing in Vedo with CrystalBuilder.")
        return objects

    # def output(self,filename):
    #         """
    #         Output the scene to a series of OBJ files (Vedo)
    #         """
    #         new_filename = self.adjust_filename(filename)
    #         if self.backend == 'trimesh':
    #             import crystalbuilder.conversions.trimesh_outputs as cbo
    #             cbo.merge_and_output(self.plot,new_filename)
            
    #         else:
    #             objects = self.plot.get_meshes()
    #             k=0
    #             for obj in objects:
    #                 k+=1
    #                 string=f"{new_filename}/object-{k}.obj"
    #                 self.viewer.write(obj, string)

        
    #     def adjust_filename(self, filename:str):
    #         if filename.endswith((".stl", ".obj", "/")):
    #             filename = filename.removesuffix('/')
    #             filename = filename.split(".")[0]
    #         else:
    #             filename = filename       
            
    #         if self.backend == 'trimesh':
    #             filename = filename+'.stl'
    #         else:
    #             filename = filename
    #         return filename

def build_scene(backend:Literal['vedo', 'trimesh'], structures, **kwargs):
    if backend == 'vedo':
        return VedoScene(structures=structures, **kwargs)
    elif backend == 'trimesh':
        return TrimeshScene(structures=structures, **kwargs)
    else:
        pass

def visualize(structures, **kwargs):
    return VedoScene(structures=structures, **kwargs)

        

if __name__ == "__main__":
    import crystalbuilder.geometry as geo 
    tmshape = geo.Sphere(radius=1, center=[1,0,0])
    scene = build_scene(backend='trimesh',structures=[tmshape])
    scene.show()
    # scene.close()
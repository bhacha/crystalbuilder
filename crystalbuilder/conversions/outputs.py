import trimesh as tm
import numpy as np
from matplotlib import pyplot as plt

def merge_and_output(scene, filename):
    """
    Merge meshes in trimesh scene and output them to an STL file
    
    Parameters
    ----------
    scene : tm.Scene
        Trimesh scene with objects
    
    filename : str
        Name of file to be saved, you must include stl suffix!
    
    """
    merged_geometry = merge_geometry(scene)
    output_to_stl(merged_geometry, filename)

def merge_geometry(scene):
    """
    Merge meshes in scene
    
    Parameters
    ----------
    scene : tm.Scene
        Trimesh scene with objects
        
    Returns
    -------
    Trimesh.mesh
        combined structures
        
    """
    geometry = scene.dump()
    combined = tm.boolean.boolean_manifold(meshes=geometry, operation='union')
    return combined
    
def output_to_stl(mesh, filename):
    """
    Outputs mesh to STL file
    
    Parameters
    ----------
    filename : str
        Name of file to be saved, you must include stl suffix!
    
    """
    mesh.export(filename)
    
def output_scene_to_model(scene, output_filename):
    """
    Create mesh from scene. This does not perform any Boolean operations
    
    Parameters
    ----------
    scene : tm.Scene
        Trimesh scene with objects
    
    filename : str
        Name of file to be saved, you must include stl suffix!
    
    
    """
    newmesh = scene.to_mesh()
    newmesh.export(output_filename)
    



if __name__ == "__main__":
    
    block = tm.primitives.Box([1,1,1])
    sphere = tm.primitives.Sphere(radius=.5, center=[.5,.5,0])
    collection = [block, sphere]
    # collection = tm.boolean.boolean_manifold([block, sphere], operation='union')
    scene = tm.Scene()
    scene.add_geometry(collection)
    print(scene.dump())
    # newmesh = scene.to_mesh()
    # newmesh.export("TestMesh2.stl")
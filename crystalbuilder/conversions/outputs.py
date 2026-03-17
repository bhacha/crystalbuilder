import trimesh as tm
import numpy as np
from matplotlib import pyplot as plt




def merge_and_output(scene, filename):
    merged_geometry = merge_geometry(scene)
    output_to_stl(merged_geometry, filename)


def merge_geometry(scene):
    geometry = scene.dump()
    combined = tm.boolean.boolean_manifold(meshes=geometry, operation='union')
    return combined
    
def output_to_stl(mesh, filename):
    mesh.export(filename)
    
def output_scene_to_model(scene, output_filename):
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
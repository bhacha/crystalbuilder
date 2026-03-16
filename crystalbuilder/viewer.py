from .configuration import viewer_mode

view_mode = viewer_mode


if view_mode == 'vedo':
    from crystalbuilder.view_modes.vedo_viewer import *
   
elif view_mode == 'trimesh':
    from crystalbuilder.view_modes.trimesh_viewer import *
    
else: 
    print("No view mode specified in config. Using Vedo.")
    from crystalbuilder.view_modes.vedo_viewer import *


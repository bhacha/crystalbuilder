from typing import Literal
viewer_mode = 'vedo' #'vedo' or 'trimesh'


def set_viewer_mode(value:Literal["trimesh", "vedo"]):
    global viewer_mode
    viewer_mode = value
    
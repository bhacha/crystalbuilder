from crystalbuilder import convert
from crystalbuilder import lattice
from crystalbuilder import vectors
from crystalbuilder import bilbao
import trimesh
import vedo
import numpy as np
import numpy.typing as npt


def MonkhorstPack(size):
    """
    This is a direct copy of the Monkhorst-Pack k-space sampling method in ase (https://iopscience.iop.org/article/10.1088/1361-648X/aa680e)
    
    This way there's no need to import ase. 

    Parameters
    ----------
    size : ndarray
        number of points (kx, ky, kz) to sample reciprocal space. This should only be used in MPB, as it performs the necessary multiplication by the reciprocal lattice vectors 

    """
    if np.less_equal(size, 0).any():
        raise ValueError(f'Illegal size: {list(size)}')
    kpts = np.indices(size).transpose((1, 2, 3, 0)).reshape((-1, 3))
    return (kpts + 0.5) / size - 0.5

class TransformationMatrix:
    """
    A class representing a 4x4 transformation matrix. It initializes as an identity matrix, and the plan is to include various methods for defining the elements.
    
    No translations should be handled by this class, the 4x4 shape is just to ensure compatibility with Trimesh or other programs that use a full 4x4.
    
    """
    def __init__(self) -> None:
        
        eyemat = np.identity(3) #3x3 matrix for rotations
        
        
        self.tmat = np.pad(eyemat, (0, 1)) #pad to 4x4 after rotations are defined
        self.tmat[3,3] = 1 #Set the translation component to 1 (no translations should be handled by this matrix)
        
        
       

    @classmethod
    def rotate_to(cls, axis_vector, initial_vector=[0,0,1]):
        """
        Normalize an input axis vector, then create a rotation matrix that takes [0,0,1] (default) into that vector. This uses a matrix notation of Rodrigues's Rotation Formula.
        """
        orientation = np.asarray(axis_vector)/np.linalg.norm(axis_vector) #normalize desired axis
        v1 = np.asarray(initial_vector)/np.linalg.norm(initial_vector) #normalize current vector
        
  
        rot_axis_unnorm = np.cross(v1, orientation) #take the cross product to find the axis of rotation
        sin_theta = rot_axis_unnorm #Since our vectors are length 1, sine of theta is simply their cross product.
        cos_theta = np.dot(v1, orientation) # Similarly, the value of cosine theta is the dot product
        
        rot_axis = rot_axis_unnorm/np.linalg.norm(rot_axis_unnorm) #Normalize axis of rotation (probably unnecessary, but computationally cheaper than worrying about possible edge cases)
        
        skew_mat = np.array(
        ((0, -rot_axis[2], rot_axis[1]), 
        (rot_axis[2], 0, -rot_axis[0]), 
        (-rot_axis[1], rot_axis[0], 0))
    )
        eyemat = np.identity(3)   
        rot_mat = eyemat + (sin_theta * skew_mat) + ((1-cos_theta)*(skew_mat@skew_mat))
        rot_mat = np.pad(rot_mat, (0,1)).round(decimals=4)
        rot_mat[3,3] = 1
        return rot_mat

        

if __name__ == "__main__":
    
    tmat = TransformationMatrix.rotate_to([1,0,0])
    cyl1 = trimesh.primitives.Cylinder(radius=1, height=1)
    cylinder = trimesh.primitives.Cylinder(radius=1, height=1)
    cylinder.apply_transform(tmat)
    
    # print(tmat.shape)
    # print(tmat)
    # print(cylinder.direction)
    cylinder.show(viewer='gl')
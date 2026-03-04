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
    
    The 4x4 shape is to ensure compatibility with Trimesh or other programs that use a full 4x4. Rotations and Translations should still be passed separately.
    
    """
    
    def _check_same(value1, value2):
        val1_arr = np.asarray(value1)
        val2_arr = np.asarray(value2)
        if np.array_equiv(val1_arr, val2_arr):
            print(f"{val1_arr} is the same as {val2_arr}; No rotating performed.")
            return True
        else:
            return False
    
    def __init__(self) -> None:
        
        eyemat = np.identity(3) #3x3 matrix for rotations
        
        
        self.tmat = np.pad(eyemat, (0, 1)) #pad to 4x4 after rotations are defined
        self.tmat[3,3] = 1 #Set the 4,4 element to 1
        
        
    @classmethod
    def shift_and_rotate(cls, new_position, axis_vector, initial_axis = [0,0,1], initial_position=[0,0,0]):
        rotmat = cls.rotate_to(axis_vector=axis_vector, initial_vector=initial_axis)   
        transmat = cls.shift_to(new_position=new_position, initial_position=initial_position)
        combined_mat = np.matmul(transmat, rotmat)
        return combined_mat
        
    @classmethod
    def rotate_to(cls, axis_vector, initial_vector=[0,0,1]):
        """
        Normalize an input axis vector, then create a rotation matrix that takes [0,0,1] (default) into that vector. This uses a matrix notation of Rodrigues's Rotation Formula.
        """
        if cls._check_same(axis_vector, initial_vector):
            # print("same")
            return np.identity(4, dtype=float)
        else:
            orientation = np.asarray(axis_vector)/np.linalg.norm(axis_vector) #normalize desired axis
            v1 = np.asarray(initial_vector)/np.linalg.norm(initial_vector) #normalize current vector
            
    
            rot_axis_unnorm = np.cross(v1, orientation) #take the cross product to find the axis of rotation
            sin_theta = np.linalg.norm(rot_axis_unnorm) #Since our vectors are length 1, sine of theta is simply the magnitude of their cross product.
            cos_theta = np.dot(v1, orientation) # Similarly, the value of cosine theta is the dot product

            
            rot_axis = rot_axis_unnorm/np.linalg.norm(rot_axis_unnorm) #Normalize axis of rotation (probably unnecessary, but computationally cheaper than worrying about possible edge cases)

            
            skew_mat = np.array(
            ((0, -rot_axis[2], rot_axis[1]), 
            (rot_axis[2], 0, -rot_axis[0]), 
            (-rot_axis[1], rot_axis[0], 0))
            )
            eyemat = np.identity(3, dtype=float)   

            rot_mat = eyemat + (sin_theta* skew_mat) + ((1-cos_theta)*(skew_mat@skew_mat))

            rot_mat = np.pad(rot_mat, (0,1))
            rot_mat[3,3] = 1.0
            
            return rot_mat

    @classmethod
    def shift_to(cls, new_position, initial_position=[0,0,0]):
        
        eyemat = np.identity(3) #3x3 matrix for rotations
        
        tmat = np.pad(eyemat, (0, 1)) #pad to 4x4 after rotations are defined
        tmat[3,3] = 1 #Set the 4,4 element to 1
        
        tmat[0, 3] = new_position[0]
        tmat[1, 3] = new_position[1]
        tmat[2, 3] = new_position[2]
        return tmat


if __name__ == "__main__":
       
    tmat = TransformationMatrix.rotate_to([1,0,0])
    transmat = TransformationMatrix.shift_to([1,1,1])
    # print(f"Rotation: \n{tmat}")
    # print(f"Translation: \n {transmat}")
    combined = np.matmul(transmat, tmat)
    
    # combmat = TransformationMatrix.shift_and_rotate(new_position=[0,0,0], axis_vector=[1,0,0])

    # cyl1 = trimesh.primitives.Cylinder(radius=1, height=1)
    # cylinder = trimesh.primitives.Cylinder(radius=1, height=1)
    # cylinder.apply_transform(tmat)

    
    
    # print(tmat.shape)
    # print(tmat)
    # print(cylinder.direction)
    # cylinder.show(viewer='gl')
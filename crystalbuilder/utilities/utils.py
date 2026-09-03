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
            #print(f"{val1_arr} is the same as {val2_arr}; No rotating performed.")
            return True
        else:
            return False
    
    def __init__(self, transformation_matrix) -> None:
        
        self.tmat = transformation_matrix
    
       
        
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
        
        tmat[0, 3] = new_position[0]-initial_position[0]
        tmat[1, 3] = new_position[1]-initial_position[1]
        tmat[2, 3] = new_position[2]-initial_position[2]
        return tmat

    @classmethod
    def transform(cls, desired_vectors:npt.NDArray|list, initial_vectors:npt.NDArray|list =[[1,0,0], [0,1,0], [0,0,1]]):
        """
        This should orient and shear a rectangle to make the desired parallelepiped. In creating this I realized that my other methods are way overengineered...
        
        I already know the resulting vector, so I don't need anything like the Rodrigues formula when I can just solve MA=B -> M = BA^-1 to find the transformation matrix M. 
        
        """
        initial_vec_array = np.zeros((4,4))
        final_vec_array = np.zeros((4,4))
        for number, vector in enumerate(initial_vectors):
            initial_vec_array[:3, number] = np.asarray(vector)[:3]
        
        for number, vector in enumerate(desired_vectors):
            final_vec_array[:3, number] = np.asarray(vector)[:3]

        initial_vec_array[3,3] = final_vec_array[3,3] = 1

        tmat = final_vec_array @ np.linalg.inv(initial_vec_array)
        return tmat
    
    @classmethod
    def transform_in_place(cls, origin, desired_vectors:npt.NDArray|list, initial_vectors:npt.NDArray|list =[[1,0,0], [0,1,0], [0,0,1]]):
        """
        This corrects any weirdness that occurs when transforming an object that's away from the global origin (0,0,0)
        """
        object_origin_position = np.asarray(origin)
        shiftmat1 = cls.shift_to([0,0,0], object_origin_position)
        transform_mat = cls.transform(desired_vectors=desired_vectors, initial_vectors=initial_vectors)
        shiftmat2 = cls.shift_to(new_position=object_origin_position, initial_position=[0,0,0])
        tmat = shiftmat2 @ (transform_mat @ shiftmat1)
        # print(f"Transformation Matrix Info: \n Determinant: {np.linalg.det(tmat)}")
        # print(f"Shift Matrix 1: \n {shiftmat1} \n Shift Matrix 2: \n {shiftmat1} \n \n Final Transformation Matrix: \n {tmat}")
        return tmat


if __name__ == "__main__":
       
    desired_a = [[1,1,0], [0,1,1], [1,0,1], [0,0,0]]
    
    newmat = TransformationMatrix.transform(desired_vectors=desired_a)
    print(newmat)
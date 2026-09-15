import numpy as np
from numpy._typing._array_like import NDArray
import crystalbuilder.utilities.cb_types as cbt
from crystalbuilder.utilities.cb_types import Number, VectorSet, VectorType, AngleUnits, AxisType, Iterable
import logging

logger = logging.getLogger(__name__)

rounder = 50 #sets decimal rounding
#Needs Done

def flatten(list: list) -> list:
    flat_list = [item for sublist in list for item in sublist]
    return flat_list

def angle_check(theta:Number, unit:AngleUnits) -> float:
    if unit == 'degrees' or 'deg' or 'd' or 'degree':
        radthet = float(np.radians(theta))
    elif unit == 'radians' or 'rad' or 'r' or 'radian':    
        radthet = float(theta)
    else:
        print("Error: Units must be 'degrees' or 'radians'")
        return 0
    return radthet

def shift(point:VectorType, shift_vector:VectorType) -> NDArray:
    """
    TO DO

    shift point by the shift vector
    """
    point_arr = np.asarray(point)
    shiftvec = np.asarray(shift_vector)
    shiftedpoint = point_arr.reshape(3,) + shiftvec.reshape(3,)
    return shiftedpoint

def get_shift_vector(point:VectorType, newpoint:VectorType) -> NDArray:
    point_arr = np.asarray(point)
    newpoint = np.asarray(newpoint)
    shiftvec = newpoint.reshape(3,) - point_arr.reshape(3,)
    return shiftvec

def shift_angle(point:VectorType, theta:Number, distance:Number, unit: AngleUnits='degrees'):
    """
    Shifts in x-y plane a distance at angle theta
    """
    point_arr = np.asarray(point)
    shiftvec = np.asarray(rotate([[distance, 0, 0]], theta, axis=2, unit=unit))
    shiftedpoint = point_arr.reshape(3,) + shiftvec.reshape(3,)
    return shiftedpoint

def rotate(point:VectorType, theta:Number, relative_point:VectorType =(0,0,0), axis: AxisType = 2, unit: AngleUnits='degrees', toarray:bool=True) -> VectorType|VectorSet:
    """
    rotates counterclockwise a point or list of points about relative_point by theta in
    This does a 2D rotation only, so string a few together to rotate in more than one axis

    Parameters:
        point (list of array_like)
        theta (float)
        relative_point (array_like)
        axis (0,1,2)
        unit (str): 'degrees' or 'radians'

    Returns:
        List of coordinate lists (3-list)

    """

    radthet = angle_check(theta, unit)


    coordinatelist = []
    
    if radthet == None: return np.array([0,0,0])
    for coord in point:

        if axis==2:
            newcoord = rotatez(coord, radthet, relative_point)
            
        elif axis ==1:
            newcoord = rotatey(coord, radthet, relative_point)
            
        elif axis ==0:
            newcoord = rotatex(coord, radthet, relative_point)
            
        else:
            print("Error: Check Axis Direction")
            return np.array([0,0,0])
        
        newcoord = np.asarray(newcoord).reshape(3,).tolist()
        coordinatelist.append(newcoord)
        if toarray==False: 
            new_coordinates=coordinatelist
        else:
            new_coordinates=np.asarray(coordinatelist)
        
        logger.debug(f"coordinates: {new_coordinates} \n type: {type(new_coordinates)} \n data type: {type(new_coordinates[0][0])}")


    return new_coordinates 

def rotatex(point:VectorType, theta:Number, relative_point:VectorType) -> NDArray:
    """
    rotates counterclockwise a point in x by theta radians about relative_point
    """
    x = point[0]
    y = point[1]
    z = point[2]

    relx = relative_point[0]
    rely = relative_point[1]
    relz = relative_point[2]

    tmat = np.array([
                    [1,0,0,0],
                    [0, 1, 0, 0],
                    [0,0,1,0],
                    [relx, rely, relz,1]])
    
    tnmat = np.array([
                    [1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [-relx, -rely, -relz, 1]])

    rxmat = np.array([
                    [1, 0, 0, 0],
                    [0, np.cos(theta), -np.sin(theta), 0], 
                    [0, np.sin(theta), np.cos(theta), 0],
                    [0,0,0,1]
                    ]).round(rounder)
    logger.debug(f"rxmat= {rxmat}")

    rt1mat = np.matmul(rxmat,tnmat)
    logger.debug(f"rt1mat = {rt1mat}")

    rt2mat = np.matmul(tmat,rt1mat)
    logger.debug(f"rt2mat = {rt2mat}")
    
    rotation = np.matmul(rt2mat, np.array([[x],[y],[z],[1]]))
    return rotation[:3]

def rotatey(point:VectorType, theta:Number, relative_point:VectorType) -> NDArray:
    """
    rotates counterclockwise a point in y by theta radians about relative_point
    """
    x = point[0]
    y = point[1]
    z = point[2]

    relx = relative_point[0]
    rely = relative_point[1]
    relz = relative_point[2]

    tmat = np.array([
                    [1,0,0,0],
                    [0, 1, 0, 0],
                    [0,0,1,0],
                    [relx, rely, relz,1]])
    
    tnmat = np.array([
                    [1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [-relx, -rely, -relz, 1]])

    rymat = np.array([
                    [np.cos(theta), 0, np.sin(theta), 0],
                    [0, 1, 0, 0], 
                    [-np.sin(theta), 0, np.cos(theta), 0],
                    [0,0,0,1]
                    ]).round(rounder)
    
    logger.debug(f"rymat= {rymat}")

    rt1mat = np.matmul(rymat,tnmat)
    logger.debug(f"rt1mat = {rt1mat}")

    rt2mat = np.matmul(tmat,rt1mat)
    logger.debug(f"rt2mat = {rt2mat}")
    
    rotation = np.matmul(rt2mat, np.array([[x],[y],[z],[1]]))
    return rotation[:3]

def rotatez(point:VectorType, theta:Number, relative_point:VectorType) -> NDArray:
    """
    rotates counterclockwise a point in z by theta radians about relative_point
    """
    x = point[0]
    y = point[1]
    z = point[2]

    relx = relative_point[0]
    rely = relative_point[1]
    relz = relative_point[2]

    tmat = np.array([
                    [1,0,0,relx],
                    [0,1,0,rely],
                    [0,0,1,relz],
                    [0,0,0,1]])
    
    
    tnmat = np.array([
                    [1,0,0,-relx],
                    [0,1,0,-rely],
                    [0,0,1,-relz],
                    [0,0,0,1]])

    rzmat = np.array([
                    [np.cos(theta), -np.sin(theta),0 , 0],
                    [np.sin(theta), np.cos(theta), 0, 0], 
                    [0, 0, 1, 0],
                    [0,0,0,1]
                    ]).round(rounder)
    logger.debug(f"translation matrix = {tmat} \n negative translation matrix = {tnmat} \n rzmat = {rzmat}")

        

    rt1mat = np.matmul(rzmat,tnmat)
    logger.debug(f"rt1mat = {rt1mat}")

    rt2mat = np.matmul(tmat,rt1mat)
    logger.debug(f"rt2mat = {rt2mat}")
    
    rotation = np.matmul(rt2mat, np.array([[x],[y],[z],[1]]))
    return rotation[:3]

def basis_change(basis1:VectorType|cbt.Literal['cartesian'], basis2:VectorType|cbt.Literal['cartesian'], point_in_basis1) -> NDArray:
    """
    makes column vectors from basis1 and basis2, then determines the change-of-basis matrix. Applies this to specified point and returns the coordinate in the other basis.

    Both bases need to be defined in cartesian basis, but the output will be in terms of basis2


    Parameters
    ----------
    basis1: basis in 3x3 list or array, or 'cartesian'
    basis2: basis in 3x3 list or array, or 'cartesian'
    point_in_basis1: 3-list point specified in units of basis 1

    """
    cartbasis = [[1,0,0], [0,1,0], [0,0,1]]
    try: 
        if basis1 == 'cartesian': basis1=cartbasis
    except ValueError:
        pass
    
    try: 
        if basis2 == 'cartesian': basis2=cartbasis
    except ValueError:
        pass
    
    
    bas1_arr = np.transpose(np.asarray(basis1))
    bas2_arr = np.transpose(np.asarray(basis2))
    point_arr = np.asarray(point_in_basis1).reshape(3,1)

    newpoint = np.matmul(bas1_arr, point_arr)
    outpoint = np.matmul(bas2_arr, newpoint)
    return outpoint.reshape(3,)

def cart_to_pol(point:VectorType) -> list:
    x = point[0]
    y = point[1]
    z = point[2]
    r = np.sqrt((x**2 + y**2))
    theta = np.arctan2(y, x)+np.pi
    return [r, theta, z]

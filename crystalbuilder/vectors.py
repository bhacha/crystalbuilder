import numpy as np
from matplotlib import pyplot as plt

debug = 'off'

rounder = 50 #sets decimal rounding
#Needs Done


def flatten(list):
    flat_list = [item for sublist in list for item in sublist]
    return flat_list

def angle_check(theta, unit):
    if unit == 'degrees' or 'deg' or 'd' or 'degree':
        radthet = np.radians(theta)
    elif unit == 'radians' or 'rad' or 'r' or 'radian':    
        radthet = theta
    else:
        print("Error: Units must be 'degrees' or 'radians'")
    return radthet

def shift(point, shift_vector):
    """
    TO DO

    shift point by the shift vector
    """
    point_arr = np.asarray(point)
    shiftvec = np.asarray(shift_vector)
    shiftedpoint = point_arr.reshape(3,) + shiftvec.reshape(3,)
    return shiftedpoint

def get_shift_vector(point, newpoint):
    point_arr = np.asarray(point)
    newpoint = np.asarray(newpoint)
    shiftvec = newpoint.reshape(3,) - point_arr.reshape(3,)
    return shiftvec

def shift_angle(point, theta, distance, unit='degrees'):
    """
    Shifts in x-y plane a distance at angle theta
    """
    point_arr = np.asarray(point)
    shiftvec = rotate([[distance, 0, 0]], theta, axis=2, unit=unit)
    print(shiftvec.T)
    print(point_arr)
    shiftedpoint = point_arr.reshape(3,) + shiftvec.reshape(3,)
    return shiftedpoint

def rotate(point, theta, relative_point=(0,0,0), axis=2, unit='degrees', toarray=True):
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
    

    for coord in point:

        if axis==2:
            newcoord = rotatez(coord, radthet, relative_point)
            
        elif axis ==1:
            newcoord = rotatey(coord, radthet, relative_point)
            
        elif axis ==0:
            newcoord = rotatex(coord, radthet, relative_point)
            
        else:
            print("Error: Check Axis Direction")
        
        newcoord = newcoord.reshape(3,).tolist()
        coordinatelist.append(newcoord)
        if toarray==False: 
            new_coordinates=coordinatelist
        else:
            new_coordinates=np.asarray(coordinatelist)
        
        if debug == 'on':
            print('coordinates=\n', new_coordinates)
            print('type= ', type(new_coordinates))
            print('data type= ', type(new_coordinates[0][0]))


    return new_coordinates

def rotatex(point, theta, relative_point):
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
    if debug=='on':
        print("rxmat", '= ', rxmat)

    rt1mat = np.matmul(rxmat,tnmat)
    if debug=='on':
        print("rt1mat", '= ', rt1mat)

    rt2mat = np.matmul(tmat,rt1mat)
    if debug=='on':
        print("rt2mat", '= ', rt2mat)
    
    rotation = np.matmul(rt2mat, np.array([[x],[y],[z],[1]]))
    return rotation[:3]

def rotatey(point, theta, relative_point):
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
    if debug=='on':
        print("rymat", '= ', rymat)

    rt1mat = np.matmul(rymat,tnmat)
    if debug=='on':
        print("rt1mat", '= ', rt1mat)

    rt2mat = np.matmul(tmat,rt1mat)
    if debug=='on':
        print("rt2mat", '= ', rt2mat)
    
    rotation = np.matmul(rt2mat, np.array([[x],[y],[z],[1]]))
    return rotation[:3]

def rotatez(point, theta, relative_point):
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
    if debug=='on':
        print("translation matrix = \n", tmat)
        print("negative translation matrix = \n", tnmat)
        print("rzmat", '=\n', rzmat)
        

    rt1mat = np.matmul(rzmat,tnmat)
    if debug=='on':
        print("rt1mat", '=\n', rt1mat)

    rt2mat = np.matmul(tmat,rt1mat)
    if debug=='on':
        print("rt2mat", '=\n', rt2mat)
    
    rotation = np.matmul(rt2mat, np.array([[x],[y],[z],[1]]))
    return rotation[:3]

def basis_change(basis1, basis2, point_in_basis1):
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

def cart_to_pol(point):
    x = point[0]
    y = point[1]
    z = point[2]
    r = np.sqrt((x**2 + y**2))
    theta = np.arctan2(y, x)+np.pi
    return [r, theta, z]

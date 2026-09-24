
import re
import os
location = os.path.dirname(os.path.realpath(__file__))
resources = os.path.join(location, 'resources')
import requests
import numpy as np
from bs4 import BeautifulSoup
import json
import crystalbuilder.utilities.cb_types as cbt    
import logging

baselogger = logging.getLogger(__name__)
class LatticeAdapter(logging.LoggerAdapter):
    
    def process(self, msg, kwargs):
        return f'{self.extra['prefix']} - {msg}', kwargs # pyright: ignore[reportOptionalSubscript]

logger = LatticeAdapter(baselogger, {'prefix':"bilbao.py"})

bilbao_url = "https://cryst.ehu.es/"

cookie_dict = {"turnstile_passed": '1767991980'} #filler cookie. Should be set with _get_spacegroups()

def _set_turnstile_cookie(cookie):
    formatted_cookie = str(cookie)
    global cookie_dict
    cookie_dict = {"turnstile_passed": formatted_cookie}
    
def _check_turnstile_cookie():
    URL = bilbao_url+"cgi-bin/cryst/programs/nph-kv-list"
    page = requests.post(URL, data={'gnum': str(1),'standard':'Optimized listing of k-vector types using ITA description'}, cookies=cookie_dict)
    soup = BeautifulSoup(page.content, "html.parser") # type: ignore
    kvec_table = soup.find_all('table')[1]
    rows = kvec_table('tr')[2:]
    raw_kvec_dict = {}

def download_all_spacegroup_data(cookie=None, force_redownload=False):
    _get_spacegroups(cookie, 'all', force_redownload=force_redownload)
    

def _get_spacegroups(cookie, spacegroup, **kwargs):
    """
    This should not be used in a regular import scenario. This scrapes data from the Bilbao server to create offline resource files, but only works with a cookie obtained after passing a Cloudflare DDOS protection. It will fail if run without configuring that.
    """
    
    force_redownload = kwargs.get("force_redownload", False)
    
    if cookie is not None:
        _set_turnstile_cookie(cookie)
    
    if spacegroup == 'all':
        spacegroup = list(range(1, 231))
    else:
        pass

    if isinstance(spacegroup, list):
        for n in spacegroup:
            groupnum = int(n)
            # get_kvectors(groupnum, force_redownload=force_redownload)
            get_genmat(groupnum, force_redownload=force_redownload)
    else:
        # get_kvectors(int(spacegroup), force_redownload=force_redownload)
        get_genmat(int(spacegroup), force_redownload=force_redownload)

def _check_resource(filename:str):
    if os.path.exists(filename):
            with open(filename) as f:
                data_dict = json.load(f)
            return data_dict
    else:
        return False

def _get_resource(filename:str) -> dict | cbt.Literal[False]:
    if os.path.exists(filename):
            with open(filename) as f:
                data_dict = json.load(f)
            return data_dict
    else:
        return False
    
def _create_resource(filename:str, dictionary:dict) -> None:
    if len(dictionary) != 0:
        try:
            os.mkdir(resources)
        except FileExistsError:
            print(f"Saving {filename} to Resources file at {resources}")

        for key, value in dictionary.items():
            if isinstance(value, np.ndarray):
                dictionary[key] = value.tolist()
        with open(filename, 'w') as f:
            json.dump(dictionary, f, indent=3)
    else:
        raise Exception("Error: No Data Found. Check group number or run _set_turnstile_cookie() to bypass the Bilbao Crystallographic Server's Cloudflare Protection")
        
        
def get_kvectors(groupnum:int, output:cbt.Literal['dictionary', 'list', 'array', None]='dictionary', **kwargs) -> dict|cbt.Array|list|None:
    
    
    force_redownload = kwargs.get("force_redownload", False)
    
    kvec_array = [] #will convert coordinates to array
    kvec_dictionary = {} ## for converting both symbols and coordinates to formatted dictionary
    
    file = os.path.join(resources, f'{groupnum}-kvec.json')
    localkdict = _get_resource(file)
    if (localkdict) and not (force_redownload):
        for key, k in localkdict.items():
            kvec_array.append(k)
        save_file = False
        kvec_dictionary = localkdict
    else:
        save_file = True
        URL = bilbao_url+"cgi-bin/cryst/programs/nph-kv-list"
        page = requests.post(URL, data={'gnum': str(groupnum),'standard':'Optimized listing of k-vector types using ITA description'}, cookies=cookie_dict)
        soup = BeautifulSoup(page.content, "html.parser") # type: ignore
        kvec_table = soup.find_all('table')[1]
        rows = kvec_table('tr')[2:]
        if len(rows) == 0:
            raise Exception("Error: No data found. Invalid group number, the Turnstile Cookie is not set up correctly or the Bilbao Server is unreachable.")
            
        raw_kvec_dict = {}
        for row in rows:
            sympoint = row.find_all('td')[0].get_text() #first cell has symbol/letter
            coordstring = row.find_all('td')[1].get_text() #next cell has the coordinates
            coord = coordstring.split(',') #split the kvec into components
            raw_kvec_dict[sympoint] = coord # create dictionary from symbol and coordinate

        for key, n in raw_kvec_dict.items():
            if len(n) == 3:           #Make sure we have (kx,ky,kz)
                point = []             ## container for the 3 coordinates
                for index, k in enumerate(n): ## iterate through all the points
                    k= re.split(r'\b\D\b', k) ### remove blanks, letters, and slashes from division signs.
                    try:
                        coordinate = float(k[0])/float(k[1])
                    except IndexError:
                        coordinate = float(k[0])
                    except ValueError:
                        try:
                            coordinate = float(k[0])
                        except ValueError:
                            coordinate = 1
                        pass
                    pass    
                    point.append(coordinate)
                kxkykz = np.reshape(np.array(point),(3))
                kvec_array.append(kxkykz)
        
                kvec_dictionary[key] = kxkykz
        

    kvec_array = np.reshape(np.asarray(kvec_array), (-1,3))

    if save_file == True:
        _create_resource(file, kvec_dictionary)
        
    if output == 'dictionary':
        return kvec_dictionary
    elif output == 'array':
        return kvec_array
    elif output == 'list':
        return list(kvec_array)
    else:
        return 

def get_genmat(groupnum:int, output:cbt.Literal['array', 'list', None]=None, **kwargs) -> list[cbt.Array]|cbt.Array|None:
    """ Retrieve generator matrices 
    
    Parameters
    -----------
    groupnum : int
        One of 230 numbered space groups in the IUCr
    
    Returns
    --------
    matrix_list : list
        list of matrices representing general positions
    
    """

    force_redownload = kwargs.get("force_redownload", False)
    matrix_list = [] #will convert coordinates to array
    gen_dictionary = {} ## for converting both symbols and coordinates to formatted dictionary
    
    file = os.path.join(resources, f'{groupnum}-generators.json')
    localgendict = _get_resource(file)
    if localgendict and not force_redownload:
        for key, k in localgendict.items():
            matrix = k
            matrix_list.append(k)
        save_file = False
    else:
        save_file = True
        URL = bilbao_url+ "cgi-bin/cryst/programs/nph-getgen"
        page = requests.post(URL, data={'gnum': str(
            groupnum), 'what': 'gp', 'list': 'Standard/Default+Setting'}, cookies=cookie_dict)
        gen_pos = BeautifulSoup(page.content, "html.parser") # type: ignore
        holder = gen_pos.find_all("pre")

        matrix_text = []
        if len(holder) == 0:
            raise Exception("Error: No data found. Invalid group number, the Turnstile Cookie is not set up correctly or the Bilbao Server is unreachable.")
                    
        for k in holder:
            matrix_text.append(k.get_text()) #get text from table

        for f in range(0, len(matrix_text)):  
            genpos_line = matrix_text[f].split('\n') #separate the matrix text based on newline, giving 3x4 matrix of strings

            genpos_matrix = np.array([]).reshape(0,4)  #create an empty numpy array to "append" each row of the matrix to

            for row_string in genpos_line:
                row_list = list(filter(None, row_string.split(' '))) # generate a list of strings for each row.
                row_elements = [] ## create list to store the elements as floats
                
                for element in row_list: #go through and convert string elements to floating point ones
                    try:
                        matrix_value = float(element) #try simply converting
                    except ValueError:
                        elem_split = element.split('/') #if the simple conversion doesn't work, it's likely because it's written as a fraction
                        matrix_value = float(elem_split[0])/float(elem_split[1]) #calculate the float from the fraction

                    
                    row_elements.append(matrix_value)  #Put the element in a list with the others in the same row

                row_elements = np.asarray(row_elements) #convert to numpy array
                genpos_matrix = np.vstack([genpos_matrix, row_elements]) #add the below our existing row
            
            matrix_list.append(genpos_matrix) #After iterating through the rows of the matrix, put the matrix in the list

    if save_file == True:
        matdict = {}
        for key, value in enumerate(matrix_list):
            matdict[key] = value
        
        _create_resource(file, matdict) 

    if output == 'list':
        return matrix_list
    elif output == 'array':
        return np.asanyarray(matrix_list)
    else:
        return
    

def get_coordinates(groupnum:int, origin:cbt.VectorType, output:cbt.Literal['array', 'list']='array', a_mag:cbt.VectorType = np.array([1,1,1]), include_out_of_bounds=True, **kwargs) -> list|cbt.Array|None:
    """Generates positions from specified origin and generator matrices

    Parameters
    ----------
    groupnum : int
        One of 230 numbered space groups in the IUCr
        
    origin : VectorType
        Any point that should be used as (x,y,z) for symmetry operations from the generator matrices. 
        
    output : Literal['array', 'list'], optional, default 'array'
            'array' outputs m x 3 numpy array with m being the number of generator matrices. If 'list', outputs a list of lists
            
    a_mag : VectorType, optional, default array[1,1,1]
        Magnitude of lattice vector. All coordinates are multiplied by the components of this vector.
        
    include_out_of_bounds : bool, optional, default True
        Include (True, default) points that are outside of the range 0 to a_mag. This feature is a WIP.
        
    kwargs
    ------
    output_array : bool
        This was previously a regular argument, but was superseeded by `output`. For backwards compatiblity, this kwarg will override the choice made in `output`. E.g., True will return an array and False will return a list.

    
    Returns
    -------
    coordinates : array, list, default array
        Returns an array if output_array is True (default), returns a list object otherwise.


    """
    
    output_kwarg = kwargs.get("output_array", None)
    if output_kwarg is True:
        output = 'array'
    elif output_kwarg is False:
        output = 'list'
    else:
        pass
        

    bound_override = include_out_of_bounds
    lattice_scaling = np.asarray(a_mag)
    logger.debug(f"origin: {origin}")
    position_vector = np.array([origin[0], origin[1], origin[2]]).reshape(3,1) #type:ignore
    matrix_list = get_genmat(groupnum, output='list')
    assert matrix_list is not None
    coordinate_list = []
    coordinate_array = np.array([]).reshape(0,3)
    for n in matrix_list: #type:ignore
        n = np.asarray(n)
        # scaled_n = (n.T*lattice_scaling).T
        linear_part, translation_part = np.split(n, [3,], axis=1) #Split matrix into linear part and translation part, *after* third element in row
 
        #linear_part is 3x3, translation_part is 3x1
        linear_product = np.matmul(linear_part, position_vector)  #matrix part
        # print(linear_product)
        # print(f"lattice: {lattice_scaling} \n translation: {translation_part.T} ")


        transformation = linear_product + (translation_part.T * lattice_scaling).T #affine transformation
        # print(transformation)
        new_point = transformation.reshape(1,3) #make row matrix
        if ((((new_point<=lattice_scaling).all()) and ((new_point>= 0).all())) or (bound_override == True)):
            if output=='array':
                coordinate_array = np.concatenate([coordinate_array, new_point], axis=0)
            elif output == 'list':
                coordinate_list.append(new_point.tolist()) #add point to list
            else:
                pass
        else:
            continue
        

    if output == 'array':
        return coordinate_array
    elif output == 'list':
        return coordinate_list
    else:
        return

class SpaceGroup():
    """ 
    One of 230 space groups

    This class will have the properties necessary for each space group, as pulled from the Bilbao database.

    Includes:
        k-vectors with labels
        generator matrices
        generation of equivalent points
    """

    def __init__(
            self,
            group_number: int,
            **kwargs
                    ) -> None:
        
        """
        Create the instance of a Space Group

        Parameters
        -----------
        group_number : int
            1-230, corresponding to IUCr and Bilbao server notation.
        
        kwargs
        -------
        points : list, ndarray
            Initial coordinates that will be operated on by the symmetry operations to create the entire unit cell.
        
        """
        
        self.point_list: cbt.Array|None = kwargs.get("points", None)
        self.group_num = group_number
        
        self.kvec_dict = get_kvectors(self.group_num, output='dictionary')
        self.kvec_arr = get_kvectors(self.group_num, output='array')

        self.generator_matrices = get_genmat(self.group_num)

        self.generated_points = self.calculate_points(self.point_list)

    def calculate_points(self, point_list: list|cbt.Array|None, a_mag: cbt.VectorType = [1,1,1], ignore_repeats:bool = True) -> cbt.Array:
        """
        Return a list of coordinates resulting from symmetry operations to each point in `point_list`. This is called once if the `SpaceGroup` is initialized with the `points` kwarg.
        It can be called any number of times to directly return points from new `point_list` inputs.
        
        Parameter
        ----------
        point_list : tuple, list, ndarray
            point(s) on which to perform symmetry operations

        a_mag : list, ndarray
            magnitude of lattice vectors in each direction
                
        ignore_repeats : bool (default true)
            Ignore points that are identical to ones already calculated. There's no reason to change this unless you're trying to view all of the positions
        
        Return
        -------
        generated_points : ndarray
            Unique points resulting from the symmetry operations on points in point_list. This includes negative values and values greater than 1 (outside the primitive cell).
        """
        generated_points:cbt.Array = np.array([]).reshape(-1,3)
        if point_list is not None:
            logger.debug(f"Point list is: {point_list}")
            logger.debug(f"point list type is: {type(point_list)}")
            if any(isinstance(point, (list, np.ndarray, tuple)) for point in point_list):
                for n in point_list:
                    logger.debug(f"individual point in list is type: {type(n)}")
                    scaled_point = n * np.asarray(a_mag)
                    newpoint = get_coordinates(self.group_num, origin=scaled_point, a_mag=a_mag, output='array')
                    generated_points = np.vstack((generated_points, newpoint))
                generated_points.reshape(-1,3)
                listlen=len(generated_points)
                if ignore_repeats == True:
                    generated_points = np.unique(generated_points, axis=0)
                
            else:
                logger.debug(f"only found one point of type: {type(point_list)}")
                scaled_point = point_list * np.asarray(a_mag)
                print(scaled_point)
                generated_points:cbt.Array = get_coordinates(self.group_num, origin=scaled_point, a_mag=a_mag)
                generated_points.reshape(-1,3)
                listlen=len(generated_points)
                if ignore_repeats == True:
                    generated_points = np.unique(generated_points, axis=0)
                
            print(f"Generated {listlen} points, returned {len(generated_points)}. {listlen - len(generated_points)} duplicates removed")
            print(f"Returned {len(generated_points)} points")
            return generated_points

        else:
            return np.array([0,0,0])
                 

if __name__ == "__main__":

    pass
    # _get_spacegroups(cookie='1770081648', spacegroup=230)
    

    # # crystest = SpaceGroup(227)
    # # pointlist = crystest.calculate_points([(0,0,0)])
    # # print(pointlist)
    # print(pointlist.shape)
    
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.invert_xaxis()
    
    # ax.scatter(pointlist[:, 0], pointlist[:, 1], pointlist[:,2])
    # plt.show()
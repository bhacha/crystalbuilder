
import re
import os

location = os.path.dirname(os.path.realpath(__file__))
resources = os.path.join(location, 'resources')

if os.path.exists(resources):
    pass
else:
    os.makedirs(resources)
import requests
import numpy as np
from bs4 import BeautifulSoup
import json
    

def check_resource(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            kvec_dict = json.load(f)
            kvec_dict.pop("_attribution")
        return kvec_dict
    else:
        return False
    
def create_resource(filename, dictionary):
    for key, value in dictionary.items():
        if isinstance(value, np.ndarray):
            dictionary[key] = value.tolist()
    try:
        with open(filename, 'w') as f:
            dictionary["_attribution"] = "This data was obtained from the Bilbao Crystallographic Server at www.cryst.ehu.es. Please cite the following: "\
                                        "| M. I. Aroyo, J. M. Perez-Mato, C. Capillas, E. Kroumova, S. Ivantchev, G. Madariaga, A. Kirov & H. Wondratschek. 'Bilbao Crystallographic Server I: Databases and crystallographic computing programs'. Zeitschrift fuer Kristallographie (2006), 221, 1, 15-27. | and " \
                                        "| M. I. Aroyo, A. Kirov, C. Capillas, J. M. Perez-Mato & H. Wondratschek. 'Bilbao Crystallographic Server II: Representations of crystallographic point groups and space groups'. Acta Cryst. (2006), A62, 115-128. |" 
            json.dump(dictionary, f, indent=3)
    except Exception as e:
        print(f"Cannot save {filename} resource file. Error: {type(e).__name__}")
        
        
        
def get_kvectors(groupnum, dict_out=False):
    
    kvec_array = [] #will convert coordinates to array
    kvec_dictionary = {} ## for converting both symbols and coordinates to formatted dictionary
    
    file = os.path.join(resources, f'{groupnum}-kvec.json')
    localkdict = check_resource(file)
    if localkdict:
        for key, k in localkdict.items():
            kvec_array.append(k)
        save_file = False
        kvec_dictionary = localkdict
    else:
        save_file = True
        URL = "http://webbdcrista2.ehu.es/cgi-bin/cryst/programs/nph-kv-list"
        page = requests.post(URL, data={'gnum': str(groupnum),'standard':'Optimized listing of k-vector types using ITA description'})
        soup = BeautifulSoup(page.content, "html.parser")
        kvec_table = soup.find_all('table')[1]
        rows = kvec_table('tr')[2:]
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
        create_resource(file, kvec_dictionary)
        
    if dict_out == True:
        return kvec_dictionary
    else:
        return kvec_array

def get_genmat(groupnum):
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

    matrix_list = [] #will convert coordinates to array
    gen_dictionary = {} ## for converting both symbols and coordinates to formatted dictionary
    
    file = os.path.join(resources, f'{groupnum}-generators.json')
    localgendict = check_resource(file)
    if localgendict:
        for key, k in localgendict.items():
            matrix = k
            matrix_list.append(k)
        save_file = False
    else:
        save_file = True
        URL = "http://webbdcrista2.ehu.es/cgi-bin/cryst/programs/nph-getgen"
        page = requests.post(URL, data={'gnum': str(
            groupnum), 'what': 'gp', 'list': 'Standard/Default+Setting'})
        gen_pos = BeautifulSoup(page.content, "html.parser")
        holder = gen_pos.find_all("pre")

        matrix_text = []
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
        
        create_resource(file, matdict) 

    return matrix_list

def get_coordinates(groupnum, origin, output_array=True):
    """ Generates positions from specified origin and generator matrices
    
    Parameters
    -----------
    groupnum : int
        One of 230 numbered space groups in the IUCr

    origin : list
        Any point that should be used as (x,y,z) for symmetry operations from the generator matrices
    
    output_array : bool
        Oututs numpy array by default (True), since the result should be an m x 3 matrix with m being the number of generator matrices. If False, the output is a list of lists.
    
    Returns
    --------
    coordinates : list, array
        Returns an array if output_array is True (default), returns a list object otherwise.


    
    """

    position_vector = np.array([origin[0], origin[1], origin[2]]).reshape(3,1)
    matrix_list = get_genmat(groupnum)
    coordinate_list = []
    coordinate_array = np.array([]).reshape(0,3)
    for n in matrix_list:
        n = np.asarray(n)
        linear_part, translation_part = np.split(n, [3,], axis=1) #Split matrix into linear part and translation part, *after* third element in row
        #linear_part is 3x3, translation_part is 3x1
        linear_product = np.matmul(linear_part, position_vector)  #matrix part
        transformation = linear_product + translation_part #affine transformation
        new_point = transformation.reshape(1,3) #make row matrix
        if ((new_point.all() <= 1) and (new_point.all() >= 0)):
            if output_array==True:
                coordinate_array = np.concatenate([coordinate_array, new_point], axis=0)
            else:
                coordinate_list.append(new_point.tolist()) #add point to list
        else:
            continue
        

    if output_array == True:
        return coordinate_array
    else:
        return coordinate_list

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
            group_number,
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
        
        self.point_list = kwargs.get("points", None)
        self.group_num = group_number
        
        self.kvec_dict = get_kvectors(self.group_num, dict_out=True)
        self.kvec_arr = get_kvectors(self.group_num, dict_out=False)

        self.generator_matrices = get_genmat(self.group_num)

        self.generated_points = self.calculate_points(self.point_list)

    def calculate_points(self, point_list):
        """
        Return a list of coordinates resulting from symmetry operations to each point in `point_list`. This is called once if the `SpaceGroup` is initialized with the `points` kwarg.
        It can be called any number of times to directly return points from new `point_list` inputs.
        
        Parameter
        ----------
        point_list : tuple, list, ndarray
            point(s) on which to perform symmetry operations
            
        Return
        -------
        generated_points : ndarray
            Unique points resulting from the symmetry operations on points in point_list. This includes negative values and values greater than 1 (outside the primitive cell).
        """
        generated_points = np.array([]).reshape(-1,3)
        if point_list is not None:
            if isinstance(point_list, (list, np.ndarray)):
                for n in point_list:
                    newpoint = get_coordinates(self.group_num, origin=n)
                    generated_points = np.vstack((generated_points, newpoint))
                generated_points.reshape(-1,3)
                generated_points = np.unique(generated_points, axis=0)
                
            else:
                generated_points = get_coordinates(self.group_num, origin=point_list)
                generated_points.reshape(-1,3)
                generated_points = np.unique(generated_points, axis=0)
        
            return generated_points
        else:
            pass
        

if __name__ == "__main__":
    from matplotlib import pyplot as plt


    # crystest = SpaceGroup(227)
    # pointlist = crystest.calculate_points([(0,0,0)])
    # print(pointlist)
    # print(pointlist.shape)
    
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    
    # ax.scatter(pointlist[:, 0], pointlist[:, 1], pointlist[:,2])
    # plt.show()

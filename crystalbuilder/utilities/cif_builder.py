import crystalbuilder.geometry as geo
import crystalbuilder.lattice
import crystalbuilder.utilities.cif_reader as cifr
from crystalbuilder.utilities.utils import TransformationMatrix as tmat
import numpy as np


class CIF_structure:
    
    def __init__(self,
                 cif_dictionary):
        
        self.atom_format_dictionary = {}
        self.dictionary = cif_dictionary
        self.extract_lattice_info()
        self.define_lattice()
        
    def _initialize_atom_dictionary(self):
        atom_names = self.dictionary['positions'].keys()
        self.atom_format_dictionary[atom_names] = {
            "color": None, "radius": None
        }
    
    
        
    @classmethod
    def from_file(cls, filename):
        cif_data = cifr.CIF_file(filename)
        dictionary = cif_data.data
        return cls(dictionary)
    
    def define_lattice(self):
        """
        This takes the unit cell parameters and the orthonormal cartesian basis to create the crystal basis (lattice vectors)
        
        The expression comes from Ch. 1 of "Understanding Single-Crystal X-Ray Crystallography" by Dennis Bennett and the DIALS documentation (https://dials.github.io/dials-2.2/documentation/conventions.html)
        
        WIP: right now, the resulting array of lattice vectors does not have them all with a magnitude <=1. I actually don't think this matters for MPB, since it should renormalize for me. The example I used is a CIF from space group 12, which *does* have varying lengths of lattice vectors. I think this means that this result is "more" correct and that MPB will need me to specify the magnitudes in [a_1, a_2, a_3] (which makes sense)
        
        """        
        cart_vectors = np.array([[1,0,0],[0,1,0],[0,0,1]]) #Cartesian basis
        scaled_cart =self.basis_lengths *  cart_vectors
        
        alph_rad = np.deg2rad(self.angle_alph)
        bet_rad = np.deg2rad(self.angle_bet)
        gam_rad = np.deg2rad(self.angle_gam)

        a, b, c = self.basis_lengths
        
        volume = a*b*c*np.sqrt(1-np.cos(alph_rad)**2 - np.cos(bet_rad)**2 - np.cos(gam_rad)**2 + (2*np.cos(alph_rad)*np.cos(bet_rad)*np.cos(gam_rad)))
                
        change_to_cartesian = np.array( [[a, b*np.cos(gam_rad), c*np.cos(bet_rad)],
                                   [0, b*np.sin(gam_rad), (c*(np.cos(alph_rad) - np.cos(bet_rad)*np.cos(gam_rad))/np.sin(gam_rad))],
                                   [0, 0, volume/(a*b*np.sin(gam_rad))]]) #This basis transforms from lattice space to orthonormal cartesian; we want the inverse
        
        change_to_lattice = np.linalg.inv(change_to_cartesian)
        
        self.lattice_vector_matrix = np.matmul(change_to_lattice, scaled_cart).round(3) + 0 #tiny numbers get truncated to 0, but the minus sign is preserved. Adding 0 fixes that.
        self.lattice_vectors = [self.lattice_vector_matrix[:,0], self.lattice_vector_matrix[:,1], self.lattice_vector_matrix[:,2]]

    def extract_lattice_info(self):
        self.space_group = self.dictionary['Space Group']
        self.angle_alph = float(self.dictionary['cell_angle_alpha'])
        self.angle_bet = float(self.dictionary['cell_angle_beta'])
        self.angle_gam = float(self.dictionary['cell_angle_gamma'])
        self.lattice_parameters = np.array([float(self.dictionary['cell_length_a']),float(self.dictionary['cell_length_b']), float(self.dictionary['cell_length_c'])])
        self.basis_lengths = np.divide(self.lattice_parameters, np.max(self.lattice_parameters))
        

    def build_atoms(self):
        pass


    def _build_unique_atoms(self, radius=.05):
        positions = self.dictionary['positions']
        atom_list = []
        for atom in positions.keys():
            gen_atom = self._build_atoms(positions[atom], radius=radius, name=str(atom))
            atom_list += gen_atom
        self.labelled_atoms = atom_list
        return self.labelled_atoms

    @property
    def atom_formats(self):
        return self.atom_format_dictionary

    @atom_formats.setter
    def _set_atom_formats(self, updated_dictionary):
        self.atom_format_dictionary.update(updated_dictionary)
        
        
    def _build_generic_atoms(self, radius):
        positions = list(self.dictionary['positions'].values())
        self.generic_atoms = self._build_atoms(positions, radius)
        return self.generic_atoms
        

    def _build_atoms(self, position_list, radius=.05, **kwargs):
        """
        Create the geo.Spheres that correspond to atoms, each with radius r
        
        Parameters
        ----------
        radius : float
            radius of each "atom" sphere
        
        kwargs
        ------
        "color" : matplotlib color name
        "name" : str
            atom label

        """
        if radius is None: radius = .05
        color = kwargs.get('color', 'w')
        name = kwargs.get('name', 'atom')
        sphere_list = []
        for position in position_list:
            sphere = geo.Sphere(center=position, radius=radius,color=color, name=name)
            sphere_list.append(sphere)
        
        return sphere_list
    
    
        
if __name__ == "__main__":
    filename = "1000117.cif"
    struct = CIF_structure.from_file(filename)
    atoms = struct._build_generic_atoms(radius=1)
    print(atoms)
    # print(struct.dictionary)

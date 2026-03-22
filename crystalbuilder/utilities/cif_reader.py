import re
   
 
class CIF_file:
    """
    A class for opening and parsing CIF files containing crystallographic data.
    
    The only parameter is a filename.
    
    The main property of the CIF_File object is a dictionary with all the grepped fields. Accessing instance.atom_positions or instance.unlabeled positions will return a dictionary with just the positions or a list of unlabeled positions, respectively.
    
    
    Notes
    -----
        - This grabs the lines *containing*  `_cell_len`, `cell_angle`, `cell_formula_`, and `cell_volume` to create a dictionary of lattice parameters
        - nested in this dictionary is another dictionary, "positions" i.e. ExampleDictionary["positions"] that holds the atoms in the loop
        - To build this loop, the `atom_site_fract` lines are found and their index is used to pull the values from the lines starting with the line immediately after the last `_atom_site*` line.
            - This works with some early tests, since the last line of the loop info block should have that format
        
        - The next line is assumed to be the start of the coordinates and this is where it gets dicey.
            - The loop checks that the line is at least 3 space-delimited items and extracts the ones that match the indices of the `_atom_site_fract` fields 
            - so if the 3rd-5th lines of the loop info are `_atom_site_fract` fields, the 3-5 elements of the atom data lines are taken to be the position
            - There are likely to be errors if later fields in the file contain >= 3 space-delimited sections, since they will likely be parsed as containing this information
            - Further refinement can be done in the future, but this works for the 3 files I checked, so it's good for now.
        
        
    """
    
    
    def __init__(self, filename:str):
        with open(filename,'r') as f:
            self.file_lines = [line.rstrip() for line in f]
    
            self.raw_dictionary = self.parse_cif()
            self.clean_atom_dictionary()
    @property
    def atom_positions(self) -> dict:
        positions = self.dictionary["positions"]
        return positions
    
    @property
    def unlabeled_positions(self) -> list:
        positions = self.dictionary["positions"]
        unlab_pos = [positions[n] for n in positions]
        return unlab_pos
            
    @property
    def data(self) -> dict:
        return self.dictionary
    
    def parse_cif(self):
        lattice_dictionary = self.get_lattice_parameters()
        atom_dictionary = self.get_atom_loop()
        
        crystal_dictionary = lattice_dictionary|atom_dictionary
        return crystal_dictionary
    
    def get_lattice_parameters(self):
        lattice_dictionary = {}
        for line in self.file_lines:
            if "_cell_len" in line or "cell_angle" in line or "cell_formula_" in line or "cell_volume" in line:
                key, value = line.split(maxsplit=1)
                value = value.split("(")
                lattice_dictionary[key[1:]] = float(value[0])
            elif "_space_group_IT_number" in line:
                key, value = line.split(maxsplit=1)
                lattice_dictionary["Space Group"] = int(value)

        return lattice_dictionary
                 
    def get_atom_loop(self):
        """
        The exact shape of the atom position loop can vary. 
        Some sources don't include wyckoff symbols or attached hydrogens. 
        
        THIS IS NOT WORKING YET. 
        
        """
        atom_dictionary = {
            "positions":{}
        }
        atom_loop_length = 0
        position_indices = []
        final_index = 0
        for index, line in enumerate(self.file_lines):
            if ("atom_site_" in line) and ("aniso" not in line):
                if "fract" in line:
                    position_indices.append(atom_loop_length)
                else:
                    pass
                atom_loop_length += 1
                final_index = index+1

        for line in self.file_lines[final_index:]:
            split_line = line.split()
            if len(split_line)>=3:
                atom_label = split_line[0]
                atom_dictionary["positions"][atom_label] = [split_line[position_indices[0]], 
                                            split_line[position_indices[1]], 
                                            split_line[position_indices[2]] ]
    
            
        return atom_dictionary

    def clean_atom_dictionary(self):
        self.dictionary = self.raw_dictionary.copy()
        for element_positions in self.raw_dictionary["positions"]:
            pos = self.raw_dictionary["positions"][element_positions]
            formatted_pos = [float(coordinate.split("(")[0]) for coordinate in pos]
            self.dictionary["positions"][element_positions] = formatted_pos

    
if __name__ == "__main__":
    
    cif = "1000443.cif"
    data = CIF_file(cif)
    data.unlabeled_positions
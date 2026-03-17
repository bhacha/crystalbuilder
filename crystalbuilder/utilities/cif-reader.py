import re

with open("2106498.cif",'r') as f:
    file_lines = [line.rstrip() for line in f]
 
 
def parse_cif(filename):
    with open(filename,'r') as f:
        file_lines = [line.rstrip() for line in f]
    
    lattice_dictionary = get_lattice_parameters(file_lines)
    atom_dictionary = get_atom_loop(file_lines)
    
    crystal_dictionary = lattice_dictionary|atom_dictionary
    return crystal_dictionary
        
    
def get_lattice_parameters(filedata):
    lattice_dictionary = {}
    for line in filedata:
        if "_cell_len" in line or "cell_angle" in line or "cell_formula_" in line or "cell_volume" in line:
            key, value = line.split(maxsplit=1)
            value = value.split("(")
            lattice_dictionary[key[1:]] = float(value[0])
        elif "_space_group_IT_number" in line:
            key, value = line.split(maxsplit=1)
            print(value)
            lattice_dictionary["Space Group"] = int(value)

    return lattice_dictionary
            
            
def get_atom_loop(filedata):
    """
    The exact shape of the atom position loop can vary. 
    Some sources don't include wyckoff symbols or attached hydrogens. 
    
    THIS IS NOT WORKING YET. 
    
    """
    atom_dictionary = {}
    atom_loop_length = 0
    position_indices = []
    for index, line in enumerate(filedata):
        if "atom_site" in line:
            if "fract" in line:
                position_indices.append(atom_loop_length)
            else:
                pass
            atom_loop_length += 1
            final_index = index+1

    for line in filedata[final_index:]:
        split_line = line.split()
        if len(split_line)>=3:
            atom_label = split_line[0]
            atom_dictionary[atom_label] = [split_line[position_indices[0]], 
                                           split_line[position_indices[1]], 
                                           split_line[position_indices[2]] ]
  
        
    return atom_dictionary
    
if __name__ == "__main__":
    
    cif = "2106498.cif"
    crystal_dict = parse_cif(cif)
    print(crystal_dict)
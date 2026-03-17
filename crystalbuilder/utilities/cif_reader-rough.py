import re

#look for line beginning with "_space_group_IT_number" and include the entire line
space_group_regex = "^_space_group_IT_number.*"

#Split line right before space group number
space_group_split_regex = r"(?=\d.+)"



search_basislength_regex = "^_cell_length_[a-c].*"
search_basiskey_regex = "^_cell_length_[a-c]"

split_basislength_regex = r'\d*\.\d*'
split_atompositions_regex = r'\d*\.\d*'

search_atomloop_regex = r"(?<=_atom_site_)(?:fract).*(?=loop_)?"
split_atomloop_regex = r"(\n)(?!_)(.*)"

structure_dict = {}

with open("2106498.cif",'r') as f:
    file_lines = f.read()
    

space_group_search = re.search(space_group_regex, file_lines, re.MULTILINE)
print(space_group_search.group(0))
space_group_number = re.split(space_group_split_regex, space_group_search.group(0))[1]



lattice_vectors_search_list = re.findall(search_basislength_regex, file_lines, re.MULTILINE)
for result in lattice_vectors_search_list:
    key = re.search(search_basiskey_regex, result)
    value = re.search(split_basislength_regex, result)
    structure_dict[key.group(0)] = value.group(0)

loop_search_block = re.findall(search_atomloop_regex, file_lines, re.MULTILINE)
print(loop_search_block)





def get_atom_positions(loop_search_block):
    atom_block = re.findall(split_atomloop_regex, loop_search_block.group(0))
    for result in atom_block:
        relevant_string = result[1]
        atom_name = re.match(r"^\S*", relevant_string).group(0)
        matches = re.finditer(split_atompositions_regex, relevant_string)
        for number, match in enumerate(matches):
            if number == 0:
                ax = "_x"
                structure_dict[atom_name+ax] = match.group(0)
            elif number == 1:
                ax = "_y"
                structure_dict[atom_name+ax] = match.group(0)
            elif number == 2:
                ax = "_z"
                structure_dict[atom_name+ax] = match.group(0)
            else:
                pass
    
        
# get_atom_positions(loop_search_block)
# print(structure_dict)
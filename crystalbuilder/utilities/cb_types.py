import numpy as np
import numpy.typing as npt
import typing as tp
import collections.abc as coll



Literal = tp.Literal
Iterable = coll.Iterable

angle_unit_type = tp.Literal['deg', 'degrees', 'd', 'degree', 'radians', 'rad', 'r', 'radian']
number = np.number | float 



array = np.ndarray

vector_type = coll.Sequence | array
axis_number = tp.Literal[0,1,2]
axis_type = axis_number|array


vector_list = list[vector_type] | tuple[vector_type] | coll.Sequence[vector_type] | array
matrix_like = list[coll.Sequence] | array 

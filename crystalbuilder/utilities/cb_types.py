import numpy as np
import numpy.typing as npt
import typing as tp



Literal = tp.Literal
Iterable = tp.Iterable
vector_type = list|np.ndarray|tuple
angle_unit_type = tp.Literal['deg', 'degrees', 'd', 'degree', 'radians', 'rad', 'r', 'radian']
number = np.number | float
array = np.ndarray
matrix_like = list[tp.Iterable] | array
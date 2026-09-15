from __future__ import annotations
import numpy as np
import numpy.typing as npt
import typing as tp
import collections.abc as coll



Literal = tp.Literal
Iterable = coll.Iterable

AngleUnits = tp.Literal['deg', 'degrees', 'd', 'degree', 'radians', 'rad', 'r', 'radian']
Number = float 



Array = npt.NDArray

VectorType = coll.Sequence | Array
AxisNumber = tp.Literal[0,1,2]
AxisType = AxisNumber|VectorType


VectorSet = list[VectorType] | tuple[VectorType] | coll.Sequence[VectorType] | Array
MatrixLike = list[coll.Sequence] | Array 

`crystalbuilder` is a package created for building photonic crystals and implementing them for simulation (Lumerical, Tidy3D, MEEP (and MPB)) and exporting them for 3D printing. 

The current version of the package features (as Works in Progress):
 - Full support for cylinders and spheres as basic geometry objects
 - Partial support for rectangles and triangles. These will probably be a buggy mess for anything beyond 2D photonic crystals. 
 - Backends to Tidy3D and MEEP/MPB. These do not use an intermediate STL/OBJ step, which makes it much friendlier on resources than simply exporting and importing STL files. 
 - Support for arbitrary lattice bases
 - Supercell-building properties. Tile not just an object, but an entire group of them.
 - Some skeletons of a method for modulating the supercells, such as that used for Dirac vortex crystals. 
 - Interface with the Bilbao Crystallographic Server for the automatic creation of lattices. 

 You can check out the `documentation here`_ and the whole project is `hosted on Github`_.

.. _documentation here: https://crystalbuilder.readthedocs.io/en/latest/

.. _hosted on Github: https://github.com/bhacha/crystalbuilder
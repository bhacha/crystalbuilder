.. CrystalBuilder documentation master file, created by
   sphinx-quickstart on Tue Jan 14 13:37:00 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CrystalBuilder
============================
This is Sphinx-generated documentation for the crystalbuilder package, designed for generating 2D and 3D photonic crystals. 


Submodules
==========

The CrystalBuilder package contains 5 main modules. 

* :ref:`geometry <geometry_docs>`
   * Objects for defining unit cells

* :ref:`lattice <lattice_docs>`
   * Methods for tiling unit cells or geometries

* :ref:`convert <convert_docs>`
   * Methods for converting CrystalBuilder objects to MPB, MEEP, etc.

* :ref:`bilbao <bilbao_docs>`
   * Interface to pull positions from Bilbao servers. 

* :ref:`vectors <vectors_docs>`
   * Methods for manipulating vectors. This is probably not necessary for most general uses.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   CrystalBuilder <self>
   Getting Started <source/getting_started>

.. toctree::
   :maxdepth: 1
   :caption: Examples

   source/diamond_examples



.. toctree::
   :maxdepth: 1
   :caption: API Documentation


   source/bilbao
   source/convert
   source/geometry
   source/lattice
   source/vectors
   
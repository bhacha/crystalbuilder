Exporting a Crystal Example
==============================

Here, we will build a crystal structure and export it using Trimesh.

.. code-block:: python
    :force:
    :name: define-lattice

    from crystalbuilder import *
    import crystalbuilder.geometry as geo
    import matplotlib.pyplot as plt
    import numpy as np
    import vedo

    a1 = [0, 1, 1]
    a2 = [1, 0 ,1]
    a3 = [1, 1, 0]

    a_mag = np.sqrt(.5)


    geo_lattice = lattice.Lattice(a1, a2, a3, magnitude = [a_mag, a_mag, a_mag])

.. code-block:: python
    :name: make-cylinders

Now lets use our previously defined lattice to tile these cylinders into a crystal.

.. code-block:: python
    :name: tile-lattice

    a1_reps = 5
    a2_reps = 5
    a3_reps = 5
    crystal = geo_lattice.tile_geogeometry(unit_cell, a1_reps, a2_reps, a3_reps)

We can visualize this using CrystalBuilder's viewer package, which builds the structure as a `vedo <https://github.com/marcomusy/vedo>`_ scene. 

.. code-block:: python
    :name: view-crystal

    scene = viewer.visualize(crystal)
    scene.show().close()

It looks good, so let's convert to MPB and simulate a band structure.

.. code-block:: python
    :name: convert-mpb

    import meep as mp
    from meep import mpb

    material = mp.Medium(epsilon=9)

    mpb_lattice = convert.to_mpb_lattice(geo_lattice)
    mpb_geometry = convert.geo_to_mpb(unit_cell, material=material, lattice=mpb_lattice)


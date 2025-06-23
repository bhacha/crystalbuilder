Rod-Connected Diamond Example
==============================

This notebook will walk through an example of creating a 3D photonic crystal based on the rod-connected diamond motif. The structure will be made using CrystalBuilder's geo package and then simulated using MPB. 

First, let's define our basis. The unit length in MPB is `a` which you can think of as 1 (in whatever units you want). The values used in MPB are all multiples of this. For optical wavelengths, its easiest to consider this to be in units of microns. **It doesn't actually matter though.** Just know that every value you use and every answer you get will be relative to this `a`. 

Back to our diamond lattice. This is a face-centered cubic crystal, which has a rhombohedral primitive cell. This is what we will use for the simulation, but the conventional diamond unit cell is actually cubic, so our lattice vector will be :math:`\sqrt{\frac{a}{2}}` instead of `a`` units long. I know what you might be thinking:

    *"But wait, I thought the units didn't matter!"*


Well, you're right. What we're doing here is defining our basis vectors so that the primitive cell we build will be a truly sized chunk of the conventional unit cell with dimensions `a` x `a` x `a`. You don't have to do this step, but you will need to do an extra scaling step at the end if you want to convert to wavelength (which likely depends on your conventional cell `a`). By scaling at the beginning, you can treat your conventional cell `a` as 1 and use MPB normally.

Let's import our packages and define our lattice.

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


We've now defined our lattice. It's important to note that this is a CrystalBuilder lattice and not an MPB one. They can be converted, as we will show later, but they are not the exact same. 

Let's get the positions of the "atoms" in the diamond lattice that our rods will connect. Unlike in MPB, **all of our vectors will be in Cartesian coordinates.** If you would prefer to work in a crystal basis, you can check out the options in :doc:`vectors`, but you'll likely be disappointed because I try to do everything in cartesian space.

The square diamond lattice looks like 4 tetrahedra connected to one another, but our rhombohedral primitive cell will only include one of them. The tetrahedral rods will connect to one another at :math:`\left( \frac{1}{4}, \frac{1}{4}, \frac{1}{4} \right) \cdot a`.

Omitting the factor of a (since a=1), the other points will be:

* :math:`\left( 0, 0, 0 \right)`
* :math:`\left( \frac{1}{2}, \frac{1}{2}, 0 \right)`
* :math:`\left( \frac{1}{2}, 0, \frac{1}{2} \right)`
* :math:`\left( 0, \frac{1}{2}, \frac{1}{2} \right)`


We'll make cylinders that connect these points. CrystalBuilder's Cylinder class features ``Cylinder.from_vertices()`` as a way to define the objects based on their start/end positions and a radius. Let's set those now.

.. code-block:: python
    :name: make-cylinders

    diamond_points = [
    (1/4, 1/4, 1/4),
    (0,0,0),
    (1/2, 1/2, 0),
    (1/2, 0, 1/2),
    (0,1/2, 1/2)
    ]

    radius = .01*a_mag

    cylinder_1 = geo.Cylinder.from_vertices([diamond_points[0], diamond_points[1]], radius=radius)
    cylinder_2 = geo.Cylinder.from_vertices([diamond_points[0], diamond_points[2]], radius=radius)
    cylinder_3 = geo.Cylinder.from_vertices([diamond_points[0], diamond_points[3]], radius=radius)
    cylinder_4 = geo.Cylinder.from_vertices([diamond_points[0], diamond_points[4]], radius=radius)

    unit_cell = [cylinder_1, cylinder_2, cylinder_3, cylinder_4]

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


The above conversions are done by the CrystalBuilder convert module, and our output defines our mpb_lattice and our mpb_geometry. From here, you can continue your regular MPB simulation process!

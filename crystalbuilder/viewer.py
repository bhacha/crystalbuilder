import vedo
import crystalbuilder
import crystalbuilder.geometry as geo

vedo.settings.default_backend='vtk'



def add_to_visualizer(structures, plot, **kwargs):
    for object in structures:       
        if isinstance(object, geo.Cylinder):
            plot += visualize_cylinder(object, **kwargs)
        elif isinstance(object, geo.Sphere):
            plot += visualize_sphere(object, **kwargs)
        elif isinstance(object, geo.SuperCell):
            plot += visualize_supercell(object, **kwargs)


def visualize(structures, plotter_style=7, **kwargs):
    """
    
    Parameters
    -----------
    structures : list of geo

    """
    
    plot = vedo.Plotter(axes=plotter_style)

    add_to_visualizer(structures, plot)
    
    for object in structures:
        if isinstance(object, geo.Structure):
            if isinstance(object, geo.Cylinder):
                obj  = visualize_cylinder(object, **kwargs)
                plot += obj
            elif isinstance(object, geo.SuperCell):
                obj  = visualize_supercell(object, **kwargs)
                plot += obj
            elif isinstance(object, geo.Sphere):
                obj = visualize_sphere(object, **kwargs)
                plot += obj
        elif isinstance(object, list):
            for n in object:
                add_to_visualizer(n, plot)
                
    
    return plot

def visualize_unit_cell(Lattice, plot):
    basis = Lattice.output_basis_as_Tmat_list()
    axes = basis
    Transform = vedo.transformations.LinearTransform(axes)
    print(Transform)
    box = vedo.Box( pos = [0, 1, 0, 1, 0, 1]).wireframe()
    box.apply_transform(Transform)
    print(box.boundaries())
    plot += box
    return plot

def visualize_cylinder(cylinder, **kwargs):
    center = cylinder.center
    radius = cylinder.radius
    height = cylinder.height
    axis = cylinder.axis
    name = str(cylinder.center)
    obj = vedo.Cylinder(pos=center, r=radius, height=height, axis=axis, **kwargs).legend(name)
    obj.name = name
    return obj

def visualize_sphere(sphere, **kwargs):
    center = sphere.center
    radius = sphere.radius
    name = str(sphere.center)
    obj = vedo.Sphere(pos=center, r=radius, **kwargs).legend(name)
    obj.name = name
    return obj

def visualize_supercell(SuperCell, **kwargs):
    objects = []
    for structure in SuperCell:
        if isinstance(structure, geo.Cylinder):
            objects.append(visualize_cylinder(structure, **kwargs))
        elif isinstance(structure, geo.Sphere):
            objects.append(visualize_sphere(structure, **kwargs))
    return objects




if __name__ == "__main__":
    import crystalbuilder.lattice as lattice
    a1 = [0, 1, 1]
    a2 = [1, 0 ,1]
    a3 = [1, 1, 0]

    a_mag=1
    
    geo_lattice = lattice.Lattice(a1, a2, a3, magnitude = [a_mag, a_mag, a_mag])
    cylinder1 = geo.Cylinder(center=(0,0,0), radius=1, height=3, axis=2)
    cylinder2 = geo.Cylinder(center=(5,5,0), radius=2, height=6, axis=1)
    plot = visualize([cylinder1, cylinder2])
    plot= visualize_unit_cell(geo_lattice, plot)
    plot.show()
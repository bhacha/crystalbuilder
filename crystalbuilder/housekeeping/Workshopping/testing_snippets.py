    
# Geometry Testing 
"""
Make a block in pyplot using edges and vertices.

x = y = z = 1
    
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection='3d')


e1=(1.0, 1, 0.0)
e2=(0.0, 1.0, 1.0)
e3=(0.0, 0.0, 1.0)

block = Block.from_vectors(center=[.5,.5,.5], list_of_vectors=[e1, e2, e3], magnitudes= [2,1,1])
vertices = block.vertices
ax.scatter(xs=vertices[:, 0], ys = vertices[:,1], zs=vertices[:,2])
edges = block.edge_array
for n in range(0, 12):
    ax.plot([edges[0,n,0],edges[1,n,0]], [edges[0,n,1],edges[1,n,1]], [edges[0,n,2], edges[1,n,2]])"""
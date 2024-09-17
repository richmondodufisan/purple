import gmsh
import math
import sys

gmsh.initialize()
gmsh.model.add("cornea_rectangle")

newMeshName = "cornea_rectangle.msh"

# quad elements
gmsh.option.setNumber("Mesh.Algorithm", 8);

ylen = 0.001

xlen = 30 * ylen

# mesh_refine = xlen/800
mesh_refine = 0.00025/4

# Adding points 
p1 = gmsh.model.occ.addPoint(0, 0, 0, mesh_refine)
p2 = gmsh.model.occ.addPoint(xlen, 0, 0, mesh_refine)
p3 = gmsh.model.occ.addPoint(xlen, ylen, 0, mesh_refine)
p4 = gmsh.model.occ.addPoint(0, ylen, 0, mesh_refine)
p5 = gmsh.model.occ.addPoint((xlen/10), ylen, 0, mesh_refine)
p6 = gmsh.model.occ.addPoint(xlen/2, ylen, 0, mesh_refine)

# Adding lines 
c1 = gmsh.model.occ.addLine(p4, p1)
c2 = gmsh.model.occ.addLine(p1, p2)
c3 = gmsh.model.occ.addLine(p2, p3)
c4 = gmsh.model.occ.addLine(p3, p5)
c5 = gmsh.model.occ.addLine(p5, p4)

# Adding Surfaces
cloop1 = gmsh.model.occ.addCurveLoop([c5, c1, c2, c3, c4])
s1 = gmsh.model.occ.addPlaneSurface([cloop1])

gmsh.model.occ.synchronize()

# Add physical groups
gmsh.model.addPhysicalGroup(1, [c4, c5], name = "top")
gmsh.model.addPhysicalGroup(1, [c2], name = "bottom")
gmsh.model.addPhysicalGroup(1, [c1], name = "left")
gmsh.model.addPhysicalGroup(1, [c3], name = "right")
gmsh.model.addPhysicalGroup(0, [p4], name = "loading_point")
gmsh.model.addPhysicalGroup(0, [p5], name = "data_point")
gmsh.model.addPhysicalGroup(0, [p1], name = "pressure_bc_point")

gmsh.option.setNumber("Mesh.RecombineAll", 1)
gmsh.model.occ.synchronize()

# Create 2D mesh
gmsh.model.mesh.generate(2)

# gmsh.fltk.run()

gmsh.option.setNumber("Mesh.SaveAll", 1)

gmsh.write(newMeshName)



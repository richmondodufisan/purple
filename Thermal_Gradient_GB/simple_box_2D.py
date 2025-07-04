import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("Box Geometry")

# Dimensions
length = 120  # X-dimension
height = 20   # Y-dimension
refinement = 5.0

# Create points
p1 = gmsh.model.occ.addPoint(0, 0, 0, refinement)
p2 = gmsh.model.occ.addPoint(0, height, 0, refinement)
p3 = gmsh.model.occ.addPoint(length, height, 0, refinement)
p4 = gmsh.model.occ.addPoint(length, 0, 0, refinement)

# Create lines
c1 = gmsh.model.occ.addLine(p1, p2)
c2 = gmsh.model.occ.addLine(p2, p3)
c3 = gmsh.model.occ.addLine(p3, p4)
c4 = gmsh.model.occ.addLine(p4, p1)

# Define curve loop and surface
cloop1 = gmsh.model.occ.addCurveLoop([c1, c2, c3, c4])
s1 = gmsh.model.occ.addPlaneSurface([cloop1])

# Synchronize the CAD kernel
gmsh.model.occ.synchronize()

# Define physical groups
gmsh.model.addPhysicalGroup(1, [c1], name = "left")
gmsh.model.addPhysicalGroup(1, [c3], name = "right")

# Optional: view before meshing
# gmsh.fltk.run()

# Mesh generation (2D since we're meshing a surface)
gmsh.option.setNumber("Mesh.SaveAll", 1)
gmsh.model.mesh.generate(2)

# Save to file
gmsh.write("simple_box_2D.msh")

# Optional: view mesh
gmsh.fltk.run()

# Finalize
gmsh.finalize()

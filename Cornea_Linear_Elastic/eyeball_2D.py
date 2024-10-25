import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("2D geometry")

# Set the refinement size
refinement = 0.00002

# Create points
p1 = gmsh.model.occ.addPoint(0, 0, 0, refinement)
p2 = gmsh.model.occ.addPoint(0.002, 0, 0, refinement)
p3 = gmsh.model.occ.addPoint(-0.002, 0, 0, refinement)
p4 = gmsh.model.occ.addPoint(0, -0.002, 0, refinement)
p5 = gmsh.model.occ.addPoint(0, 0.002, 0, refinement)

# Create circles (arcs between points)
c1 = gmsh.model.occ.addCircleArc(p5, p1, p2)
c2 = gmsh.model.occ.addCircleArc(p2, p1, p4)
c3 = gmsh.model.occ.addCircleArc(p4, p1, p3)
c4 = gmsh.model.occ.addCircleArc(p3, p1, p5)

# Create a curve loop and plane surface
cl1 = gmsh.model.occ.addCurveLoop([c4, c1, c2, c3])
s1 = gmsh.model.occ.addPlaneSurface([cl1])

# Synchronize the built model with the Gmsh kernel before adding physical groups
gmsh.model.occ.synchronize()

# Physical groups (for boundary conditions, etc.)
gmsh.model.addPhysicalGroup(0, [p5], 5, "loading_point")
gmsh.model.addPhysicalGroup(1, [c1], 6, "sample_location")

# Ensure that all elements are saved in the mesh file, even those not part of physical groups
gmsh.option.setNumber("Mesh.SaveAll", 1)

# Generate mesh
gmsh.model.mesh.generate(2)

# Save the mesh to a file
gmsh.write("eyeball_2D.msh")

# Uncomment to run Gmsh's built-in GUI (optional)
# gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()

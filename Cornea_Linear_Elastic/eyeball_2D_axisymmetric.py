import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("2D geometry")

# Set the refinement size
refinement = 0.002 / 100

# Create points in the x-y plane
p1 = gmsh.model.occ.addPoint(0, 0, 0, refinement)
p2 = gmsh.model.occ.addPoint(0, 0.002, 0, refinement)
p3 = gmsh.model.occ.addPoint(0, -0.002, 0, refinement)
p4 = gmsh.model.occ.addPoint(0.002, 0, 0, refinement)

# Create circle arcs and lines
c1 = gmsh.model.occ.addCircleArc(p2, p1, p4)
c2 = gmsh.model.occ.addCircleArc(p3, p1, p4)
l3 = gmsh.model.occ.addLine(p2, p1)
l4 = gmsh.model.occ.addLine(p1, p3)

# Create curve loop and plane surface
cl1 = gmsh.model.occ.addCurveLoop([l3, l4, c2, -c1])
s1 = gmsh.model.occ.addPlaneSurface([cl1])

# Synchronize the built model with the Gmsh kernel before adding physical groups
gmsh.model.occ.synchronize()

# Physical groups (for boundary conditions, etc.)
gmsh.model.addPhysicalGroup(0, [p2], 5, "loading_point")
gmsh.model.addPhysicalGroup(0, [p3], 6, "fixed_point")
gmsh.model.addPhysicalGroup(1, [c1], 7, "sample_location")
gmsh.model.addPhysicalGroup(1, [l3, l4], 8, "symmetry_axis")  # Include both l3 and l4

# Ensure that all elements are saved in the mesh file, even those not part of physical groups
gmsh.option.setNumber("Mesh.SaveAll", 1)

# Generate mesh
gmsh.model.mesh.generate(2)

# Save the mesh to a file
gmsh.write("eyeball_2D_axisymmetric.msh")

# Run Gmsh's built-in GUI (optional)
gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()

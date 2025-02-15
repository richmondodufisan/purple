import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("Box Geometry")

# Specify the dimensions of the rectangular box
length = 500  # X-dimension
width = 50   # Y-dimension
height = 50   # Z-dimension
half_height = height / 2

# Set mesh refinement size (optional)
refinement = 5.0

# Create points based on specified dimensions
p1 = gmsh.model.occ.addPoint(0, 0, 0, refinement)
p2 = gmsh.model.occ.addPoint(0, width, 0, refinement)
p3 = gmsh.model.occ.addPoint(length, width, 0, refinement)
p4 = gmsh.model.occ.addPoint(length, 0, 0, refinement)
p5 = gmsh.model.occ.addPoint(0, width, height, refinement)
p6 = gmsh.model.occ.addPoint(length, width, height, refinement)
p7 = gmsh.model.occ.addPoint(length, 0, height, refinement)
p8 = gmsh.model.occ.addPoint(0, width, half_height, refinement)  # Mid height point
p9 = gmsh.model.occ.addPoint(0, width, height, refinement)        # Duplicate of p5 for demo
p10 = gmsh.model.occ.addPoint(0, 0, height, refinement)

# Create lines
l1 = gmsh.model.occ.addLine(p10, p7)
l2 = gmsh.model.occ.addLine(p1, p4)
l3 = gmsh.model.occ.addLine(p4, p7)
l4 = gmsh.model.occ.addLine(p10, p1)
l5 = gmsh.model.occ.addLine(p5, p2)
l6 = gmsh.model.occ.addLine(p2, p1)
l7 = gmsh.model.occ.addLine(p10, p5)
l8 = gmsh.model.occ.addLine(p5, p6)
l9 = gmsh.model.occ.addLine(p6, p7)
l10 = gmsh.model.occ.addLine(p6, p3)
l11 = gmsh.model.occ.addLine(p4, p3)
l12 = gmsh.model.occ.addLine(p3, p2)

# Define curve loops and surfaces
cl1 = gmsh.model.occ.addCurveLoop([l1, -l3, -l2, -l4])
s1 = gmsh.model.occ.addPlaneSurface([cl1])

cl2 = gmsh.model.occ.addCurveLoop([l3, -l9, l10, -l11])
s2 = gmsh.model.occ.addPlaneSurface([cl2])

cl3 = gmsh.model.occ.addCurveLoop([l8, l9, -l1, l7])
s3 = gmsh.model.occ.addPlaneSurface([cl3])

cl4 = gmsh.model.occ.addCurveLoop([l4, -l6, -l5, -l7])
s4 = gmsh.model.occ.addPlaneSurface([cl4])

cl5 = gmsh.model.occ.addCurveLoop([l12, -l5, l8, l10])
s5 = gmsh.model.occ.addPlaneSurface([cl5])

cl6 = gmsh.model.occ.addCurveLoop([l2, l11, l12, l6])
s6 = gmsh.model.occ.addPlaneSurface([cl6])

# Create surface loop and volume
surface_loop = gmsh.model.occ.addSurfaceLoop([s1, s2, s3, s4, s5, s6])
volume = gmsh.model.occ.addVolume([surface_loop])

# Remove the mid-height point (p8) as per the original script
gmsh.model.occ.remove([(0, p8)])

# Synchronize the geometry before adding physical groups
gmsh.model.occ.synchronize()

# Define physical surfaces
gmsh.model.addPhysicalGroup(2, [s4], 13, "left")
gmsh.model.addPhysicalGroup(2, [s2], 14, "right")
gmsh.model.addPhysicalGroup(2, [s1, s6, s5, s3], 15, "sides")

# Ensure that all elements are saved in the mesh file
gmsh.option.setNumber("Mesh.SaveAll", 1)

# Generate 3D mesh
gmsh.model.mesh.generate(3)

# Save the mesh to a file
gmsh.write("simple_box_3D.msh")

# Run the GUI to view the geometry (optional)
gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()

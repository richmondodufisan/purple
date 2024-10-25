import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("3D geometry")

# Set the refinement size
refinement = 0.002 / 15

# Create points
p1 = gmsh.model.occ.addPoint(0, 0, 0, refinement)
p2 = gmsh.model.occ.addPoint(0, 0.002, 0, refinement)
p3 = gmsh.model.occ.addPoint(0, -0.002, 0, refinement)
p4 = gmsh.model.occ.addPoint(0, 0, 0.002, refinement)
p5 = gmsh.model.occ.addPoint(0, 0, -0.002, refinement)
p6 = gmsh.model.occ.addPoint(0.002, 0, 0, refinement)
p7 = gmsh.model.occ.addPoint(-0.002, 0, 0, refinement)

# Create circles (arcs between points)
c1 = gmsh.model.occ.addCircleArc(p4, p1, p2)
c2 = gmsh.model.occ.addCircleArc(p2, p1, p5)
c3 = gmsh.model.occ.addCircleArc(p6, p1, p2)
c4 = gmsh.model.occ.addCircleArc(p2, p1, p7)
c5 = gmsh.model.occ.addCircleArc(p4, p1, p3)
c6 = gmsh.model.occ.addCircleArc(p5, p1, p3)
c7 = gmsh.model.occ.addCircleArc(p6, p1, p3)
c8 = gmsh.model.occ.addCircleArc(p7, p1, p3)
c9 = gmsh.model.occ.addCircleArc(p4, p1, p7)
c10 = gmsh.model.occ.addCircleArc(p4, p1, p6)
c11 = gmsh.model.occ.addCircleArc(p6, p1, p5)
c12 = gmsh.model.occ.addCircleArc(p5, p1, p7)

# Create curve loops and surfaces
cl2 = gmsh.model.occ.addCurveLoop([c1, -c3, -c10])
s1 = gmsh.model.occ.addSurfaceFilling(cl2)

cl4 = gmsh.model.occ.addCurveLoop([c9, -c4, -c1])
s2 = gmsh.model.occ.addSurfaceFilling(cl4)

cl6 = gmsh.model.occ.addCurveLoop([c2, -c11, c3])
s3 = gmsh.model.occ.addSurfaceFilling(cl6)

cl8 = gmsh.model.occ.addCurveLoop([c2, c12, -c4])
s4 = gmsh.model.occ.addSurfaceFilling(cl8)

cl10 = gmsh.model.occ.addCurveLoop([c5, -c7, -c10])
s5 = gmsh.model.occ.addSurfaceFilling(cl10)

cl12 = gmsh.model.occ.addCurveLoop([c7, -c6, -c11])
s6 = gmsh.model.occ.addSurfaceFilling(cl12)

cl14 = gmsh.model.occ.addCurveLoop([c6, -c8, -c12])
s7 = gmsh.model.occ.addSurfaceFilling(cl14)

cl16 = gmsh.model.occ.addCurveLoop([c5, -c8, -c9])
s8 = gmsh.model.occ.addSurfaceFilling(cl16)

# Create the volume by defining the surface loop
sl1 = gmsh.model.occ.addSurfaceLoop([s7, s6, s5, s1, s2, s4, s3, s8])
vol1 = gmsh.model.occ.addVolume([sl1])

# Synchronize the built model with the Gmsh kernel before adding physical groups
gmsh.model.occ.synchronize()

# Now add physical groups for points and curves
gmsh.model.addPhysicalGroup(0, [p4], 18, "loading_point")
gmsh.model.addPhysicalGroup(1, [c10], 19, "sample_location")

# Ensure that all elements are saved in the mesh file, even those not part of physical groups
gmsh.option.setNumber("Mesh.SaveAll", 1)

# Generate the 3D mesh
gmsh.model.mesh.generate(3)

# Save the mesh to a file
gmsh.write("eyeball_3D.msh")

# Uncomment to run Gmsh's built-in GUI (optional)
# gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()

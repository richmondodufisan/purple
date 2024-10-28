import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("3D geometry")

# Set the refinement size
refinement = 0.002 / 30

# Create the sphere by specifying the center point and radius
radius = 0.002
center_x, center_y, center_z = 0, 0, 0
sphere = gmsh.model.occ.addSphere(center_x, center_y, center_z, radius, tag=1)

# Synchronize to make sure the geometry is available before assigning mesh sizes
gmsh.model.occ.synchronize()

# Get all the points of the sphere and apply the mesh size
sphere_entities = gmsh.model.getEntities(0)  # Get all points (0 indicates points)
for entity in sphere_entities:
    gmsh.model.mesh.setSize([entity], refinement)

# Define the loading point at the top of the sphere (north pole)
loading_point = gmsh.model.occ.addPoint(center_x, center_y, center_z + radius, refinement)

# Synchronize to make the point available in the model
gmsh.model.occ.synchronize()

# Add curves (arcs) to the sphere
p_center = gmsh.model.occ.addPoint(center_x, center_y, center_z, refinement)
p_top = gmsh.model.occ.addPoint(center_x, center_y, center_z + radius, refinement)
p_bottom = gmsh.model.occ.addPoint(center_x, center_y, center_z - radius, refinement)
p_front = gmsh.model.occ.addPoint(center_x + radius, center_y, center_z, refinement)
p_back = gmsh.model.occ.addPoint(center_x - radius, center_y, center_z, refinement)
p_right = gmsh.model.occ.addPoint(center_x, center_y + radius, center_z, refinement)
p_left = gmsh.model.occ.addPoint(center_x, center_y - radius, center_z, refinement)

# Create circle arcs between these points (meridians)
arc1 = gmsh.model.occ.addCircleArc(p_top, p_center, p_front)
arc2 = gmsh.model.occ.addCircleArc(p_front, p_center, p_bottom)
arc3 = gmsh.model.occ.addCircleArc(p_top, p_center, p_back)
arc4 = gmsh.model.occ.addCircleArc(p_back, p_center, p_bottom)
arc5 = gmsh.model.occ.addCircleArc(p_top, p_center, p_right)
arc6 = gmsh.model.occ.addCircleArc(p_right, p_center, p_bottom)
arc7 = gmsh.model.occ.addCircleArc(p_top, p_center, p_left)
arc8 = gmsh.model.occ.addCircleArc(p_left, p_center, p_bottom)

# Embed the arcs inside the sphere to ensure nodes are created along them
gmsh.model.occ.fragment([(3, sphere)], [(1, arc1), (1, arc2), (1, arc3), (1, arc4), (1, arc5), (1, arc6), (1, arc7), (1, arc8)])

# Synchronize the embedded geometry
gmsh.model.occ.synchronize()

# Add a physical group for the loading point (explicitly for points, tag = 0)
gmsh.model.addPhysicalGroup(0, [loading_point], 18, "loading_point")

# Add physical group for the arcs (for later referencing)
gmsh.model.addPhysicalGroup(1, [arc1, arc2, arc3, arc4, arc5, arc6, arc7, arc8], 19, "embedded_arcs")

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

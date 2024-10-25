import gmsh

# Initialize Gmsh
gmsh.initialize()
gmsh.model.add("3D geometry")

# Set the refinement size
refinement = 0.002 / 15

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

# Add a physical group for the loading point
gmsh.model.addPhysicalGroup(0, [loading_point], 18, "loading_point")

# Ensure that all elements are saved in the mesh file, even those not part of physical groups
gmsh.option.setNumber("Mesh.SaveAll", 1)

# Generate the 3D mesh
gmsh.model.mesh.generate(3)

# Save the mesh to a file
gmsh.write("eyeball_3D_sphere.msh")

# Uncomment to run Gmsh's built-in GUI (optional)
gmsh.fltk.run()

# Finalize Gmsh
gmsh.finalize()

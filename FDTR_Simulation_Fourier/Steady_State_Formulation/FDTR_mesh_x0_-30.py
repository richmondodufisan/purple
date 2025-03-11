import gmsh

gmsh.initialize()
gmsh.model.add("FDTR_mesh")

newMeshName = "FDTR_mesh_x0_-30.msh"

# Dimensions
x_dir = 160
y_dir = 80
z_dir = 40
radius = 8
trans_thick = 0.09

# Refinement Parameters
dummy_factor = 2
sub_center_ref = 0.09
trans_thick_ref = 0.09
pump_refine = 0.2
reg_element_refine = 20

# 1. Create the **Base Substrate Box**
substrate = gmsh.model.occ.addBox(-x_dir, -y_dir, -z_dir, 2*x_dir, 2*y_dir, z_dir)




# 2. Create the **First (Larger) Hemisphere for Refinement**
large_sphere = gmsh.model.occ.addSphere(0, 0, 0, radius)
cutting_box = gmsh.model.occ.addBox(-radius, -radius, 0, 2*radius, 2*radius, radius)
large_hemisphere = gmsh.model.occ.cut([(3, large_sphere)], [(3, cutting_box)])[0][0]




# 3. Create the **Second (Smaller) Hemisphere for Finer Refinement**
small_radius = radius / dummy_factor
small_sphere = gmsh.model.occ.addSphere(0, 0, 0, small_radius)

# Make the cutting box slightly larger
cutting_box_small = gmsh.model.occ.addBox(-radius-1, -radius-1, -1e-3, 2*radius+2, 2*radius+2, radius+1)

# Perform the cut
cut_result = gmsh.model.occ.cut([(3, small_sphere)], [(3, cutting_box_small)])
if cut_result:
    small_hemisphere = cut_result[0][0]  # Access the first element safely
else:
    raise ValueError("Boolean cut for small hemisphere failed. Check geometry setup.")
    
    



# 4. Create the **Transducer Box (Top Rectangular Volume)**
transducer = gmsh.model.occ.addBox(-x_dir, -y_dir, 0, 2*x_dir, 2*y_dir, trans_thick)

# 5. Create the **Cylindrical Refinement Region in Transducer**
cylinder = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, trans_thick, radius)


# Make mesh coherent & synchronize
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()
# gmsh.fltk.run()



# **Mesh Refinement Assignment Using a Loop**
# Get all points in the model
p = gmsh.model.occ.getEntities(0)

# Loop through each point and determine mesh refinement
for point in p:
    point_id = point[1]
    
    # Get point coordinates
    val = gmsh.model.getValue(0, point_id, [])

    # Compute distance from center
    checkSphere = (val[0])**2 + (val[1])**2 + (val[2])**2
    checkCylinder = (val[0])**2 + (val[1])**2  # Cylinder check only in XY

    # Assign mesh size based on location
    if checkSphere <= ((small_radius)**2 + 1e-2) and val[2] <= 0:
        # Point is inside the **smaller hemisphere**
        gmsh.model.mesh.setSize([point], trans_thick_ref)
    
    elif checkSphere <= ((radius)**2 + 1e-2) and val[2] <= 0:
        # Point is inside the **larger hemisphere**
        gmsh.model.mesh.setSize([point], pump_refine)
    
    elif checkCylinder <= (radius**2 + 1e-2) and (0 <= val[2] <= trans_thick):
        # Point is inside the **cylindrical refinement region**
        gmsh.model.mesh.setSize([point], trans_thick_ref)
    
    else:
        # Default refinement for all other points
        gmsh.model.mesh.setSize([point], reg_element_refine)




# Make mesh coherent & synchronize
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()
# gmsh.fltk.run()


# **Mesh Generation**
gmsh.option.setNumber("Mesh.Algorithm", 5)  # Efficient 3D meshing algorithm
gmsh.model.mesh.generate(3)

# **Write Mesh to File**
gmsh.write(newMeshName)

# **Visualize in Gmsh GUI**
# gmsh.fltk.run()

# Finalize
gmsh.finalize()

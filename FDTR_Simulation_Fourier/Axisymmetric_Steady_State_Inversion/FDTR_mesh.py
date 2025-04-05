import gmsh
import math
import sys

gmsh.initialize()
gmsh.model.add("FDTR_mesh")

newMeshName = "FDTR_mesh.msh"

radius = 8
trans_thick = 0.09


trans_thick_ref = 0.09
sub_center_ref=0.09

x_len = 40
y_len = 40

dummy_factor = 1.6
trans_thick_ref = 0.045
pump_inner_refine = 0.075
pump_outer_refine = 0.2
reg_element_refine = 4


# NB: In axisymmetric case, y axis becomes z axis in MOOSE
# Adding points for base box/substrate, i.e Silicon sample
p1 = gmsh.model.occ.addPoint(0, 0, 0)
p2 = gmsh.model.occ.addPoint(x_len, 0, 0)
p3 = gmsh.model.occ.addPoint(0, -y_len, 0)
p4 = gmsh.model.occ.addPoint(x_len, -y_len, 0)

# Adding lines for base box
c1 = gmsh.model.occ.addLine(p1, p2)
c2 = gmsh.model.occ.addLine(p1, p3)
c3 = gmsh.model.occ.addLine(p3, p4)
c4 = gmsh.model.occ.addLine(p2, p4)


# Adding Surfaces
cloop1 = gmsh.model.occ.addCurveLoop([c1, c2, c3, c4])
s1 = gmsh.model.occ.addPlaneSurface([cloop1])

# Add transducer box
p5 = gmsh.model.occ.addPoint(0, trans_thick, 0)
p6 = gmsh.model.occ.addPoint(x_len, trans_thick, 0)

# Add transducer lines
c5 = gmsh.model.occ.addLine(p1, p5)
c6 = gmsh.model.occ.addLine(p2, p6)
c7 = gmsh.model.occ.addLine(p5, p6)

# Adding transducer surface
cloop2 = gmsh.model.occ.addCurveLoop([c1, c5, c7, c6])
s2 = gmsh.model.occ.addPlaneSurface([cloop2])


##### REFINEMENT DUMMY POINTS #####
# Points for radial refinement dummy surface
p7 = gmsh.model.occ.addPoint(radius, 0, 0)
p8 = gmsh.model.occ.addPoint(0, -radius, 0)

# Make circle arcs for radial refinement
c8 = gmsh.model.occ.addCircleArc(p7, p1, p8)

c9 = gmsh.model.occ.addLine(p1, p7)
c10 = gmsh.model.occ.addLine(p1, p8)

# Make surface loops for semisphere
cloop3 = gmsh.model.occ.addCurveLoop([c8, c9, c10])
s3 = gmsh.model.occ.addPlaneSurface([cloop3])


##### ADDITIONAL SUB-REFINEMENT DUMMY POINTS #####
# Points for radial refinement dummy surface
p9 = gmsh.model.occ.addPoint(radius/dummy_factor, 0, 0)
p10 = gmsh.model.occ.addPoint(0, -radius/dummy_factor, 0)

# Make circle arcs for radial refinement
c11 = gmsh.model.occ.addCircleArc(p9, p1, p10)

c12 = gmsh.model.occ.addLine(p1, p9)
c13 = gmsh.model.occ.addLine(p1, p10)

# Make surface loops for semisphere
cloop4 = gmsh.model.occ.addCurveLoop([c11, c12, c13])
s4 = gmsh.model.occ.addPlaneSurface([cloop4])

# Adding mesh refinement for pump region in transducer
p11 = gmsh.model.occ.addPoint(radius, trans_thick, 0)

c14 = gmsh.model.occ.addLine(p5, p11)
c15 = gmsh.model.occ.addLine(p7, p11)

cloop5 = gmsh.model.occ.addCurveLoop([c5, c14, c15, c9])
s5 = gmsh.model.occ.addPlaneSurface([cloop5])

# Adding mesh sub-refinement for pump region in transducer
p12 = gmsh.model.occ.addPoint(radius/dummy_factor, trans_thick, 0)

c16 = gmsh.model.occ.addLine(p5, p12)
c17 = gmsh.model.occ.addLine(p9, p12)

cloop6 = gmsh.model.occ.addCurveLoop([c12, c17, c16, c5])
s6 = gmsh.model.occ.addPlaneSurface([cloop6])


gmsh.model.occ.synchronize()

# # EMBED Dummy Points in Mesh

gmsh.model.mesh.embed(2, [s3], 2, s1)
gmsh.model.mesh.embed(2, [s4], 2, s1)

gmsh.model.mesh.embed(2, [s5], 2, s2)
gmsh.model.mesh.embed(2, [s6], 2, s2)

# Make mesh coherent
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

# assign mesh size at all points without a mesh size constraint
p = gmsh.model.occ.getEntities(0)

# Loop through each point and determine mesh refinement
for point in p:
    point_id = point[1]
    
    # Get point coordinates
    val = gmsh.model.getValue(0, point_id, [])

    # Compute distances from center
    checkSphere = (val[0])**2 + (val[1])**2
    checkOuterCylinder = (val[0])**2   # Outer cylinder check in XY
    checkInnerCylinder = (val[0])**2   # Inner cylinder check in XY
    
    small_radius = radius/dummy_factor

    # Assign mesh size based on location
    if checkSphere <= ((small_radius)**2 + 1e-2) and val[1] <= 0:
        # Point is inside the **smaller hemisphere**
        gmsh.model.mesh.setSize([point], pump_inner_refine)
    
    elif checkSphere <= ((radius)**2 + 1e-2) and val[1] <= 0:
        # Point is inside the **larger hemisphere**
        gmsh.model.mesh.setSize([point], pump_outer_refine)
    
    elif checkInnerCylinder <= (small_radius**2 + 1e-2) and (0 <= val[1] <= trans_thick):
        # Point is inside the **inner cylindrical refinement region**
        gmsh.model.mesh.setSize([point], trans_thick_ref)
    
    elif checkOuterCylinder <= (radius**2 + 1e-2) and (0 <= val[1] <= trans_thick):
        # Point is inside the **outer cylindrical refinement region**
        gmsh.model.mesh.setSize([point], trans_thick_ref)
    
    else:
        # Default refinement for all other points
        gmsh.model.mesh.setSize([point], reg_element_refine)
   

# More efficient meshing algorithm used when there are multiple subvolumes
gmsh.option.setNumber("Mesh.Algorithm",5)

# Create 2D mesh
gmsh.model.mesh.generate(2)

gmsh.write(newMeshName)

gmsh.fltk.run()


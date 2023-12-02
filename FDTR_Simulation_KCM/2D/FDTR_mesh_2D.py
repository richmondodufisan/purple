import gmsh
import math
import sys

gmsh.initialize()
gmsh.model.add("FDTR_mesh")

newMeshName = "FDTR_mesh_x0_-15_theta_0.msh"

theta = 0
xcen = 0
ycen = 0
radius = 8
trans_thick = 0.09

dummy_factor = 3
trans_thick_ref = 0.09
sub_center_ref=0.09

x_dir = 40
y_dir = 40
gb_width = 0.1

pump_refine = 0.4
reg_element_refine = 6
gb_refine = 0.8

# Initialize gb refinement values
x_left_up = 0
x_right_up = 0
y_left_up = 0
y_right_up = 0

x_left_down = 0
x_right_down = 0
y_left_down = 0
y_right_down = 0

###### Calculation for grain boundary refinement #######

theta_rad = ((90.0 - theta) * 3.14159265359)/(180)
theta_rad_og = (theta * 3.14159265359)/(180)
tan_theta = -1.0*math.tan(theta_rad)
cos_theta = math.cos(theta_rad_og)


# Refine region ny a multiple of the grain boundary size to the left and right
width_refine = 10
part_width = (gb_width/cos_theta)*width_refine

x_left_up = -part_width/2.0
x_right_up = part_width/2.0

# Check for zero angle
is_angle_zero = ((-1e-8 <= theta) and (theta <= 1e-8))

# Get x and y coordinates for LEFT side
if (is_angle_zero):
    x_left_down = x_left_up
    y_left_down = -y_dir
else:
    x_left_down = (1.0/tan_theta)*(-y_dir + (tan_theta*x_left_up))
    y_left_down = -y_dir
    
if (x_left_down >= x_dir):
    x_left_down = x_dir
    y_left_down = (tan_theta*x_dir)-(tan_theta*x_left_up)

# Get x and y coordinates for RIGHT side
if (is_angle_zero):
    x_right_down = x_right_up
    y_right_down = -y_dir
else:
    x_right_down = (1.0/tan_theta)*(-y_dir + (tan_theta*x_right_up))
    y_right_down = -y_dir
    
if (x_right_down >= x_dir):
    x_right_down = x_dir
    y_right_down = (tan_theta*x_dir)-(tan_theta*x_right_up)

y_left_up = 0
y_right_up = 0

###### END grain boundary refinement calculations #######



# Adding points for base box/substrate, i.e Silicon sample
p1 = gmsh.model.occ.addPoint(x_dir, 0, 0, reg_element_refine)
p2 = gmsh.model.occ.addPoint(-x_dir, 0, 0, reg_element_refine)
p3 = gmsh.model.occ.addPoint(x_dir, -y_dir, 0, reg_element_refine)
p4 = gmsh.model.occ.addPoint(-x_dir, -y_dir, 0, reg_element_refine)

# Adding lines for base box
c1 = gmsh.model.occ.addLine(p1, p2)
c2 = gmsh.model.occ.addLine(p2, p4)
c3 = gmsh.model.occ.addLine(p1, p3)
c4 = gmsh.model.occ.addLine(p3, p4)

# Adding substrate surface
cloop1 = gmsh.model.occ.addCurveLoop([c1, c2, c3, c4])
s1 = gmsh.model.occ.addPlaneSurface([cloop1])

# Adding transducer box points
p5 = gmsh.model.occ.addPoint(x_dir, trans_thick, 0, reg_element_refine)
p6 = gmsh.model.occ.addPoint(-x_dir, trans_thick, 0, reg_element_refine)

# Add transducer lines
c5 = gmsh.model.occ.addLine(p1, p5)
c6 = gmsh.model.occ.addLine(p2, p6)
c7 = gmsh.model.occ.addLine(p5, p6)

# Adding transudcer surface
cloop2 = gmsh.model.occ.addCurveLoop([c1, c5, c6, c7])
s2 = gmsh.model.occ.addPlaneSurface([cloop2])

# Points for radial refinement dummy volume
p7 = gmsh.model.occ.addPoint(xcen, 0, 0, sub_center_ref)
p8 = gmsh.model.occ.addPoint(xcen+radius, 0, 0, pump_refine)
p9 = gmsh.model.occ.addPoint(xcen-radius, 0, 0, pump_refine)
p10 = gmsh.model.occ.addPoint(xcen, 0-radius, 0, pump_refine)

# Make circle arcs for radial refinement
c8 = gmsh.model.occ.addLine(p8, p9)
c9 = gmsh.model.occ.addCircleArc(p8, p7, p10)
c10 = gmsh.model.occ.addCircleArc(p9, p7, p10)

# Make semicircle surface
cloop3 = gmsh.model.occ.addCurveLoop([c8, c9, c10])
s3 = gmsh.model.occ.addPlaneSurface([cloop3])

##### ADDITIONAL SUB-CIRCLE REFINEMENT DUMMY POINTS #####
p11 = gmsh.model.occ.addPoint(xcen+(radius/dummy_factor), 0, 0, sub_center_ref)
p12 = gmsh.model.occ.addPoint(xcen-(radius/dummy_factor), 0, 0, sub_center_ref)
p13 = gmsh.model.occ.addPoint(xcen, 0-(radius/dummy_factor), 0, sub_center_ref)

c11 = gmsh.model.occ.addLine(p11, p12)
c12 = gmsh.model.occ.addCircleArc(p11, p7, p13)
c13 = gmsh.model.occ.addCircleArc(p12, p7, p13)

cloop4 = gmsh.model.occ.addCurveLoop([c11, c12, c13])
s4 = gmsh.model.occ.addPlaneSurface([cloop4])

##### END SUB-CIRCLE DUMMY REFINEMENT #####

# Adding points for grain boundary refinement dummy volume
p14 = gmsh.model.occ.addPoint(x_left_up, y_left_up, 0, gb_refine)
p15 = gmsh.model.occ.addPoint(x_right_up, y_right_up, 0, gb_refine)
p16 = gmsh.model.occ.addPoint(x_left_down, y_right_down, 0, gb_refine)
p17 = gmsh.model.occ.addPoint(x_right_down, y_right_down, 0, gb_refine)

# Adding lines..
c14 = gmsh.model.occ.addLine(p14, p15)
c15 = gmsh.model.occ.addLine(p16, p17)
c16 = gmsh.model.occ.addLine(p14, p16)
c17 = gmsh.model.occ.addLine(p15, p17)

# Surface
cloop5 = gmsh.model.occ.addCurveLoop([c14, c16, c15, c17])
s5 = gmsh.model.occ.addPlaneSurface([cloop5])

# Adding mesh refinement for pump region in transducer
p18 = gmsh.model.occ.addPoint(xcen+radius, 0, 0, pump_refine)
p19 = gmsh.model.occ.addPoint(xcen-radius, 0, 0, pump_refine)
p20 = gmsh.model.occ.addPoint(xcen+radius, trans_thick, 0, pump_refine)
p21 = gmsh.model.occ.addPoint(xcen-radius, trans_thick, 0, pump_refine)

# Adding lines
c18 = gmsh.model.occ.addLine(p18, p19)
c19 = gmsh.model.occ.addLine(p20, p21)
c20 = gmsh.model.occ.addLine(p18, p20)
c21 = gmsh.model.occ.addLine(p19, p21)

# Surface
cloop6 = gmsh.model.occ.addCurveLoop([c18, c20, c19, c21])
s6 = gmsh.model.occ.addPlaneSurface([cloop6])

##### TRANSDUCER DUMMY SUB-SURFACE #####

p22 = gmsh.model.occ.addPoint(xcen+(radius/dummy_factor), 0, 0, trans_thick_ref)
p23 = gmsh.model.occ.addPoint(xcen-(radius/dummy_factor), 0, 0, trans_thick_ref)
p24 = gmsh.model.occ.addPoint(xcen+(radius/dummy_factor), trans_thick, 0, trans_thick_ref)
p25 = gmsh.model.occ.addPoint(xcen-(radius/dummy_factor), trans_thick, 0, trans_thick_ref)

c22 = gmsh.model.occ.addLine(p22, p23)
c23 = gmsh.model.occ.addLine(p24, p25)
c24 = gmsh.model.occ.addLine(p22, p24)
c25 = gmsh.model.occ.addLine(p23, p25)

cloop7 = gmsh.model.occ.addCurveLoop([c22, c24, c23, c25])
s7 = gmsh.model.occ.addPlaneSurface([cloop7])

##### END TRANSDUCER DUMMY SUB-SURFACE #####

gmsh.model.occ.synchronize()

# EMBED Dummy Points in Mesh
gmsh.model.mesh.embed(0, [p7], 2, s3)

gmsh.model.mesh.embed(2, [s6], 2, s3)
gmsh.model.mesh.embed(2, [s7], 2, s5)

# Make mesh coherent
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()

# assign mesh size at all points without a mesh size constraint
p = gmsh.model.occ.getEntities(0)
s = gmsh.model.mesh.getSizes(p)
for ps in zip(p, s):
    # get coordinates of newly created points
    val = gmsh.model.getValue(0, ps[0][1], [])
    
    # check if they are within the radius of the small sphere
    checkSphere = ((val[0])**2 + (val[1])**2 + (val[2])**2)
    # checkCylinder = ((val[0])**2 + (val[1])**2 + (val[2]-0.09)**2)
    print(val)
    
    # assign small sphere refinement if yes, large sphere refinement otherwise
    if (( checkSphere <= ((radius/dummy_factor)**2 + 1e-2)) and ((val[1]) <= 0)):
        gmsh.model.mesh.setSize([ps[0]], trans_thick_ref)
    elif (( checkSphere <= ((radius)**2 + 1e-2)) and ((val[1]) <= 0)):
        gmsh.model.mesh.setSize([ps[0]], pump_refine)

# More efficient meshing algorithm used when there are multiple subvolumes
gmsh.option.setNumber("Mesh.Algorithm",5)

# Create 2D mesh
gmsh.model.mesh.generate(2)

# gmsh.write(newMeshName)

gmsh.fltk.run()

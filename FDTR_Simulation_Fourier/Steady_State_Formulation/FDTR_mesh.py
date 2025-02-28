import gmsh
import math
import sys

gmsh.initialize()
gmsh.model.add("FDTR_mesh")

newMeshName = "FDTR_mesh.msh"

xcen = 0
ycen = 0
radius = 7.5
trans_thick = 0.09

dummy_factor = 2
trans_thick_ref = 0.09
sub_center_ref = 0.09

x_dir = 160
y_dir = 80
z_dir = 40

pump_refine = 0.09
reg_element_refine = 25



# Adding points for base box/substrate, i.e Silicon sample
p1 = gmsh.model.occ.addPoint(x_dir, y_dir, trans_thick, reg_element_refine)
p2 = gmsh.model.occ.addPoint(x_dir, -y_dir, trans_thick, reg_element_refine)
p3 = gmsh.model.occ.addPoint(-x_dir, -y_dir, trans_thick, reg_element_refine)
p4 = gmsh.model.occ.addPoint(-x_dir, y_dir, trans_thick, reg_element_refine)
p5 = gmsh.model.occ.addPoint(-x_dir, y_dir, -z_dir, reg_element_refine)
p6 = gmsh.model.occ.addPoint(-x_dir, -y_dir, -z_dir, reg_element_refine)
p7 = gmsh.model.occ.addPoint(x_dir, -y_dir, -z_dir, reg_element_refine)
p8 = gmsh.model.occ.addPoint(x_dir, y_dir, -z_dir, reg_element_refine)

# Adding lines for base box
c1 = gmsh.model.occ.addLine(p3, p2)
c2 = gmsh.model.occ.addLine(p3, p6)
c3 = gmsh.model.occ.addLine(p6, p7)
c4 = gmsh.model.occ.addLine(p7, p2)
c5 = gmsh.model.occ.addLine(p6, p5)
c6 = gmsh.model.occ.addLine(p5, p8)
c7 = gmsh.model.occ.addLine(p8, p7)
c8 = gmsh.model.occ.addLine(p8, p1)
c9 = gmsh.model.occ.addLine(p1, p2)
c10 = gmsh.model.occ.addLine(p3, p4)
c11 = gmsh.model.occ.addLine(p4, p5)
c12 = gmsh.model.occ.addLine(p4, p1)

# Adding Surfaces
cloop1 = gmsh.model.occ.addCurveLoop([c10, c11, c5, c2])
s1 = gmsh.model.occ.addPlaneSurface([cloop1])
cloop2 = gmsh.model.occ.addCurveLoop([c3, c4, -c1, c2])
s2 = gmsh.model.occ.addPlaneSurface([cloop2])
cloop3 = gmsh.model.occ.addCurveLoop([c7, c4, -c9, -c8])
s3 = gmsh.model.occ.addPlaneSurface([cloop3])
cloop4 = gmsh.model.occ.addCurveLoop([c6, c7, -c3, c5])
s4 = gmsh.model.occ.addPlaneSurface([cloop4])
cloop5 = gmsh.model.occ.addCurveLoop([c6, c8, -c12, c11])
s5 = gmsh.model.occ.addPlaneSurface([cloop5])
cloop6 = gmsh.model.occ.addCurveLoop([c1, -c9, -c12, -c10])
s6 = gmsh.model.occ.addPlaneSurface([cloop6])


# Substrate volume
sloop1 = gmsh.model.occ.addSurfaceLoop([s6, s2, s4, s5, s3, s1])
v1 = gmsh.model.occ.addVolume([sloop1])


# Points for radial refinement dummy volume
p13 = gmsh.model.occ.addPoint(xcen, ycen, trans_thick, sub_center_ref)
p14 = gmsh.model.occ.addPoint(xcen, ycen+radius, trans_thick, pump_refine)
p15 = gmsh.model.occ.addPoint(xcen, ycen-radius, trans_thick, pump_refine)
p16 = gmsh.model.occ.addPoint(xcen+radius, ycen, trans_thick, pump_refine)
p17 = gmsh.model.occ.addPoint(xcen-radius, ycen, trans_thick, pump_refine)
p18 = gmsh.model.occ.addPoint(xcen, ycen, trans_thick-radius, pump_refine)

# Make circle arcs for radial refinement
c21 = gmsh.model.occ.addCircleArc(p17, p13, p15)
c22 = gmsh.model.occ.addCircleArc(p15, p13, p16)
c23 = gmsh.model.occ.addCircleArc(p16, p13, p14)
c24 = gmsh.model.occ.addCircleArc(p17, p13, p14)
c25 = gmsh.model.occ.addCircleArc(p17, p13, p18)
c26 = gmsh.model.occ.addCircleArc(p15, p13, p18)
c27 = gmsh.model.occ.addCircleArc(p16, p13, p18)
c28 = gmsh.model.occ.addCircleArc(p14, p13, p18)

# Make surface loops for semisphere
cloop12 = gmsh.model.occ.addCurveLoop([c21, c22, c23, c24])
s12 = gmsh.model.occ.addPlaneSurface([cloop12])
cloop13 = gmsh.model.occ.addCurveLoop([c25, c26, c21])
s13 = gmsh.model.occ.addSurfaceFilling(cloop13)
cloop14 = gmsh.model.occ.addCurveLoop([c22, c27, c26])
s14 = gmsh.model.occ.addSurfaceFilling(cloop14)
cloop15 = gmsh.model.occ.addCurveLoop([c23, c28, c27])
s15 = gmsh.model.occ.addSurfaceFilling(cloop15)
cloop16 = gmsh.model.occ.addCurveLoop([c24, c28, c25])
s16 = gmsh.model.occ.addSurfaceFilling(cloop16)

# Make semisphere volume
sloop3 = gmsh.model.occ.addSurfaceLoop([s12, s13, s14, s15, s16])
v3 = gmsh.model.occ.addVolume([sloop3])

##### ADDITIONAL SUB-SPHERE REFINEMENT DUMMY POINTS #####
p36 = gmsh.model.occ.addPoint(xcen, ycen+(radius/dummy_factor), trans_thick, sub_center_ref)
p37 = gmsh.model.occ.addPoint(xcen, ycen-(radius/dummy_factor), trans_thick, sub_center_ref)
p38 = gmsh.model.occ.addPoint(xcen+(radius/dummy_factor), ycen, trans_thick, sub_center_ref)
p39 = gmsh.model.occ.addPoint(xcen-(radius/dummy_factor), ycen, trans_thick, sub_center_ref)
p40 = gmsh.model.occ.addPoint(xcen, ycen, trans_thick-(radius/dummy_factor), sub_center_ref)

c49 = gmsh.model.occ.addCircleArc(p39, p13, p37)
c50 = gmsh.model.occ.addCircleArc(p37, p13, p38)
c51 = gmsh.model.occ.addCircleArc(p38, p13, p36)
c52 = gmsh.model.occ.addCircleArc(p39, p13, p36)
c53 = gmsh.model.occ.addCircleArc(p39, p13, p40)
c54 = gmsh.model.occ.addCircleArc(p37, p13, p40)
c55 = gmsh.model.occ.addCircleArc(p38, p13, p40)
c56 = gmsh.model.occ.addCircleArc(p36, p13, p40)

cloop28 = gmsh.model.occ.addCurveLoop([c49, c50, c51, c52])
s28 = gmsh.model.occ.addPlaneSurface([cloop28])
cloop29 = gmsh.model.occ.addCurveLoop([c53, c54, c49])
s29 = gmsh.model.occ.addSurfaceFilling(cloop29)
cloop30 = gmsh.model.occ.addCurveLoop([c50, c55, c54])
s30 = gmsh.model.occ.addSurfaceFilling(cloop30)
cloop31 = gmsh.model.occ.addCurveLoop([c51, c56, c55])
s31 = gmsh.model.occ.addSurfaceFilling(cloop31)
cloop32 = gmsh.model.occ.addCurveLoop([c52, c56, c53])
s32 = gmsh.model.occ.addSurfaceFilling(cloop32)

sloop6 = gmsh.model.occ.addSurfaceLoop([s28, s29, s30, s31, s32])
v6 = gmsh.model.occ.addVolume([sloop6])

##### END SUB-SPHERE DUMMY REFINEMENT #####

gmsh.model.occ.synchronize()

# Make mesh coherent
gmsh.model.occ.removeAllDuplicates()
gmsh.model.occ.synchronize()


# assign mesh size at all points without a mesh size constraint
p = gmsh.model.occ.getEntities(0)
s = gmsh.model.mesh.getSizes(p)
for ps in zip(p, s):
    if ps[1] == 0:
        # get coordinates of newly created points
        val = gmsh.model.getValue(0, ps[0][1], [])
        
        # check if they are within the radius of the small sphere
        checkSphere = ((val[0])**2 + (val[1])**2 + (val[2])**2)
        # checkCylinder = ((val[0])**2 + (val[1])**2 + (val[2]-0.09)**2)
        # print(checkSphere)
        
        # assign small sphere refinement if yes, large sphere refinement otherwise
        if (( checkSphere <= ((radius/dummy_factor)**2 + 1e-2)) and ((val[2]) <= 0)):
            gmsh.model.mesh.setSize([ps[0]], trans_thick_ref)
        else:
            gmsh.model.mesh.setSize([ps[0]], pump_refine)
   


gmsh.option.setNumber("Mesh.Algorithm", 5)

# Create 3D mesh
gmsh.model.mesh.generate(3)

gmsh.write(newMeshName)

# gmsh.fltk.run()

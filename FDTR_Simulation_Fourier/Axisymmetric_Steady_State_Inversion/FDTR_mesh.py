import gmsh
import math
import sys

gmsh.initialize()
gmsh.model.add("FDTR_mesh")

newMeshName = "FDTR_mesh.msh"

radius = 8
trans_thick = 0.133

dummy_factor = 2
trans_thick_ref = 0.2
sub_center_ref=0.2

x_len = 40
z_len = 40

pump_refine = 1.5
reg_element_refine = 4



# Adding points for base box/substrate, i.e Silicon sample
p1 = gmsh.model.occ.addPoint(0, 0, 0, sub_center_ref)
p2 = gmsh.model.occ.addPoint(x_len, 0, 0, reg_element_refine)
p3 = gmsh.model.occ.addPoint(0, 0, -z_len, reg_element_refine)
p4 = gmsh.model.occ.addPoint(x_len, 0, -z_len, reg_element_refine)

# Adding lines for base box
c1 = gmsh.model.occ.addLine(p1, p2)
c2 = gmsh.model.occ.addLine(p1, p3)
c3 = gmsh.model.occ.addLine(p3, p4)
c4 = gmsh.model.occ.addLine(p2, p4)


# Adding Surfaces
cloop1 = gmsh.model.occ.addCurveLoop([c1, c2, c3, c4])
s1 = gmsh.model.occ.addPlaneSurface([cloop1])

# Add transducer box
p5 = gmsh.model.occ.addPoint(0, 0, trans_thick, sub_center_ref)
p6 = gmsh.model.occ.addPoint(x_len, 0, trans_thick, reg_element_refine)

# Add transducer lines
c5 = gmsh.model.occ.addLine(p1, p5)
c6 = gmsh.model.occ.addLine(p2, p6)
c7 = gmsh.model.occ.addLine(p5, p6)

# Adding transducer surface
cloop2 = gmsh.model.occ.addCurveLoop([c1, c5, c7, c6])
s2 = gmsh.model.occ.addPlaneSurface([cloop2])


##### REFINEMENT DUMMY POINTS #####
# Points for radial refinement dummy surface
p7 = gmsh.model.occ.addPoint(radius, 0, 0, pump_refine)
p8 = gmsh.model.occ.addPoint(0, 0, -radius, pump_refine)


# Make circle arcs for radial refinement
c8 = gmsh.model.occ.addCircleArc(p7, p1, p8)

c9 = gmsh.model.occ.addLine(p1, p7)
c10 = gmsh.model.occ.addLine(p1, p8)

# Make surface loops for semisphere
cloop3 = gmsh.model.occ.addCurveLoop([c8, c9, c10])
s3 = gmsh.model.occ.addPlaneSurface([cloop3])


##### ADDITIONAL SUB-REFINEMENT DUMMY POINTS #####
# Points for radial refinement dummy surface
p9 = gmsh.model.occ.addPoint(radius/dummy_factor, 0, 0, sub_center_ref)
p10 = gmsh.model.occ.addPoint(0, 0, -radius/dummy_factor, sub_center_ref)


# Make circle arcs for radial refinement
c11 = gmsh.model.occ.addCircleArc(p9, p1, p10)

c12 = gmsh.model.occ.addLine(p1, p9)
c13 = gmsh.model.occ.addLine(p1, p10)

# Make surface loops for semisphere
cloop4 = gmsh.model.occ.addCurveLoop([c11, c12, c13])
s4 = gmsh.model.occ.addPlaneSurface([cloop4])





# Adding mesh refinement for pump region in transducer
p11 = gmsh.model.occ.addPoint(radius, 0, trans_thick, pump_refine)

c14 = gmsh.model.occ.addLine(p5, p11)
c15 = gmsh.model.occ.addLine(p7, p11)

cloop5 = gmsh.model.occ.addCurveLoop([c5, c14, c15, c9])
s5 = gmsh.model.occ.addPlaneSurface([cloop5])




# Adding mesh sub-refinement for pump region in transducer
p12 = gmsh.model.occ.addPoint(radius/dummy_factor, 0, trans_thick, sub_center_ref)

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
        if (( checkSphere <= ((radius/dummy_factor)**2 + 1e-2))):
            gmsh.model.mesh.setSize([ps[0]], trans_thick_ref)
        else:
            gmsh.model.mesh.setSize([ps[0]], pump_refine)
   

# More efficient meshing algorithm used when there are multiple subvolumes
gmsh.option.setNumber("Mesh.Algorithm",5)

# Create 2D mesh
gmsh.model.mesh.generate(2)

gmsh.write(newMeshName)

# gmsh.fltk.run()


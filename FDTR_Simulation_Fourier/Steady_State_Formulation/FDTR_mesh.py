import gmsh
import math
import sys

gmsh.initialize()

# Set the number of threads for meshing
gmsh.option.setNumber("General.NumThreads", 20)

gmsh.model.add("FDTR_mesh")

newMeshName = "FDTR_mesh.msh"

xcen = 0
ycen = 0
radius = 8
trans_thick = 5

dummy_factor = 2
trans_thick_ref = 0.09
sub_center_ref= 0.09

x_dir = 160
y_dir = 80
z_dir = 40

pump_refine = 0.09
reg_element_refine = 10



# # Adding points for base box/substrate, i.e Silicon sample
# p1 = gmsh.model.occ.addPoint(x_dir, y_dir, 0, reg_element_refine)
# p2 = gmsh.model.occ.addPoint(x_dir, -y_dir, 0, reg_element_refine)
# p3 = gmsh.model.occ.addPoint(-x_dir, -y_dir, 0, reg_element_refine)
# p4 = gmsh.model.occ.addPoint(-x_dir, y_dir, 0, reg_element_refine)
# p5 = gmsh.model.occ.addPoint(-x_dir, y_dir, -z_dir, reg_element_refine)
# p6 = gmsh.model.occ.addPoint(-x_dir, -y_dir, -z_dir, reg_element_refine)
# p7 = gmsh.model.occ.addPoint(x_dir, -y_dir, -z_dir, reg_element_refine)
# p8 = gmsh.model.occ.addPoint(x_dir, y_dir, -z_dir, reg_element_refine)

# # Adding lines for base box
# c1 = gmsh.model.occ.addLine(p3, p2)
# c2 = gmsh.model.occ.addLine(p3, p6)
# c3 = gmsh.model.occ.addLine(p6, p7)
# c4 = gmsh.model.occ.addLine(p7, p2)
# c5 = gmsh.model.occ.addLine(p6, p5)
# c6 = gmsh.model.occ.addLine(p5, p8)
# c7 = gmsh.model.occ.addLine(p8, p7)
# c8 = gmsh.model.occ.addLine(p8, p1)
# c9 = gmsh.model.occ.addLine(p1, p2)
# c10 = gmsh.model.occ.addLine(p3, p4)
# c11 = gmsh.model.occ.addLine(p4, p5)
# c12 = gmsh.model.occ.addLine(p4, p1)

# # Adding Surfaces
# cloop1 = gmsh.model.occ.addCurveLoop([c10, c11, c5, c2])
# s1 = gmsh.model.occ.addPlaneSurface([cloop1])
# cloop2 = gmsh.model.occ.addCurveLoop([c3, c4, -c1, c2])
# s2 = gmsh.model.occ.addPlaneSurface([cloop2])
# cloop3 = gmsh.model.occ.addCurveLoop([c7, c4, -c9, -c8])
# s3 = gmsh.model.occ.addPlaneSurface([cloop3])
# cloop4 = gmsh.model.occ.addCurveLoop([c6, c7, -c3, c5])
# s4 = gmsh.model.occ.addPlaneSurface([cloop4])
# cloop5 = gmsh.model.occ.addCurveLoop([c6, c8, -c12, c11])
# s5 = gmsh.model.occ.addPlaneSurface([cloop5])
# cloop6 = gmsh.model.occ.addCurveLoop([c1, -c9, -c12, -c10])
# s6 = gmsh.model.occ.addPlaneSurface([cloop6])



# # Substrate volume
# sloop1 = gmsh.model.occ.addSurfaceLoop([s6, s2, s4, s5, s3, s1])
# v1 = gmsh.model.occ.addVolume([sloop1])






# #################### SUBSTRATE SUBVOLUME ######################

# # Points for radial refinement dummy volume
# p13 = gmsh.model.occ.addPoint(xcen, ycen, 0, sub_center_ref)
# p14 = gmsh.model.occ.addPoint(xcen, ycen+radius, 0, pump_refine)
# p15 = gmsh.model.occ.addPoint(xcen, ycen-radius, 0, pump_refine)
# p16 = gmsh.model.occ.addPoint(xcen+radius, ycen, 0, pump_refine)
# p17 = gmsh.model.occ.addPoint(xcen-radius, ycen, 0, pump_refine)
# p18 = gmsh.model.occ.addPoint(xcen, ycen, 0-radius, pump_refine)

# # Make circle arcs for radial refinement
# c21 = gmsh.model.occ.addCircleArc(p17, p13, p15)
# c22 = gmsh.model.occ.addCircleArc(p15, p13, p16)
# c23 = gmsh.model.occ.addCircleArc(p16, p13, p14)
# c24 = gmsh.model.occ.addCircleArc(p17, p13, p14)
# c25 = gmsh.model.occ.addCircleArc(p17, p13, p18)
# c26 = gmsh.model.occ.addCircleArc(p15, p13, p18)
# c27 = gmsh.model.occ.addCircleArc(p16, p13, p18)
# c28 = gmsh.model.occ.addCircleArc(p14, p13, p18)

# # Make surface loops for semisphere
# cloop12 = gmsh.model.occ.addCurveLoop([c21, c22, c23, c24])
# s12 = gmsh.model.occ.addPlaneSurface([cloop12])
# cloop13 = gmsh.model.occ.addCurveLoop([c25, c26, c21])
# s13 = gmsh.model.occ.addSurfaceFilling(cloop13)
# cloop14 = gmsh.model.occ.addCurveLoop([c22, c27, c26])
# s14 = gmsh.model.occ.addSurfaceFilling(cloop14)
# cloop15 = gmsh.model.occ.addCurveLoop([c23, c28, c27])
# s15 = gmsh.model.occ.addSurfaceFilling(cloop15)
# cloop16 = gmsh.model.occ.addCurveLoop([c24, c28, c25])
# s16 = gmsh.model.occ.addSurfaceFilling(cloop16)

# # Make semisphere volume
# sloop3 = gmsh.model.occ.addSurfaceLoop([s12, s13, s14, s15, s16])
# v3 = gmsh.model.occ.addVolume([sloop3])

# #################### END SUBSTRATE SUBVOLUME ######################





# ############### ADDITIONAL SUBSTRATE SUBVOLUME #################
# p36 = gmsh.model.occ.addPoint(xcen, ycen+(radius/dummy_factor), 0, sub_center_ref)
# p37 = gmsh.model.occ.addPoint(xcen, ycen-(radius/dummy_factor), 0, sub_center_ref)
# p38 = gmsh.model.occ.addPoint(xcen+(radius/dummy_factor), ycen, 0, sub_center_ref)
# p39 = gmsh.model.occ.addPoint(xcen-(radius/dummy_factor), ycen, 0, sub_center_ref)
# p40 = gmsh.model.occ.addPoint(xcen, ycen, 0-(radius/dummy_factor), sub_center_ref)

# c49 = gmsh.model.occ.addCircleArc(p39, p13, p37)
# c50 = gmsh.model.occ.addCircleArc(p37, p13, p38)
# c51 = gmsh.model.occ.addCircleArc(p38, p13, p36)
# c52 = gmsh.model.occ.addCircleArc(p39, p13, p36)
# c53 = gmsh.model.occ.addCircleArc(p39, p13, p40)
# c54 = gmsh.model.occ.addCircleArc(p37, p13, p40)
# c55 = gmsh.model.occ.addCircleArc(p38, p13, p40)
# c56 = gmsh.model.occ.addCircleArc(p36, p13, p40)

# cloop28 = gmsh.model.occ.addCurveLoop([c49, c50, c51, c52])
# s28 = gmsh.model.occ.addPlaneSurface([cloop28])
# cloop29 = gmsh.model.occ.addCurveLoop([c53, c54, c49])
# s29 = gmsh.model.occ.addSurfaceFilling(cloop29)
# cloop30 = gmsh.model.occ.addCurveLoop([c50, c55, c54])
# s30 = gmsh.model.occ.addSurfaceFilling(cloop30)
# cloop31 = gmsh.model.occ.addCurveLoop([c51, c56, c55])
# s31 = gmsh.model.occ.addSurfaceFilling(cloop31)
# cloop32 = gmsh.model.occ.addCurveLoop([c52, c56, c53])
# s32 = gmsh.model.occ.addSurfaceFilling(cloop32)

# sloop4 = gmsh.model.occ.addSurfaceLoop([s28, s29, s30, s31, s32])
# v4 = gmsh.model.occ.addVolume([sloop4])

# ############# END SUB-SPHERE DUMMY REFINEMENT ####################



# result = gmsh.model.occ.cut([(3, v1)], [(3, v3)], removeTool=False)
# if result[0]:  # Ensure subtraction was successful
    # v1 = result[0][0]  # Store the new volume tag

# result = gmsh.model.occ.cut([(3, v3)], [(3, v4)], removeTool=False)
# if result[0]:
    # v3 = result[0][0]





# gmsh.model.occ.synchronize()
# gmsh.fltk.run()





# Add transducer box
p1_tran = gmsh.model.occ.addPoint(x_dir, y_dir, 0, reg_element_refine)
p2_tran = gmsh.model.occ.addPoint(x_dir, -y_dir, 0, reg_element_refine)
p3_tran = gmsh.model.occ.addPoint(-x_dir, -y_dir, 0, reg_element_refine)
p4_tran = gmsh.model.occ.addPoint(-x_dir, y_dir, 0, reg_element_refine)

p9_tran = gmsh.model.occ.addPoint(x_dir, y_dir, trans_thick, reg_element_refine)
p10_tran = gmsh.model.occ.addPoint(x_dir, -y_dir, trans_thick, reg_element_refine)
p11_tran = gmsh.model.occ.addPoint(-x_dir, -y_dir, trans_thick, reg_element_refine)
p12_tran = gmsh.model.occ.addPoint(-x_dir, y_dir, trans_thick, reg_element_refine)

# Add transducer lines
c1_tran = gmsh.model.occ.addLine(p3_tran, p2_tran)
c9_tran = gmsh.model.occ.addLine(p1_tran, p2_tran)
c10_tran = gmsh.model.occ.addLine(p3_tran, p4_tran)
c12_tran = gmsh.model.occ.addLine(p4_tran, p1_tran)


c13_tran = gmsh.model.occ.addLine(p9_tran, p10_tran)
c14_tran = gmsh.model.occ.addLine(p10_tran, p11_tran)
c15_tran = gmsh.model.occ.addLine(p11_tran, p12_tran)
c16_tran = gmsh.model.occ.addLine(p12_tran, p9_tran)
c17_tran = gmsh.model.occ.addLine(p11_tran, p3_tran)
c18_tran = gmsh.model.occ.addLine(p12_tran, p4_tran)
c19_tran = gmsh.model.occ.addLine(p10_tran, p2_tran)
c20_tran = gmsh.model.occ.addLine(p9_tran, p1_tran)

# Adding surfaces
cloop6_tran = gmsh.model.occ.addCurveLoop([c1_tran, c9_tran, c12_tran, c10_tran])
s6_tran = gmsh.model.occ.addPlaneSurface([cloop6_tran])

cloop7_tran = gmsh.model.occ.addCurveLoop([c10_tran, c18_tran, c15_tran, c17_tran])
s7_tran = gmsh.model.occ.addPlaneSurface([cloop7_tran])
cloop8_tran = gmsh.model.occ.addCurveLoop([c14_tran, c17_tran, c1_tran, c19_tran])
s8_tran = gmsh.model.occ.addPlaneSurface([cloop8_tran])
cloop9_tran = gmsh.model.occ.addCurveLoop([c9_tran, c19_tran, c13_tran, c20_tran])
s9_tran = gmsh.model.occ.addPlaneSurface([cloop9_tran])
cloop10_tran = gmsh.model.occ.addCurveLoop([c12_tran, c20_tran, c16_tran, c18_tran])
s10_tran = gmsh.model.occ.addPlaneSurface([cloop10_tran])
cloop11_tran = gmsh.model.occ.addCurveLoop([c14_tran, c15_tran, c16_tran, c13_tran])
s11_tran = gmsh.model.occ.addPlaneSurface([cloop11_tran])


# Transducer volume
sloop2_tran = gmsh.model.occ.addSurfaceLoop([s6_tran, s11_tran, s8_tran, s7_tran, s10_tran, s9_tran])
v2_tran = gmsh.model.occ.addVolume([sloop2_tran])






################## TRANSDUCER SUBVOLUME ##################################

p13_tran = gmsh.model.occ.addPoint(xcen, ycen, 0, sub_center_ref)
p14_tran = gmsh.model.occ.addPoint(xcen, ycen+radius, 0, pump_refine)
p15_tran = gmsh.model.occ.addPoint(xcen, ycen-radius, 0, pump_refine)
p16_tran = gmsh.model.occ.addPoint(xcen+radius, ycen, 0, pump_refine)
p17_tran = gmsh.model.occ.addPoint(xcen-radius, ycen, 0, pump_refine)


# Adding mesh refinement for pump region in transducer
c21_tran = gmsh.model.occ.addCircleArc(p17_tran, p13_tran, p15_tran)
c22_tran = gmsh.model.occ.addCircleArc(p15_tran, p13_tran, p16_tran)
c23_tran = gmsh.model.occ.addCircleArc(p16_tran, p13_tran, p14_tran)
c24_tran = gmsh.model.occ.addCircleArc(p17_tran, p13_tran, p14_tran)


cloop12_tran = gmsh.model.occ.addCurveLoop([c21_tran, c22_tran, c23_tran, c24_tran])
s12_tran = gmsh.model.occ.addPlaneSurface([cloop12_tran])


p27_tran = gmsh.model.occ.addPoint(xcen, ycen, trans_thick, trans_thick_ref)
p28_tran = gmsh.model.occ.addPoint(xcen, ycen+radius, trans_thick, pump_refine)
p29_tran = gmsh.model.occ.addPoint(xcen, ycen-radius, trans_thick, pump_refine)
p30_tran = gmsh.model.occ.addPoint(xcen+radius, ycen, trans_thick, pump_refine)
p31_tran = gmsh.model.occ.addPoint(xcen-radius, ycen, trans_thick, pump_refine)

c41_tran = gmsh.model.occ.addCircleArc(p31_tran, p27_tran, p29_tran)
c42_tran = gmsh.model.occ.addCircleArc(p29_tran, p27_tran, p30_tran)
c43_tran = gmsh.model.occ.addCircleArc(p30_tran, p27_tran, p28_tran)
c44_tran = gmsh.model.occ.addCircleArc(p28_tran, p27_tran, p31_tran)


c45_tran = gmsh.model.occ.addLine(p31_tran, p17_tran)
c46_tran = gmsh.model.occ.addLine(p29_tran, p15_tran)
c47_tran = gmsh.model.occ.addLine(p30_tran, p16_tran)
c48_tran = gmsh.model.occ.addLine(p28_tran, p14_tran)


cloop23_tran = gmsh.model.occ.addCurveLoop([c41_tran, c42_tran, c43_tran, c44_tran])
s23_tran = gmsh.model.occ.addPlaneSurface([cloop23_tran])
cloop24_tran = gmsh.model.occ.addCurveLoop([c45_tran, c41_tran, c46_tran, c21_tran])
s24_tran = gmsh.model.occ.addSurfaceFilling(cloop24_tran)
cloop25_tran = gmsh.model.occ.addCurveLoop([c46_tran, c42_tran, c47_tran, c22_tran])
s25_tran = gmsh.model.occ.addSurfaceFilling(cloop25_tran)
cloop26_tran = gmsh.model.occ.addCurveLoop([c47_tran, c43_tran, c48_tran, c23_tran])
s26_tran = gmsh.model.occ.addSurfaceFilling(cloop26_tran)
cloop27_tran = gmsh.model.occ.addCurveLoop([c48_tran, c44_tran, c45_tran, c24_tran])
s27_tran = gmsh.model.occ.addSurfaceFilling(cloop27_tran)

sloop5_tran = gmsh.model.occ.addSurfaceLoop([s12_tran, s23_tran, s24_tran, s25_tran, s26_tran])
v5_tran = gmsh.model.occ.addVolume([sloop5_tran])

# ################## END TRANSDUCER SUBVOLUME ##################################


result = gmsh.model.occ.cut([(3, v2_tran)], [(3, v5_tran)], removeTool=False)
if result[0]:  # Ensure subtraction was successful
    v2_tran = result[0][0]  # Store the new volume tag


gmsh.model.occ.synchronize()
gmsh.fltk.run()


# ################## ADDITIONAL TRANSDUCER SUBVOLUME ##################################
# ##### TRANSDUCER DUMMY SUB-VOLUME #####
# p32 = gmsh.model.occ.addPoint(xcen, ycen+(radius/dummy_factor), trans_thick, trans_thick_ref)
# p33 = gmsh.model.occ.addPoint(xcen, ycen-(radius/dummy_factor), trans_thick, trans_thick_ref)
# p34 = gmsh.model.occ.addPoint(xcen+(radius/dummy_factor), ycen, trans_thick, trans_thick_ref)
# p35 = gmsh.model.occ.addPoint(xcen-(radius/dummy_factor), ycen, trans_thick, trans_thick_ref)

# c57 = gmsh.model.occ.addCircleArc(p35, p27, p33)
# c58 = gmsh.model.occ.addCircleArc(p33, p27, p34)
# c59 = gmsh.model.occ.addCircleArc(p34, p27, p32)
# c60 = gmsh.model.occ.addCircleArc(p32, p27, p35)

# c61 = gmsh.model.occ.addLine(p35, p39)
# c62 = gmsh.model.occ.addLine(p33, p37)
# c63 = gmsh.model.occ.addLine(p34, p38)
# c64 = gmsh.model.occ.addLine(p32, p36)

# cloop33 = gmsh.model.occ.addCurveLoop([c57, c58, c59, c60])
# s33 = gmsh.model.occ.addPlaneSurface([cloop33])
# cloop34 = gmsh.model.occ.addCurveLoop([c61, c57, c62, c49])
# s34 = gmsh.model.occ.addSurfaceFilling(cloop34)
# cloop35 = gmsh.model.occ.addCurveLoop([c62, c58, c63, c50])
# s35 = gmsh.model.occ.addSurfaceFilling(cloop35)
# cloop36= gmsh.model.occ.addCurveLoop([c63, c59, c64, c51])
# s36 = gmsh.model.occ.addSurfaceFilling(cloop36)
# cloop37 = gmsh.model.occ.addCurveLoop([c64, c60, c61, c52])
# s37 = gmsh.model.occ.addSurfaceFilling(cloop37)

# sloop6 = gmsh.model.occ.addSurfaceLoop([s28, s33, s34, s35, s36])
# v6 = gmsh.model.occ.addVolume([sloop6])

# ################## END ADDITIONAL TRANSDUCER SUBVOLUME ##################################





# gmsh.model.occ.synchronize()
# gmsh.fltk.run()


# result = gmsh.model.occ.cut([(3, v2)], [(3, v5)], removeTool=False)
# if result[0]:  # Ensure subtraction was successful
    # v2 = result[0][0]  # Store the new volume tag

# result = gmsh.model.occ.cut([(3, v5)], [(3, v6)], removeTool=False)
# if result[0]:
    # v6 = result[0][0]











# EMBED Dummy Points in Mesh
# gmsh.model.mesh.embed(0, [p13], 2, s12)
# gmsh.model.mesh.embed(0, [p13], 3, v3)

# gmsh.model.mesh.embed(0, [p27], 2, s23)
# gmsh.model.mesh.embed(0, [p27], 3, v5)

# gmsh.model.mesh.embed(3, [v6], 3, v3)
# gmsh.model.mesh.embed(3, [v7], 3, v5)

# Make mesh coherent
# gmsh.model.occ.removeAllDuplicates()
# gmsh.model.occ.synchronize()


# Subtract dummy volumes instead of relying on removeAllDuplicates
# Subtract dummy volumes instead of relying on removeAllDuplicates


# gmsh.fltk.run()

# # assign mesh size at all points without a mesh size constraint
# p = gmsh.model.occ.getEntities(0)
# s = gmsh.model.mesh.getSizes(p)

# for ps in zip(p, s):
    # if ps[1] == 0:
        # # get coordinates of newly created points
        # val = gmsh.model.getValue(0, ps[0][1], [])
        
        # # check if they are within the radius of the small sphere
        # checkSphere = ((val[0])**2 + (val[1])**2 + (val[2])**2)
        # # checkCylinder = ((val[0])**2 + (val[1])**2 + (val[2]-0.09)**2)
        # # print(checkSphere)
        
        # # assign small sphere refinement if yes, large sphere refinement otherwise
        # if (( checkSphere <= ((radius/dummy_factor)**2 + 1e-2)) and ((val[2]) <= 0)):
            # gmsh.model.mesh.setSize([ps[0]], trans_thick_ref)
        # else:
            # gmsh.model.mesh.setSize([ps[0]], pump_refine)
   
# gmsh.model.occ.removeAllDuplicates()
# gmsh.model.occ.synchronize()



# # Create 3D mesh
# gmsh.model.mesh.generate(3)

# gmsh.write(newMeshName)

# gmsh.fltk.run()

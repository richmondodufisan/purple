#Global Parameters
shear_modulus_val = 100000

stretch_ratio = 1.3
l_plate = 0.02
right_disp_val = ${fparse (stretch_ratio - 1)*l_plate}

#observation_point = ${fparse l_plate/10}

[GlobalParams]
  stabilize_strain = true
  large_kinematics = true
[]

[Mesh]
  second_order = true
  
  [sample_mesh]
    type = FileMeshGenerator
    file = cornea_rectangle.msh
  []
[]

[Variables]
  [disp_x]
    order = SECOND
    family = LAGRANGE
  []
  [disp_y]
    order = SECOND
    family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_x]
    type = TotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x disp_y'
    variable = disp_x
  []
  
  [div_sig_y]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x disp_y'
    variable = disp_y
  []
[]

[Postprocessors]
  [displace_x]
    type = PointValue
    variable = disp_x
    point = '${l_plate} 0.0005 0'
  []
[]

[Materials]
  [strain_energy]
    type = ComputeStrainEnergyNeoHookean
    mu_0 = ${shear_modulus_val}
	output_properties = 'all'
  []
  
  [intermediate]
    type = NeoHookeanStressIntermediate
  []
  
  [strain]
    type = ComputeLagrangianStrain
	displacements = 'disp_x disp_y'
	output_properties = 'all'
  []
  
  [stress]
    type = ComputeStressNeoHookean
  []
[]

[BCs]
  [left_x]
    type = ADDirichletBC
    variable = disp_x
    boundary = 'left'
    value = 0
	preset = false
  []
  [left_y]
    type = ADDirichletBC
    variable = disp_y
    boundary = 'left'
    value = 0
	preset = false
  []
  
  
  [right_x]
    type = ADDirichletBC
    variable = disp_x
    boundary = 'right'
    value = ${right_disp_val}
	preset = false
  []
  [right_y]
    type = ADDirichletBC
    variable = disp_y
    boundary = 'right'
    value = 0
	preset = false
  []
[]

[Executioner]
  type = Steady
  solve_type = 'NEWTON'
  
  petsc_options_iname = '-pc_type -pc_factor_shift_type'
  petsc_options_value = 'lu NONZERO'


  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
[]

[Outputs]
  csv = true
  exodus = true
  perf_graph = true
[]

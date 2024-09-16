#Global Parameters
shear_modulus_val = 100000
poissons_ratio_val = 0.49

stretch_ratio = 1.1
l_plate = 0.02
right_disp_val = ${fparse (stretch_ratio - 1)*l_plate}

dt_val = ${fparse right_disp_val/100}

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
	base_name = real
	save_in = force_x
  []
  
  [div_sig_y]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x disp_y'
    variable = disp_y
	base_name = real
	save_in = force_y
  []
[]

[AuxVariables]
  [force_x]
    order = SECOND
    family = LAGRANGE
  []
  [force_y]
    order = SECOND
    family = LAGRANGE
  []
[]

[Postprocessors]
  [displace_x]
    type = PointValue
    variable = disp_x
    point = '${l_plate} 0.001 0'
  []
  [react_x]
    type = PointValue
    variable = force_x
    point = '${l_plate} 0.001 0'
  []
[]

[Materials]
  [strain_energy]
    type = ComputeStrainEnergyNeoHookeanNearlyIncompressible
    mu_0 = ${shear_modulus_val}
	poissons_ratio = ${poissons_ratio_val}
	base_name = real
  []
  
  [strain]
    type = ComputeLagrangianStrain
	displacements = 'disp_x disp_y'
	base_name = real
  []
  
  [stress]
    type = ComputeStressNeoHookean
	base_name = real
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
    type = ADFunctionDirichletBC
    variable = disp_x
    boundary = 'right'
    function = 't'
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
  type = Transient
  solve_type = 'NEWTON'
  line_search = 'none'
  
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'

  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
  
  start_time = 0.0
  end_time = ${right_disp_val}
   
  [TimeStepper]
    type = IterationAdaptiveDT
    optimal_iterations = 15
    iteration_window = 3
    linear_iteration_ratio = 100
    growth_factor=1.5
    cutback_factor=0.5
    dt = ${dt_val}
  []
[]

[Outputs]
  csv = true
  exodus = true
  perf_graph = true
[]

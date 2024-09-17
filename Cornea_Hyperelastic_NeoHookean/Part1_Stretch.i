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
  []
  
  [div_sig_y]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x disp_y'
    variable = disp_y
  []
[]

[AuxVariables]
  [strain_xx]
    order = CONSTANT
    family = MONOMIAL
  []
  [strain_yy]
    order = CONSTANT
    family = MONOMIAL
  []

  [stress_xx]
    order = CONSTANT
    family = MONOMIAL
  []
  [stress_yy]
    order = CONSTANT
    family = MONOMIAL
  []
[]

[AuxKernels]
  [stress_xx]
    type = RankTwoAux
    rank_two_tensor = cauchy_stress
    variable = stress_xx
    index_i = 0
    index_j = 0
  []
  [stress_yy]
    type = RankTwoAux
    rank_two_tensor = cauchy_stress
    variable = stress_yy
    index_i = 1
    index_j = 1
  []

  [strain_xx]
    type = RankTwoAux
    rank_two_tensor = total_strain
    variable = strain_xx
    index_i = 0
    index_j = 0
  []
  [strain_yy]
    type = RankTwoAux
    rank_two_tensor = total_strain
    variable = strain_yy
    index_i = 1
    index_j = 1
  []
[]

[Postprocessors]
  [displace_x]
    type = PointValue
    variable = strain_xx
    point = '${l_plate} 0.001 0'
  []
  [react_x]
    type = PointValue
    variable = stress_xx
    point = '${l_plate} 0.001 0'
  []
[]

[Materials]
  [strain_energy]
    type = ComputeStrainEnergyNeoHookeanNearlyIncompressible
    mu_0 = ${shear_modulus_val}
	poissons_ratio = ${poissons_ratio_val}
  []
  
  [strain]
    type = ComputeLagrangianStrain
	displacements = 'disp_x disp_y'
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

  nl_rel_tol = 1e-12
  nl_abs_tol = 1e-12
  l_tol = 1e-8
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

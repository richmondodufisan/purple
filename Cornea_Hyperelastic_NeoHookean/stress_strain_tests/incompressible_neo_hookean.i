#Global Parameters

shear_modulus_val = 100000

stretch_ratio = 5.0
l_plate = 0.02
right_disp_val = ${fparse (stretch_ratio - 1)*l_plate}

dt_val = ${fparse right_disp_val/100}

#observation_point = ${fparse l_plate/10}

[GlobalParams]
  large_kinematics = true
[]

[Mesh]
  second_order = true
  
  [sample_mesh]
    type = FileMeshGenerator
    file = rectangular_plate.msh
  []
[]

[Variables]
  [disp_x]
    order = FIRST
    family = LAGRANGE
  []
  [disp_y]
    order = FIRST
    family = LAGRANGE
  []
  [pressure]
    order = CONSTANT
    family = MONOMIAL
  []
[]


[Kernels]
  [div_sig_x]
    type = TLStressDivergenceIncompressible
	component = 0
	displacements = 'disp_x disp_y'
    variable = disp_x
	pressure = pressure
  []
  
  [div_sig_y]
    type = TLStressDivergenceIncompressible
	component = 1
	displacements = 'disp_x disp_y'
    variable = disp_y
	pressure = pressure
  []
  
  [incompressibility]
    type = TLIncompressibilityPressure
    variable = pressure
	displacements = 'disp_x disp_y'
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
  
  [jacobian]
    order = CONSTANT
    family = MONOMIAL
  []
[]

[AuxKernels]
  [jacobian]
    type = RankTwoScalarAux
    rank_two_tensor = deformation_gradient
    variable = jacobian
	scalar_type = ThirdInvariant
  []
  
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
  [axial_strain]
    type = PointValue
    variable = strain_xx
    point = '${l_plate} 0.001 0'
  []
  [axial_stress]
    type = PointValue
    variable = stress_xx
    point = '${l_plate} 0.001 0'
  []
  [pressure_integral]
    type = ElementIntegralVariablePostprocessor
    variable = pressure
	execute_on = 'initial timestep_begin'
  []
[]

[Materials]
  [stress]
    type = HyperelasticIsochoricNeoHookeanStress
    mu = ${shear_modulus_val}
  []
  
  [strain]
    type = ComputeLagrangianStrain
	displacements = 'disp_x disp_y'
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


[Preconditioning]
  [vcp]
    type = VCP
    full = true
    lm_variable = 'pressure'
    primary_variable = 'disp_x'
    preconditioner = 'AMG'
    is_lm_coupling_diagonal = false
    adaptive_condensation = false
  []
[]


[Executioner]
  type = Transient
  solve_type = 'NEWTON'
  line_search = 'none'
  
  petsc_options_iname = '-pc_type -ksp_type -pc_factor_mat_solver_type'
  petsc_options_value = 'lu       gmres     superlu_dist'

  nl_rel_tol = 1e-12
  nl_abs_tol = 1e-12
  l_tol = 1e-8
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
  scaling_group_variables = 'disp_x disp_y'
  
  start_time = 0.0
  end_time = ${right_disp_val}
   
  [TimeStepper]
    type = ConstantDT
    dt = ${dt_val}
  []
[]

[Outputs]
  csv = true
  exodus = true
  perf_graph = true
  print_linear_residuals = false
[]

#Global Parameters
shear_modulus_val = 100000

stretch_ratio = 1.1
l_plate = 0.02
right_disp_val = ${fparse (stretch_ratio - 1)*l_plate}

dt_val = ${fparse right_disp_val/100}

#observation_point = ${fparse l_plate/10}

[GlobalParams]
  #stabilize_strain = true
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
  [pressure]
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
  
  [incompressibility]
	type = StressIncompressibilityConstraint
	variable = pressure
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

  [strain]
    type = ComputeLagrangianStrain
	displacements = 'disp_x disp_y'
  []

  [strain_energy]
    type = ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff
    mu_0 = ${shear_modulus_val}
	pressure_var = pressure
  []

  [stress]
    type = ComputeStressNeoHookean_NumericalDiff
  []
[]

[BCs]
  [left_x]
    type = DirichletBC
    variable = disp_x
    boundary = 'left'
    value = 0
	preset = false
  []
  [left_y]
    type = DirichletBC
    variable = disp_y
    boundary = 'left'
    value = 0
	preset = false
  []
  
  
  [right_x]
    type = FunctionDirichletBC
    variable = disp_x
    boundary = 'right'
    function = 't'
	preset = false
  []
[]

[Executioner]
  type = Transient
  solve_type = 'NEWTON'
  
  petsc_options_iname = '-pc_type -pc_factor_shift_type'
  petsc_options_value = 'lu NONZERO'

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

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
  [disp_x_real]
    order = SECOND
    family = LAGRANGE
  []
  [disp_y_real]
    order = SECOND
    family = LAGRANGE
  []
  [disp_x_imag]
    order = SECOND
    family = LAGRANGE
  []
  [disp_y_imag]
    order = SECOND
    family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_x_real]
    type = TotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x_real disp_y_real'
    variable = disp_x_real
	base_name = real
	save_in = force_x_real
  []
  
  [div_sig_y_real]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_real disp_y_real'
    variable = disp_y_real
	base_name = real
	save_in = force_y_real
  []
  
  [div_sig_x_imag]
    type = TotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_x_imag
	base_name = imag
	save_in = force_x_imag
  []
  
  [div_sig_y_imag]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_y_imag
	base_name = imag
	save_in = force_y_imag
  []
[]

[AuxVariables]
  [disp_x]
  []
  [disp_y]
  []
  [force_x_real]
    order = SECOND
    family = LAGRANGE
  []
  [force_y_real]
    order = SECOND
    family = LAGRANGE
  []
  [force_x_imag]
    order = SECOND
    family = LAGRANGE
  []
  [force_y_imag]
    order = SECOND
    family = LAGRANGE
  []
[]

[AuxKernels]
  [x_displacement]
    type = ParsedAux
    variable = disp_x
    coupled_variables = 'disp_x_real disp_x_imag'
	expression = 'sqrt(disp_x_real^2 + disp_x_imag^2)'
  []
  [y_displacement]
    type = ParsedAux
    variable = disp_y
    coupled_variables = 'disp_y_real disp_y_imag'
	expression = 'sqrt(disp_y_real^2 + disp_y_imag^2)'
  []
[]

[Postprocessors]
  [displace_x]
    type = PointValue
    variable = disp_x_real
    point = '${l_plate} 0.001 0'
  []
  [react_x]
    type = PointValue
    variable = force_x_real
    point = '${l_plate} 0.001 0'
  []
[]

[Materials]
  [strain_energy_real]
    type = ComputeStrainEnergyNeoHookeanNearlyIncompressible
    mu_0 = ${shear_modulus_val}
	poissons_ratio = ${poissons_ratio_val}
	base_name = real
  []
  
  [strain_real]
    type = ComputeLagrangianStrain
	displacements = 'disp_x_real disp_y_real'
	base_name = real
  []
  
  [stress_real]
    type = ComputeStressNeoHookean
	base_name = real
  []
  
  
  [strain_energy_imag]
    type = ComputeStrainEnergyNeoHookeanNearlyIncompressible
    mu_0 = ${shear_modulus_val}
	poissons_ratio = ${poissons_ratio_val}
	base_name = imag
  []
  
  [strain_imag]
    type = ComputeLagrangianStrain
	displacements = 'disp_x_real disp_y_real'
	base_name = imag
  []
  
  [stress_imag]
    type = ComputeStressNeoHookean
	base_name = imag
  []
[]

[BCs]
  [left_x_real]
    type = ADDirichletBC
    variable = disp_x_real
    boundary = 'left'
    value = 0
	preset = false
  []
  [left_x_imag]
    type = ADDirichletBC
    variable = disp_x_imag
    boundary = 'left'
    value = 0
	preset = false
  []
  [left_y_real]
    type = ADDirichletBC
    variable = disp_y_real
    boundary = 'left'
    value = 0
	preset = false
  []
  [left_y_imag]
    type = ADDirichletBC
    variable = disp_y_imag
    boundary = 'left'
    value = 0
	preset = false
  []
  
  
  [right_x_real]
    type = ADFunctionDirichletBC
    variable = disp_x_real
    boundary = 'right'
    function = 't'
	preset = false
  []
  [right_x_imag]
    type = ADDirichletBC
    variable = disp_x_imag
    boundary = 'right'
    value = 0
	preset = false
  []
  [right_y_real]
    type = ADDirichletBC
    variable = disp_y_real
    boundary = 'right'
    value = 0
	preset = false
  []
  [right_y_imag]
    type = ADDirichletBC
    variable = disp_y_imag
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

#Global Parameters
freq_val = 3e6
omega = ${fparse 2 * pi * freq_val}

youngs_modulus_val = 70e9
poissons_ratio_val = 0.33
density = 2700

excitation_val = -0.0001

[GlobalParams]
  large_kinematics = false
[]

[Mesh]
  second_order = true
  [sample_mesh]
    type = FileMeshGenerator
    file = eyeball_2D.msh
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
  []
  
  [div_sig_y_real]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_real disp_y_real'
    variable = disp_y_real
	base_name = real
  []
  
  [reaction_x_real]
    type = ADReaction
	variable = disp_x_real
	rate = ${fparse -omega*omega*density}
  []
  
  [reaction_y_real]
    type = ADReaction
	variable = disp_y_real
	rate = ${fparse -omega*omega*density}
  []
  
  
  
  
  [div_sig_x_imag]
    type = TotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_x_imag
	base_name = imag
  []
  
  [div_sig_y_imag]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_y_imag
	base_name = imag
  []

  [reaction_x_imag]
    type = ADReaction
	variable = disp_x_imag
	rate = ${fparse -omega*omega*density}
  []
  
  [reaction_y_imag]
    type = ADReaction
	variable = disp_y_imag
	rate = ${fparse -omega*omega*density}
  []
[]

[AuxVariables]
  [disp_x]
  []
  [disp_y]
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

[Materials]
  [elastic_tensor_real]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
	base_name = real
  []
  [compute_stress_real]
    type = ComputeLagrangianLinearElasticStress
	elasticity_tensor = real_elasticity_tensor
	base_name = real
  []
  [compute_strain_real]
    type = ComputeLagrangianStrain
    displacements = 'disp_x_real disp_y_real'
	base_name = real
  []
  
  
  [elastic_tensor_imag]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
	base_name = imag
  []
  [compute_stress_imag]
    type = ComputeLagrangianLinearElasticStress
	elasticity_tensor = imag_elasticity_tensor
	base_name = imag
  []
  [compute_strain_imag]
    type = ComputeLagrangianStrain
    displacements = 'disp_x_imag disp_y_imag'
	base_name = imag
  []
[]

[BCs]
  [harmonic_perturbation_real]
    type = DirichletBC
    variable = disp_y_real
    boundary = 'loading_point'
	value = '${excitation_val}'
	preset = false
  []
  
  [harmonic_perturbation_imag]
    type = DirichletBC
    variable = disp_y_imag
    boundary = 'loading_point'
    value = 0
	preset = false
  []
  
  [fix_x_real_top]
    type = DirichletBC
    variable = disp_x_real
    boundary = 'loading_point'
	value = 0
	preset = false
  []
  
  [fix_x_imag_top]
    type = DirichletBC
    variable = disp_x_imag
    boundary = 'loading_point'
    value = 0
	preset = false
  []
  
  [fix_x_real_bottom]
    type = DirichletBC
    variable = disp_x_real
    boundary = 'fixed_point'
	value = 0
	preset = false
  []
  
  [fix_x_imag_bottom]
    type = DirichletBC
    variable = disp_x_imag
    boundary = 'fixed_point'
    value = 0
	preset = false
  []
  
  [fix_y_real_bottom]
    type = DirichletBC
    variable = disp_y_real
    boundary = 'fixed_point'
	value = 0
	preset = false
  []
  
  [fix_y_imag_bottom]
    type = DirichletBC
    variable = disp_y_imag
    boundary = 'fixed_point'
    value = 0
	preset = false
  []
[]


[VectorPostprocessors]
  [upper_right_y_disp]
    type = SideValueSampler
    variable = 'disp_y'
    boundary = 'sample_location'
    sort_by = x
  []
[]


[Executioner]
  type = Steady
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
[]

[Outputs]
  time_step_interval = 1
  #execute_on = 'initial timestep_end'
  print_linear_residuals = false
  csv = true
  exodus = true
  [pgraph]
    type = PerfGraphOutput
    execute_on = 'final'  # Default is "final"
    level = 1             # Default is 1
  []
[]

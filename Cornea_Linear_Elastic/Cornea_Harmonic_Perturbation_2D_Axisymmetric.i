#Global Parameters
freq_val = 10e6
omega = ${fparse 2 * pi * freq_val}

youngs_modulus_val = 207e9
poissons_ratio_val = 0.29
density = 7850

excitation_val = 10000000

[GlobalParams]
  large_kinematics = false
[]

[Mesh]
  second_order = true
  coord_type = RZ
  [sample_mesh]
    type = FileMeshGenerator
    file = eyeball_2D_axisymmetric.msh
  []
  
  [applied_force]
    type = ParsedGenerateSideset
	input = sample_mesh
	combinatorial_geometry = '(y > 0.025-1e-4) & (y < 0.025+1e-4) & (x < 0+1e-4) & (x < 0+1e-4)'
	new_sideset_name = top_force_area
  []
[]

[Variables]
  [disp_r_real]
    order = SECOND
    family = LAGRANGE
  []
  [disp_z_real]
    order = SECOND
	family = LAGRANGE
  []
  [disp_r_imag]
    order = SECOND
    family = LAGRANGE
  []
  [disp_z_imag]
    order = SECOND
	family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_r_real]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 0
	displacements = 'disp_r_real disp_z_real'
    variable = disp_r_real
	base_name = real
  []
  
  [div_sig_z_real]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 1
	displacements = 'disp_r_real disp_z_real'
    variable = disp_z_real
	base_name = real
  []
  
  [reaction_r_real]
    type = ADReaction
	variable = disp_r_real
	rate = ${fparse -omega*omega*density}
  []
  
  [reaction_z_real]
    type = ADReaction
	variable = disp_z_real
	rate = ${fparse -omega*omega*density}
  []

  
  
  
  
  [div_sig_r_imag]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 0
	displacements = 'disp_r_imag disp_z_imag'
    variable = disp_r_imag
	base_name = imag
  []
  
  [div_sig_z_imag]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 1
	displacements = 'disp_r_imag disp_z_imag'
    variable = disp_z_imag
	base_name = imag
  []
  
  [reaction_r_imag]
    type = ADReaction
	variable = disp_r_imag
	rate = ${fparse -omega*omega*density}
  []
  
  [reaction_z_imag]
    type = ADReaction
	variable = disp_z_imag
	rate = ${fparse -omega*omega*density}
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
	elasticity_tensor = elasticity_tensor
	base_name = real
  []
  [compute_strain_real]
    type = ComputeLagrangianStrainAxisymmetricCylindrical
    displacements = 'disp_r_real disp_z_real'
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
	elasticity_tensor = elasticity_tensor
	base_name = imag
  []
  [compute_strain_imag]
    type = ComputeLagrangianStrainAxisymmetricCylindrical
    displacements = 'disp_r_imag disp_z_imag'
	base_name = imag
  []
[]

[BCs]
  [harmonic_perturbation_real]
    type = NeumannBC
    variable = disp_z_real
    boundary = 'top_force_area'
	value = '${excitation_val}'
  []
  
  [harmonic_perturbation_imag]
    type = NeumannBC
    variable = disp_z_imag
    boundary = 'top_force_area'
    value = 0
  []
  
  [symmetry_real]
    type = DirichletBC
    variable = disp_r_real
    boundary = 'symmetry_axis'
	value = 0
	preset = false
  []
  
  [symmetry_imag]
    type = DirichletBC
    variable = disp_r_imag
    boundary = 'symmetry_axis'
    value = 0
	preset = false
  []

  [fix_r_real]
    type = DirichletBC
    variable = disp_r_real
    boundary = 'fixed_point'
	value = 0
	preset = false
  []
  [fix_r_imag]
    type = DirichletBC
    variable = disp_r_imag
    boundary = 'fixed_point'
	value = 0
	preset = false
  []
  
  [fix_z_real]
    type = DirichletBC
    variable = disp_z_real
    boundary = 'fixed_point'
	value = 0
	preset = false
  []
  [fix_z_imag]
    type = DirichletBC
    variable = disp_z_imag
    boundary = 'fixed_point'
	value = 0
	preset = false
  []  


[]

[VectorPostprocessors]
  [upper_right_z_disp]
    type = NodalValueSampler
    variable = 'disp_z_real'
    boundary = 'sample_location'
    sort_by = x
  []
  [upper_right_r_disp]
    type = NodalValueSampler
    variable = 'disp_r_real'
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

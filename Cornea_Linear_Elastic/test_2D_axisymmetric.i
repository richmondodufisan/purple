#Global Parameters
freq_val = 3e6
omega = ${fparse 2 * pi * freq_val}

youngs_modulus_val = 70e9
poissons_ratio_val = 0.33
density = 2700

excitation_val = -0.00001

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
[]

[Variables]
  [disp_r]
    order = SECOND
    family = LAGRANGE
  []
  [disp_z]
    order = SECOND
	family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_r]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 0
	displacements = 'disp_r disp_z'
    variable = disp_r_real
	base_name = real
  []
  
  [div_sig_z]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 1
	displacements = 'disp_r disp_z'
    variable = disp_z_real
	base_name = real
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
    type = ComputeLagrangianStrainAxisymmetricCylindrical
    displacements = 'disp_r disp_z'
	base_name = real
  []
[]

[BCs]
  [harmonic_perturbation_real]
    type = DirichletBC
    variable = disp_z
    boundary = 'loading_point'
	value = '${excitation_val}'
	preset = false
  []
  
  [symmetry]
    type = DirichletBC
    variable = disp_r
    boundary = 'symmetry_axis'
	value = 0
	preset = false
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

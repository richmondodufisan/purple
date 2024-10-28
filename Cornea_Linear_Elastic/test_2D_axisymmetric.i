#Global Parameters
youngs_modulus_val = 70e9
poissons_ratio_val = 0.33

excitation_val = -0.00001

[GlobalParams]
  large_kinematics = false
[]

[Mesh]
  second_order = true
  coord_type = RZ
  [sample_mesh]
    type = FileMeshGenerator
    file = eyeball_2D_axisymmetric_xy_plane.msh
  []
  [apply_load]
    type = ExtraNodesetGenerator
    new_boundary = 'loading_point'
    coord = '0 0.002 0'
    input = sample_mesh
  []
  [restrain]
    type = ExtraNodesetGenerator
    new_boundary = 'fixed_point'
    coord = '0 -0.002 0'
    input = apply_load
  []
  [symmetry_axis_gen]
    type = ParsedGenerateNodeset
    input = restrain
    combinatorial_geometry = '(abs(x) < 1e-8)'
    new_nodeset_name = symmetry_axis
  []
[]

[Variables]
  [disp_r_val]
    order = SECOND
    family = LAGRANGE
  []
  [disp_z_val]
    order = SECOND
	family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_r]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 0
	displacements = 'disp_r_val disp_z_val'
    variable = disp_r_val
  []
  
  [div_sig_z]
    type = TotalLagrangianStressDivergenceAxisymmetricCylindrical
	component = 1
	displacements = 'disp_r_val disp_z_val'
    variable = disp_z_val
  []
[]


[Materials]
  [elastic_tensor]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
  []
  [compute_stress]
    type = ComputeLagrangianLinearElasticStress
  []
  [compute_strain]
    type = ComputeLagrangianStrainAxisymmetricCylindrical
    displacements = 'disp_r_val disp_z_val'
  []
[]

[BCs]
  [downward_disp]
    type = DirichletBC
    variable = disp_z_val
    boundary = 'loading_point'
	value = '${excitation_val}'
	preset = false
  []
  
  [symmetry]
    type = DirichletBC
    variable = disp_r_val
    boundary = 'symmetry_axis'
	value = 0
	preset = false
  []
  
  [fix_disp]
    type = DirichletBC
    variable = disp_z_val
    boundary = 'fixed_point'
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

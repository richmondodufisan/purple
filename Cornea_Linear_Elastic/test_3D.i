#Global Parameters
youngs_modulus_val = 70e9
poissons_ratio_val = 0.33

excitation_val = -0.00001

[GlobalParams]
  large_kinematics = false
[]

[Mesh]
  second_order = true
  [sample_mesh]
    type = FileMeshGenerator
    file = eyeball_3D.msh
  []
  [curve_surface_1]
    type = ParsedGenerateNodeset
    input = sample_mesh
    combinatorial_geometry = '(abs(y) < 1e-8) & (abs(x * x + z * z - 0.002 *0.002) < 1e-8 ) & (z > 0) & (x > 0)'
    new_nodeset_name = curve_surf_1
  []
  [apply_load]
    type = ExtraNodesetGenerator
    new_boundary = 'loading_point'
    coord = '0 0 0.002'
    input = curve_surface_1
  []
  [restrain]
    type = ExtraNodesetGenerator
    new_boundary = 'fixed_point'
    coord = '0 0 -0.002'
    input = apply_load
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
  [disp_z]
    order = SECOND
	family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_x]
    type = TotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x disp_y disp_z'
    variable = disp_x
  []
  
  [div_sig_y]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x disp_y disp_z'
    variable = disp_y
  []
  
  [div_sig_z]
    type = TotalLagrangianStressDivergence
	component = 2
	displacements = 'disp_x disp_y disp_z'
    variable = disp_z
  []
[]

[AuxVariables]
  [disp_r]
  []
[]

[AuxKernels]
  [r_displacement]
    type = ParsedAux
    variable = disp_r
    coupled_variables = 'disp_x disp_y'
	expression = 'sqrt(disp_x^2 + disp_y^2)'
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
    type = ComputeLagrangianStrain
    displacements = 'disp_x disp_y disp_z'
  []
[]

[BCs]
  [downward_disp]
    type = DirichletBC
    variable = disp_z
    boundary = 'loading_point'
	value = '${excitation_val}'
	preset = false
  []
  [fix_disp]
    type = DirichletBC
    variable = disp_z
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
  print_linear_residuals = false
  csv = true
  exodus = true
  [pgraph]
    type = PerfGraphOutput
    execute_on = 'final'  # Default is "final"
    level = 1             # Default is 1
  []
[]

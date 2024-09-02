#Global Parameters
youngs_modulus_val = 60000
poissons_ratio_val = 0.4999

stretch_ratio = 1.1
l_plate = 0.02
right_disp_val = ${fparse (stretch_ratio - 1)*l_plate}

observation_point = ${fparse l_plate/10}

[GlobalParams]
  volumetric_locking_correction = true
  large_kinematics = true
[]

[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = cornea_rectangle_freq_10e3.msh
  []
[]

[Variables]
  [disp_x_real]
    order = FIRST
    family = LAGRANGE
  []
  [disp_y_real]
    order = FIRST
    family = LAGRANGE
  []
  [disp_x_imag]
    order = FIRST
    family = LAGRANGE
  []
  [disp_y_imag]
    order = FIRST
    family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_x_real]
    type = ADTotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x_real disp_y_real'
    variable = disp_x_real
	base_name = real
  []
  
  [div_sig_y_real]
    type = ADTotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_real disp_y_real'
    variable = disp_y_real
	base_name = real
  []
  
  [div_sig_x_imag]
    type = ADTotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_x_imag
	base_name = imag
  []
  
  [div_sig_y_imag]
    type = ADTotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_y_imag
	base_name = imag
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

[Postprocessors]
  [displace_x]
    type = PointValue
    variable = disp_x
    point = '${observation_point} 0.001 0'
  []
[]

[Materials]
  [elasticity_tensor_real]
    type = ADComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
	base_name = real
  []
  
  [strain_real]
    type = ADComputeLagrangianStrain
	displacements = 'disp_x_real disp_y_real'
	base_name = real
  []
  
  [stress_real]
    type = ADComputeLagrangianLinearElasticStress
	base_name = real
  []
  
  
  [elasticity_tensor_imag]
    type = ADComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
	base_name = imag
  []
  
  [strain_imag]
    type = ADComputeLagrangianStrain
	displacements = 'disp_x_imag disp_y_imag'
	base_name = imag
  []
  
  [stress_imag]
    type = ADComputeLagrangianLinearElasticStress
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
    type = ADDirichletBC
    variable = disp_x_real
    boundary = 'right'
    value = ${right_disp_val}
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
  
  [top_y_real]
    type = ADDirichletBC
    variable = disp_y_real
    boundary = 'top'
    value = 0
	preset = false
  []
  [top_y_imag]
    type = ADDirichletBC
    variable = disp_y_imag
    boundary = 'top'
    value = 0
	preset = false
  []
  
  [bottom_y_real]
    type = ADDirichletBC
    variable = disp_y_real
    boundary = 'bottom'
    value = 0
	preset = false
  []
  [bottom_y_imag]
    type = ADDirichletBC
    variable = disp_y_imag
    boundary = 'bottom'
    value = 0
	preset = false
  []
[]

[Executioner]
  type = Steady
  solve_type = 'NEWTON'
  
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'


  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
[]

[Outputs]
  interval = 1
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

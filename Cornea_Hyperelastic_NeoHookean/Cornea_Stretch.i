#Global Parameters
shear_modulus_val = 100000

stretch_ratio = 1.001
l_plate = 0.02
right_disp_val = ${fparse (stretch_ratio - 1)*l_plate}

observation_point = ${fparse l_plate/10}

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
  []
  
  [div_sig_y_real]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_real disp_y_real'
    variable = disp_y_real
	base_name = real
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
  [strain_energy_real]
    type = ComputeStrainEnergyNeoHookean
    mu_0 = ${shear_modulus_val}
	base_name = real
  []
  
  [intermediate_real]
    type = NeoHookeanStressIntermediate
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
    type = ComputeStrainEnergyNeoHookean
    mu_0 = ${shear_modulus_val}
	base_name = imag
  []
  
  [intermediate_imag]
    type = NeoHookeanStressIntermediate
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
  csv = true
  exodus = true
  perf_graph = true
[]

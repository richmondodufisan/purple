[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = simple_box.msh
  []
[]

[Variables]
  [q_x]
    order = SECOND
    family = LAGRANGE
  []
  [q_y]
    order = SECOND
    family = LAGRANGE
  []
  [q_z]
    order = SECOND
    family = LAGRANGE
  []
  [temperature]
    order = FIRST
    family = LAGRANGE
  []
[]


[Kernels]
  [heat_x]
    type = KCMHeatEquation
    variable = q_x
	temperature = temperature
	component_flux = 0
	
	thermal_conductivity = k_val
	length_scale = length_scale_val
	alpha = alpha_val
		
	q_x = q_x
	q_y = q_y
	q_z = q_z
  []
  [heat_y]
    type = KCMHeatEquation
    variable = q_y
	temperature = temperature
	component_flux = 1
	
	thermal_conductivity = k_val
	length_scale = length_scale_val
	alpha = alpha_val
		
	q_x = q_x
	q_y = q_y
	q_z = q_z
  []
  [heat_z]
    type = KCMHeatEquation
    variable = q_z
	temperature = temperature
	component_flux = 2
	
	thermal_conductivity = k_val
	length_scale = length_scale_val
	alpha = alpha_val
		
	q_x = q_x
	q_y = q_y
	q_z = q_z
  []
  [diffuse]
    type = DiffusionTemperature
    variable = temperature
	
	q_x = q_x
	q_y = q_y
	q_z = q_z
  []
[]

[Postprocessors]
  [central_temp]
    type = PointValue
    variable = temperature
    point = '5 5 2.5'
  []
[]

[Materials]
  [simulation_constants]
    type = ADGenericConstantMaterial
    prop_names = 'k_val length_scale_val alpha_val'
    prop_values = '1.0 0.1 2.0'
  []
[]

[BCs]
  [left_val]
    type = DirichletBC
    variable = temperature
    boundary = 'left'
    value = 0
  []
  [right_val]
    type = NeumannBC
    variable = temperature
    boundary = 'right'
    value = 1000
  []
[]

[Preconditioning]
  [smp]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Steady
  solve_type = 'PJFNK'
  
  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
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
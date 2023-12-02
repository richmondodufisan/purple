[Mesh]
  second_order = true

  [sample_mesh]
    type = FileMeshGenerator
    file = Meshes/simple_box_2d.msh
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
    type = FourierHeatEquation
    variable = q_x
	temperature = temperature
	component_flux = 0
	thermal_conductivity = k_val
  []
  [heat_y]
    type = FourierHeatEquation
    variable = q_y
	temperature = temperature
	component_flux = 1
	thermal_conductivity = k_val
  []
  [heat_z]
    type = FourierHeatEquation
    variable = q_z
	temperature = temperature
	component_flux = 2
	thermal_conductivity = k_val
  []
  [diffuse]
    type = DiffusionTemperature
    variable = temperature
	
	q_x = q_x
	q_y = q_y
	q_z = q_z
  []
  [diffuse_time]
    type = DiffusionTemperatureTimeDerivative
    variable = temperature
	
	rho_c = rho_c_val
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
    prop_names = 'k_val rho_c_val'
    prop_values = '1.0 0.0001'
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

[ICs]
  [initial_temp]
	type = ConstantIC
	variable = temperature
	value = 0.0
  []
[]

[Preconditioning]
  [smp]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Transient
  solve_type = 'PJFNK'
  
  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
  
  start_time = 0.0
  end_time = 0.1
  
  [TimeStepper]
    type = ConstantDT
    growth_factor=2
    cutback_factor_at_failure=0.5
    dt = 0.00005
  []
  [Predictor]
    type = SimplePredictor
    scale = 1.0
    skip_after_failed_timestep = true
  []
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
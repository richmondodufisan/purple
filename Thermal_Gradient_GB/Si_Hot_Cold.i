kappa_val = 9.00
density_c_val = ${fparse 2630 * 741.79}


[Mesh]
  second_order = true

  [sample_mesh]
    type = FileMeshGenerator
    file = simple_box_3D.msh
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
#  [diffuse_time]
#    type = DiffusionTemperatureTimeDerivative
#    variable = temperature
#	
#	rho_c = rho_c_val
#  []
[]

[Materials]
  [simulation_constants]
    type = ADGenericConstantMaterial
    prop_names = 'k_val rho_c_val'
    prop_values = '${kappa_val} ${density_c_val}'
  []
[]

[BCs]
  [left_val]
    type = DirichletBC
    variable = temperature
    boundary = 'left'
    value = 1000
  []
  [right_val]
    type = DirichletBC
    variable = temperature
    boundary = 'right'
    value = 300
  []
[]

#[ICs]
#  [initial_temp]
#	type = ConstantIC
#	variable = temperature
#	value = 300
#  []
#[]

[Preconditioning]
  [smp]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Steady
  solve_type = 'NEWTON'
  
  nl_rel_tol = 1e-15
  nl_abs_tol = 1e-15
  l_tol = 1e-8
  l_max_its = 300
  nl_max_its = 20
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

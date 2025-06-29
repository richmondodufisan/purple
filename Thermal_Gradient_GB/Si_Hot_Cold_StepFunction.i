kappa_bulk_val = 130.00
kappa_gb_val = 56.52

gb_width_val = 20
gb_start_loc = 50

density_c_val = ${fparse 2630 * 741.79}


[Mesh]
  second_order = true

  [sample_mesh]
    type = FileMeshGenerator
    file = simple_box_2D.msh
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
[]

[Functions]
  [grain_boundary_function]
    type = ParsedFunction
    expression = 'if((x < gb_start) | (x > (gb_start + gb_width)), k_bulk, k_gb)'
    symbol_names = 'gb_width gb_start k_bulk k_gb'
    symbol_values = '${gb_width_val} ${gb_start_loc} ${kappa_bulk_val} ${kappa_gb_val}'
  []
[]

[Materials]
  [simulation_constants]
    type = ADGenericConstantMaterial
    prop_names = 'rho_c_val'
    prop_values = '${density_c_val}'
  []
  [thermal_conductivity_sample]
    type = ADGenericFunctionMaterial
    prop_names = k_val
    prop_values = grain_boundary_function
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


[Postprocessors]
  [temp_left_gb]
    type = PointValue
    variable = temperature
    point = '50 10 0'
  []
  [temp_right_gb]
    type = PointValue
    variable = temperature
    point = '70 10 0'
  []
[]




[VectorPostprocessors]
  [temp_profile_x]
    type = LineValueSampler
    variable = temperature
    start_point = '0 10 0'
    end_point = '120 10 0'
    num_points = 500
    sort_by = x
  []
  [flux_profile_x]
    type = LineValueSampler
    variable = q_x
    start_point = '0 10 0'
    end_point = '120 10 0'
    num_points = 500
    sort_by = x
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
  solve_type = 'NEWTON'
  
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'


  nl_rel_tol = 1e-10
  nl_abs_tol = 1e-10
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
[]

[Outputs]
  print_linear_residuals = false
  csv = true
  exodus = true
[]

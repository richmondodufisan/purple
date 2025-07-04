kappa_bulk_val = 130.00

#resistance_val = 3.53857042e-01
#resistance_val = 1.98920351e-01
resistance_val = 0.20006


conductance_val = ${fparse 1.0/resistance_val}

density_c_val = ${fparse 2630 * 741.79}


[Mesh]
  second_order = true

  [sample_mesh]
    type = FileMeshGenerator
    file = simple_box_2D_5_0.msh
  []
  
  [left_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_mesh
    block_id = 1
    top_right = '60 20 0'
    bottom_left = '0 0 0'
  []
  [right_block]
    type = SubdomainBoundingBoxGenerator
    input = left_block
    block_id = 2	
    top_right = '120 20 0'
    bottom_left = '60 0 0'
  []
  [rename]
    type = RenameBlockGenerator
    old_block = '1 2'
    new_block = 'sample_left sample_right'
    input = right_block
  []
  [conductance_area]	
    type = SideSetsBetweenSubdomainsGenerator
    input = rename
    primary_block = sample_left
    paired_block = sample_right
    new_boundary = 'boundary_conductance'
  []
[]

[Variables]
  [q_x_left]
    order = SECOND
    family = LAGRANGE
	block = sample_left
  []
  [q_y_left]
    order = SECOND
    family = LAGRANGE
	block = sample_left
  []
  [q_z_left]
    order = SECOND
    family = LAGRANGE
	block = sample_left
  []
  [temperature_left]
    order = FIRST
    family = LAGRANGE
	block = sample_left
  []
  
  
  [q_x_right]
    order = SECOND
    family = LAGRANGE
	block = sample_right
  []
  [q_y_right]
    order = SECOND
    family = LAGRANGE
	block = sample_right
  []
  [q_z_right]
    order = SECOND
    family = LAGRANGE
	block = sample_right
  []
  [temperature_right]
    order = FIRST
    family = LAGRANGE
	block = sample_right
  []
[]


[Kernels]
  [heat_x_left]
    type = FourierHeatEquation
    variable = q_x_left
	temperature = temperature_left
	component_flux = 0
	thermal_conductivity = k_val
	block = sample_left
  []
  [heat_y_left]
    type = FourierHeatEquation
    variable = q_y_left
	temperature = temperature_left
	component_flux = 1
	thermal_conductivity = k_val
	block = sample_left
  []
  [heat_z_left]
    type = FourierHeatEquation
    variable = q_z_left
	temperature = temperature_left
	component_flux = 2
	thermal_conductivity = k_val
	block = sample_left
  []
  [diffuse_left]
    type = DiffusionTemperature
    variable = temperature_left
	
	q_x = q_x_left
	q_y = q_y_left
	q_z = q_z_left
	
	block = sample_left
  []
  
  
  
  [heat_x_right]
    type = FourierHeatEquation
    variable = q_x_right
	temperature = temperature_right
	component_flux = 0
	thermal_conductivity = k_val
	block = sample_right
  []
  [heat_y_right]
    type = FourierHeatEquation
    variable = q_y_right
	temperature = temperature_right
	component_flux = 1
	thermal_conductivity = k_val
	block = sample_right
  []
  [heat_z_right]
    type = FourierHeatEquation
    variable = q_z_right
	temperature = temperature_right
	component_flux = 2
	thermal_conductivity = k_val
	block = sample_right
  []
  [diffuse_right]
    type = DiffusionTemperature
    variable = temperature_right
	
	q_x = q_x_right
	q_y = q_y_right
	q_z = q_z_right
	
	block = sample_right
  []
[]



[InterfaceKernels]
  [interface]
    type = SideSetHeatTransferKernel
    variable = temperature_left
    neighbor_var = temperature_right
    boundary = 'boundary_conductance'
	conductance = ${conductance_val}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
[]



[Materials]
  [simulation_constants]
    type = ADGenericConstantMaterial
    prop_names = 'k_val rho_c_val'
    prop_values = '${kappa_bulk_val} ${density_c_val}'
  []
[]

[BCs]
  [left_val]
    type = DirichletBC
    variable = temperature_left
    boundary = 'left'
    value = 1000
  []
  [right_val]
    type = DirichletBC
    variable = temperature_right
    boundary = 'right'
    value = 300
  []
[]


[Postprocessors]
  [temp_left_gb]
    type = PointValue
    variable = temperature_left
    point = '59 10 0'
  []
  [temp_right_gb]
    type = PointValue
    variable = temperature_right
    point = '61 10 0'
  []
[]




[VectorPostprocessors]
  [temp_profile_x_left]
    type = LineValueSampler
    variable = temperature_left
    start_point = '0 10 0'
    end_point = '59 10 0'
    num_points = 250
    sort_by = x
  []
  [flux_profile_x_left]
    type = LineValueSampler
    variable = q_x_left
    start_point = '0 10 0'
    end_point = '59 10 0'
    num_points = 250
    sort_by = x
  []
  
  [temp_profile_x_right]
    type = LineValueSampler
    variable = temperature_right
    start_point = '61 10 0'
    end_point = '120 10 0'
    num_points = 250
    sort_by = x
  []
  [flux_profile_x_right]
    type = LineValueSampler
    variable = q_x_right
    start_point = '61 10 0'
    end_point = '120 10 0'
    num_points = 250
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


  nl_rel_tol = 1e-15
  nl_abs_tol = 1e-15
  l_tol = 1e-10
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
[]

[Outputs]
  print_linear_residuals = false
  csv = true
  exodus = true
[]

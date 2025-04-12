#Global Parameters
x0_val = 2
y0_val = 0
freq_val = 1e6

transducer_thickness = 0.09
probe_radius = 6.7
pump_radius = 7.65

w_Probe = ${fparse probe_radius * sqrt(2)}
w_Pump = ${fparse pump_radius * sqrt(2)}

offset = 0
gaussian_order = 2.0

pump_power = 0.01
pump_absorbance = 1
gb_width_val = 0.1
kappa_bulk_si = 130e-6
kappa_gb_si = 56.52e-6
rho_si = 2.329e-15
c_si = 0.6891e3
au_si_conductance = -3e-5
au_si_conductance_positive = 3e-5
kappa_bulk_au = 215e-6
rho_au = 19.3e-15
c_au = 0.1287e3

theta_deg = 0
theta_rad = ${fparse (theta_deg/180)*pi}

[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = FDTR_mesh.msh
  []
  [sample_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_mesh
    block_id = 1
    top_right = '160 80 0'
    bottom_left = '-160 -80 -40'
  []
  [transducer_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block
    block_id = 2	
    top_right = '160 80 ${transducer_thickness}'
    bottom_left = '-160 -80 0'
  []
  
  [rename]
    type = RenameBlockGenerator
    old_block = '1 2'
    new_block = 'sample_material transducer_material'
    input = transducer_block
  []
  
  [applied_pump_area]
    type = ParsedGenerateSideset
	input = rename
	combinatorial_geometry = '(z > ${transducer_thickness}-1e-8) & (z < ${transducer_thickness}+1e-8)'
	constant_names = 'x0 y0'
	constant_expressions = '${x0_val} ${y0_val}'
	new_sideset_name = top_pump_area
  []
  
  [applied_pump_sample]
    type = ParsedGenerateSideset
	input = applied_pump_area
	combinatorial_geometry = '(z > 0.0-1e-8) & (z < 0.0+1e-8)'
	constant_names = 'x0 y0'
	constant_expressions = '${x0_val} ${y0_val}'
	new_sideset_name = sample_pump_area
  []
  
  [conductance_area]	
    type = SideSetsBetweenSubdomainsGenerator
    input = applied_pump_sample
    primary_block = transducer_material
    paired_block = sample_material
    new_boundary = 'boundary_conductance'
  []
    
  [bottom_area]
    type = ParsedGenerateSideset
	input = conductance_area
	combinatorial_geometry = '((z > -40-1e-8) & (z < -40+1e-8))'
	new_sideset_name = bottom_surface
  []
  
  [side_areas]
    type = ParsedGenerateSideset
	input = bottom_area
	combinatorial_geometry = '((x > -160-1e-8) & (x < -160+1e-8)) | ((x > 160-1e-8) & (x < 160+1e-8)) | ((y > -80-1e-8) & (y < -80+1e-8)) | ((y > 80-1e-8) & (y < 80+1e-8))'
	new_sideset_name = side_surfaces
  []
[]

[Variables]
  [temp_trans_real]
    order = FIRST
    family = LAGRANGE
	block = transducer_material
  []
  [temp_trans_imag]
    order = FIRST
    family = LAGRANGE
	block = transducer_material
  []
  [temp_samp_real]
    order = FIRST
    family = LAGRANGE
	block = sample_material
  []
  [temp_samp_imag]
    order = FIRST
    family = LAGRANGE
	block = sample_material
  []
[]

[Kernels]
  [heat_conduction_transducer_real]
    type = HeatConductionSteadyReal
	
    variable = temp_trans_real
	imaginary_temp = temp_trans_imag
	
	thermal_conductivity = k_trans
	heat_capacity = c_trans
	omega = omega
	density = rho_trans 
	
	block = transducer_material
  []
  [heat_conduction_transducer_imag]
    type = HeatConductionSteadyImag
	
    variable = temp_trans_imag
	real_temp = temp_trans_real
	
	thermal_conductivity = k_trans
	heat_capacity = c_trans
	omega = omega
	density = rho_trans 
	
	block = transducer_material
  []
  
  
  [heat_conduction_sample_real]
    type = HeatConductionSteadyReal
	
    variable = temp_samp_real
	imaginary_temp = temp_samp_imag
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = sample_material
  []
  [heat_conduction_sample_imag]
    type = HeatConductionSteadyImag
	
    variable = temp_samp_imag
	real_temp = temp_samp_real
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = sample_material
  []
[]

[InterfaceKernels]
  [interface_real]
    type = SideSetHeatTransferKernel
    variable = temp_trans_real
    neighbor_var = temp_samp_real
    boundary = 'boundary_conductance'
	conductance = ${au_si_conductance}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [interface_imag]
    type = SideSetHeatTransferKernel
    variable = temp_trans_imag
    neighbor_var = temp_samp_imag
    boundary = 'boundary_conductance'
	conductance = ${au_si_conductance_positive}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
[]




[UserObjects]
  [average_flux_x]
    type = LayeredAverage
    variable = flux_x
    direction = x
    num_layers = 321
	block = sample_material
  []
  [average_flux_y]
    type = LayeredAverage
    variable = flux_y
    direction = x
    num_layers = 321
	block = sample_material
  []
  [average_flux_z]
    type = LayeredAverage
    variable = flux_z
    direction = x
    num_layers = 321
	block = sample_material
  []
[]





[AuxVariables]
  [avg_surf_temp_real]
  []
  [avg_surf_temp_imag]
  []
  
  [grad_tx_real]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_ty_real]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tz_real]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tx_imag]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_ty_imag]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tz_imag]
    family = MONOMIAL
    order = CONSTANT
  []
  
  
  
  [grad_mag_x]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_mag_y]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_mag_z]
    family = MONOMIAL
    order = CONSTANT
  []
  
  
  [flux_x]
    family = MONOMIAL
    order = CONSTANT
  []
  [flux_y]
    family = MONOMIAL
    order = CONSTANT
  []
  [flux_z]
    family = MONOMIAL
    order = CONSTANT
  []
  
  
  [avg_flux_x]
    family = MONOMIAL
    order = CONSTANT
  []
  [avg_flux_y]
    family = MONOMIAL
    order = CONSTANT
  []
  [avg_flux_z]
    family = MONOMIAL
    order = CONSTANT
  []
[]

[AuxKernels]
  [average_surface_temperature_real]
    type = ParsedAux
    variable = avg_surf_temp_real
    coupled_variables = 'temp_trans_real'
	constant_names = 'x0 y0 w_Probe pi'
	constant_expressions = '${x0_val} ${y0_val} ${w_Probe} 3.14159265359'
	use_xyzt = true
	expression = '((2 * temp_trans_real)/(pi*(w_Probe^2)))*exp((-2 * ((x-x0)^2+(y-y0)^2))/(w_Probe^2))'
	block = transducer_material
  []
  [average_surface_temperature_imag]
    type = ParsedAux
    variable = avg_surf_temp_imag
    coupled_variables = 'temp_trans_imag'
	constant_names = 'x0 y0 w_Probe pi'
	constant_expressions = '${x0_val} ${y0_val} ${w_Probe} 3.14159265359'
	use_xyzt = true
	expression = '((2 * temp_trans_imag)/(pi*(w_Probe^2)))*exp((-2 * ((x-x0)^2+(y-y0)^2))/(w_Probe^2))'
	block = transducer_material
  []
  
  
  [grad_tx_real_aux]
    type = VariableGradientComponent
    variable = grad_tx_real
    component = x
    gradient_variable = temp_samp_real
    block = 'sample_material'
  []

  [grad_ty_real_aux]
    type = VariableGradientComponent
    variable = grad_ty_real
    component = y
    gradient_variable = temp_samp_real
    block = 'sample_material'
  []

  [grad_tz_real_aux]
    type = VariableGradientComponent
    variable = grad_tz_real
    component = z
    gradient_variable = temp_samp_real
    block = 'sample_material'
  []

  [grad_tx_imag_aux]
    type = VariableGradientComponent
    variable = grad_tx_imag
    component = x
    gradient_variable = temp_samp_imag
    block = 'sample_material'
  []

  [grad_ty_imag_aux]
    type = VariableGradientComponent
    variable = grad_ty_imag
    component = y
    gradient_variable = temp_samp_imag
    block = 'sample_material'
  []

  [grad_tz_imag_aux]
    type = VariableGradientComponent
    variable = grad_tz_imag
    component = z
    gradient_variable = temp_samp_imag
    block = 'sample_material'
  []
  
  
  
  
  [grad_mag_x_aux]
    type = ParsedAux
    variable = grad_mag_x
    coupled_variables = 'grad_tx_real grad_tx_imag'
    expression = 'sqrt(grad_tx_real^2 + grad_tx_imag^2)'
    block = 'sample_material'
  []

  [grad_mag_y_aux]
    type = ParsedAux
    variable = grad_mag_y
    coupled_variables = 'grad_ty_real grad_ty_imag'
    expression = 'sqrt(grad_ty_real^2 + grad_ty_imag^2)'
    block = 'sample_material'
  []

  [grad_mag_z_aux]
    type = ParsedAux
    variable = grad_mag_z
    coupled_variables = 'grad_tz_real grad_tz_imag'
    expression = 'sqrt(grad_tz_real^2 + grad_tz_imag^2)'
    block = 'sample_material'
  []
  
  
  [flux_x_aux]
    type = ParsedAux
    variable = flux_x
    coupled_variables = 'grad_mag_x'
	material_properties = 'k_samp_no_ad'
    expression = 'grad_mag_x/k_samp_no_ad'
    block = 'sample_material'
  []

  [flux_y_aux]
    type = ParsedAux
    variable = flux_y
    coupled_variables = 'grad_mag_y'
	material_properties = 'k_samp_no_ad'
    expression = 'grad_mag_y/k_samp_no_ad'
    block = 'sample_material'
  []

  [flux_z_aux]
    type = ParsedAux
    variable = flux_z
    coupled_variables = 'grad_mag_z'
	material_properties = 'k_samp_no_ad'
    expression = 'grad_mag_z/k_samp_no_ad'
    block = 'sample_material'
  []


  [layered_average_x]
    type = SpatialUserObjectAux
    variable = avg_flux_x
    execute_on = timestep_end
    user_object = average_flux_x
  []
  [layered_average_y]
    type = SpatialUserObjectAux
    variable = avg_flux_y
    execute_on = timestep_end
    user_object = average_flux_y
  []
  [layered_average_z]
    type = SpatialUserObjectAux
    variable = avg_flux_z
    execute_on = timestep_end
    user_object = average_flux_z
  []


[]

[Postprocessors]
  [integral_trans_real]
    type = SideIntegralVariablePostprocessor
    boundary = 'top_pump_area'
    variable = avg_surf_temp_real
  []
  [integral_trans_imag]
    type = SideIntegralVariablePostprocessor
    boundary = 'top_pump_area'
    variable = avg_surf_temp_imag
  []
[]


[VectorPostprocessors]
  # sample at z = -0.02 to remove discontinuity warning
  # it is still the same as sampling at z = 0
  # it is an average value
  [flux_profile_x]
    type = LineValueSampler
    variable = avg_flux_x
    start_point = '-30 0 -0.02'
    end_point = '30 0 -0.02'
    num_points = 321
    sort_by = x
  []
  [flux_profile_y]
    type = LineValueSampler
    variable = avg_flux_y
    start_point = '-30 0 -0.02'
    end_point = '30 0 -0.02'
    num_points = 321
    sort_by = x
  []
  [flux_profile_z]
    type = LineValueSampler
    variable = avg_flux_z
    start_point = '-30 0 -0.02'
    end_point = '30 0 -0.02'
    num_points = 321
    sort_by = x
  []
[]


[Functions]
  [grain_boundary_function]
    type = ParsedFunction
	expression = 'if ( (x<((-gb_width/(2*cos(theta)))+(abs(z)*tan(theta)))) | (x>((gb_width/(2*cos(theta)))+(abs(z)*tan(theta)))), k_bulk, k_gb)'
	symbol_names = 'gb_width theta k_bulk k_gb'
	symbol_values = '${gb_width_val} ${theta_rad} ${kappa_bulk_si} ${kappa_gb_si}'
  []
  [angular_frequency]
	type = ParsedFunction
	expression = '2 * pi * freq'
	symbol_names = 'freq'
    symbol_values = '${freq_val}'
  []
[]

[Materials]
  [basic_transducer_materials]
    type = ADGenericConstantMaterial
    block = transducer_material
    prop_names = 'rho_trans c_trans k_trans'
    prop_values = '${rho_au} ${c_au} ${kappa_bulk_au}'
  []
  [basic_sample_materials]
    type = ADGenericConstantMaterial
    block = sample_material
    prop_names = 'rho_samp c_samp'
    prop_values = '${rho_si} ${c_si}'
  []
  [simulation_frequency]
    type = ADGenericFunctionMaterial
	prop_names = omega
    prop_values = angular_frequency
	block = 'transducer_material sample_material'
  []
  [thermal_conductivity_sample]
    type = ADGenericFunctionMaterial
    prop_names = k_samp
    prop_values = grain_boundary_function
	block = sample_material
  []
  
  [k_samp_for_aux]
    type = MaterialADConverter
    ad_props_in = k_samp
    reg_props_out = k_samp_no_ad
	block = 'sample_material'
  []
[]

[BCs]
  [ambient_temperature_real]
    type = DirichletBC
    variable = temp_samp_real
    boundary = 'bottom_surface'
    value = 0
  []
  [ambient_temperature_imag]
    type = DirichletBC
    variable = temp_samp_imag
    boundary = 'bottom_surface'
    value = 0
  []
  
  
  [heat_source_term_real]
    type = PumpSuperGaussianRing
	variable = temp_trans_real
	boundary = 'top_pump_area'
	
	pump_power = ${pump_power}
	absorbance = ${pump_absorbance}
	pump_spot_size = ${w_Pump}
	offset = ${offset}
	order = ${gaussian_order}
	center_x = ${x0_val}
	center_y = ${y0_val}
  []
  [heat_source_term_imag]
    type = NeumannBC
	variable = temp_trans_imag
	boundary = 'top_pump_area'
	value = 0
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
  print_linear_residuals = false
  csv = true
  exodus = true
[]

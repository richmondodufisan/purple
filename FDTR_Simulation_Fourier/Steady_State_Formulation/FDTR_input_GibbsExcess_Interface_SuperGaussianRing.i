#Global Parameters
x0_val = 0
y0_val = 0
freq_val = 1e6

transducer_thickness = 0.09
probe_radius = 1.34
pump_radius = 1.53

w_Probe = ${fparse probe_radius * sqrt(2)}
w_Pump = ${fparse pump_radius * sqrt(2)}

offset = 5
gaussian_order = 2.0

pump_power = 0.01
pump_absorbance = 1

kappa_bulk_si = 130e-6
rho_si = 2.329e-15
c_si = 0.6891e3

kappa_bulk_au = 215e-6
rho_au = 19.3e-15
c_au = 0.1287e3


au_si_conductance = -3e-5
au_si_conductance_positive = 3e-5

si_si_conductance = -5.6e-4
si_si_conductance_positive = 5.6e-4


theta_deg = 0
theta_rad = ${fparse (theta_deg/180)*pi}

gb_face_val = ${fparse int(-tan(theta_rad))}


flux_depth = -1


[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = FDTR_mesh.msh
  []
  
  [transducer_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_mesh
    block_id = 1	
    top_right = '160 80 ${transducer_thickness}'
    bottom_left = '-160 -80 0'
  []
  
  [left_sample_side]
    type = ParsedSubdomainMeshGenerator
	input = transducer_block
	combinatorial_geometry = '(x < (${gb_face_val} * z)) & (z < 0.0)'
	block_id = 2
  []
  
  [right_sample_side]
    type = ParsedSubdomainMeshGenerator
	input = left_sample_side
	combinatorial_geometry = '(x > (${gb_face_val} * z)) & (z < 0.0)'
	block_id = 3
  []
  
  [rename]
    type = RenameBlockGenerator
    old_block = '1 2 3'
    new_block = 'transducer_material sample_material_left sample_material_right'
    input = right_sample_side
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
  
  [conductance_area_1]	
    type = SideSetsBetweenSubdomainsGenerator
    input = applied_pump_sample
    primary_block = transducer_material
    paired_block = sample_material_left
    new_boundary = 'trans_left_sample_boundary'
  []
  
  [conductance_area_2]	
    type = SideSetsBetweenSubdomainsGenerator
    input = conductance_area_1
    primary_block = transducer_material
    paired_block = sample_material_right
    new_boundary = 'trans_right_sample_boundary'
  []
  
  [gb_area]	
    type = SideSetsBetweenSubdomainsGenerator
    input = conductance_area_2
    primary_block = sample_material_left
    paired_block = sample_material_right
    new_boundary = 'gb_interface'
  []
    
  [bottom_area]
    type = ParsedGenerateSideset
	input = gb_area
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
  [temp_samp_left_real]
    order = FIRST
    family = LAGRANGE
	block = sample_material_left
  []
  [temp_samp_left_imag]
    order = FIRST
    family = LAGRANGE
	block = sample_material_left
  []
  [temp_samp_right_real]
    order = FIRST
    family = LAGRANGE
	block = sample_material_right
  []
  [temp_samp_right_imag]
    order = FIRST
    family = LAGRANGE
	block = sample_material_right
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
  
  
  [heat_conduction_sample_left_real]
    type = HeatConductionSteadyReal
	
    variable = temp_samp_left_real
	imaginary_temp = temp_samp_left_imag
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = sample_material_left
  []
  [heat_conduction_sample_left_imag]
    type = HeatConductionSteadyImag
	
    variable = temp_samp_left_imag
	real_temp = temp_samp_left_real
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = sample_material_left
  []
  
  
  [heat_conduction_sample_right_real]
    type = HeatConductionSteadyReal
	
    variable = temp_samp_right_real
	imaginary_temp = temp_samp_right_imag
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = sample_material_right
  []
  [heat_conduction_sample_right_imag]
    type = HeatConductionSteadyImag
	
    variable = temp_samp_right_imag
	real_temp = temp_samp_right_real
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = sample_material_right
  []
[]

[InterfaceKernels]
  [interface_left_real]
    type = SideSetHeatTransferKernel
    variable = temp_trans_real
    neighbor_var = temp_samp_left_real
    boundary = 'trans_left_sample_boundary'
	conductance = ${au_si_conductance}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [interface_left_imag]
    type = SideSetHeatTransferKernel
    variable = temp_trans_imag
    neighbor_var = temp_samp_left_imag
    boundary = 'trans_left_sample_boundary'
	conductance = ${au_si_conductance_positive}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [interface_right_real]
    type = SideSetHeatTransferKernel
    variable = temp_trans_real
    neighbor_var = temp_samp_right_real
    boundary = 'trans_right_sample_boundary'
	conductance = ${au_si_conductance}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [interface_right_imag]
    type = SideSetHeatTransferKernel
    variable = temp_trans_imag
    neighbor_var = temp_samp_right_imag
    boundary = 'trans_right_sample_boundary'
	conductance = ${au_si_conductance_positive}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [gb_real]
    type = SideSetHeatTransferKernel
    variable = temp_samp_left_real
    neighbor_var = temp_samp_right_real
    boundary = 'gb_interface'
	conductance = ${si_si_conductance}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [gb_imag]
    type = SideSetHeatTransferKernel
    variable = temp_samp_left_imag
    neighbor_var = temp_samp_right_imag
    boundary = 'gb_interface'
	conductance = ${si_si_conductance_positive}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
[]

[AuxVariables]
  [avg_surf_temp_real]
  []
  [avg_surf_temp_imag]
  []
  
  [grad_tx_real_left]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_ty_real_left]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tz_real_left]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tx_imag_left]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_ty_imag_left]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tz_imag_left]
    family = MONOMIAL
    order = CONSTANT
  []
  
  
  
  [flux_x_left]
    family = MONOMIAL
    order = CONSTANT
  []
  [flux_y_left]
    family = MONOMIAL
    order = CONSTANT
  []
  [flux_z_left]
    family = MONOMIAL
    order = CONSTANT
  []
  
  
  
  
  [grad_tx_real_right]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_ty_real_right]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tz_real_right]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tx_imag_right]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_ty_imag_right]
    family = MONOMIAL
    order = CONSTANT
  []
  [grad_tz_imag_right]
    family = MONOMIAL
    order = CONSTANT
  []
  
  
  
  [flux_x_right]
    family = MONOMIAL
    order = CONSTANT
  []
  [flux_y_right]
    family = MONOMIAL
    order = CONSTANT
  []
  [flux_z_right]
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
  
  
  [grad_tx_real_left_aux]
    type = VariableGradientComponent
    variable = grad_tx_real_left
    component = x
    gradient_variable = temp_samp_left_real
    block = 'sample_material_left'
  []

  [grad_ty_real_left_aux]
    type = VariableGradientComponent
    variable = grad_ty_real_left
    component = y
    gradient_variable = temp_samp_left_real
    block = 'sample_material_left'
  []

  [grad_tz_real_left_aux]
    type = VariableGradientComponent
    variable = grad_tz_real_left
    component = z
    gradient_variable = temp_samp_left_real
    block = 'sample_material_left'
  []

  [grad_tx_imag_left_aux]
    type = VariableGradientComponent
    variable = grad_tx_imag_left
    component = x
    gradient_variable = temp_samp_left_imag
    block = 'sample_material_left'
  []

  [grad_ty_imag_left_aux]
    type = VariableGradientComponent
    variable = grad_ty_imag_left
    component = y
    gradient_variable = temp_samp_left_imag
    block = 'sample_material_left'
  []

  [grad_tz_imag_left_aux]
    type = VariableGradientComponent
    variable = grad_tz_imag_left
    component = z
    gradient_variable = temp_samp_left_imag
    block = 'sample_material_left'
  []
  
  
  
  
  [flux_x_left_aux]
    type = ParsedAux
    variable = flux_x_left
    coupled_variables = 'grad_tx_real_left grad_tx_imag_left'
	material_properties = 'k_samp_no_ad'
    expression = '(sqrt(grad_tx_real_left^2 + grad_tx_imag_left^2))/k_samp_no_ad'
    block = sample_material_left
  []

  [flux_y_left_aux]
    type = ParsedAux
    variable = flux_y_left
    coupled_variables = 'grad_ty_real_left grad_ty_imag_left'
	material_properties = 'k_samp_no_ad'
    expression = '(sqrt(grad_ty_real_left^2 + grad_ty_imag_left^2))/k_samp_no_ad'
    block = sample_material_left
  []

  [flux_z_left_aux]
    type = ParsedAux
    variable = flux_z_left
    coupled_variables = 'grad_tz_real_left grad_tz_imag_left'
	material_properties = 'k_samp_no_ad'
    expression = '(sqrt(grad_tz_real_left^2 + grad_tz_imag_left^2))/k_samp_no_ad'
    block = sample_material_left
  []
  
  
  
  
  
  



  [grad_tx_real_right_aux]
    type = VariableGradientComponent
    variable = grad_tx_real_right
    component = x
    gradient_variable = temp_samp_right_real
    block = 'sample_material_right'
  []

  [grad_ty_real_right_aux]
    type = VariableGradientComponent
    variable = grad_ty_real_right
    component = y
    gradient_variable = temp_samp_right_real
    block = 'sample_material_right'
  []

  [grad_tz_real_right_aux]
    type = VariableGradientComponent
    variable = grad_tz_real_right
    component = z
    gradient_variable = temp_samp_right_real
    block = 'sample_material_right'
  []

  [grad_tx_imag_right_aux]
    type = VariableGradientComponent
    variable = grad_tx_imag_right
    component = x
    gradient_variable = temp_samp_right_imag
    block = 'sample_material_right'
  []

  [grad_ty_imag_right_aux]
    type = VariableGradientComponent
    variable = grad_ty_imag_right
    component = y
    gradient_variable = temp_samp_right_imag
    block = 'sample_material_right'
  []

  [grad_tz_imag_right_aux]
    type = VariableGradientComponent
    variable = grad_tz_imag_right
    component = z
    gradient_variable = temp_samp_right_imag
    block = 'sample_material_right'
  []
  
  
  
  
  [flux_x_right_aux]
    type = ParsedAux
    variable = flux_x_right
    coupled_variables = 'grad_tx_real_right grad_tx_imag_right'
	material_properties = 'k_samp_no_ad'
    expression = '(sqrt(grad_tx_real_right^2 + grad_tx_imag_right^2))/k_samp_no_ad'
    block = sample_material_right
  []

  [flux_y_right_aux]
    type = ParsedAux
    variable = flux_y_right
    coupled_variables = 'grad_ty_real_right grad_ty_imag_right'
	material_properties = 'k_samp_no_ad'
    expression = '(sqrt(grad_ty_real_right^2 + grad_ty_imag_right^2))/k_samp_no_ad'
    block = sample_material_right
  []

  [flux_z_right_aux]
    type = ParsedAux
    variable = flux_z_right
    coupled_variables = 'grad_tz_real_right grad_tz_imag_right'
	material_properties = 'k_samp_no_ad'
    expression = '(sqrt(grad_tz_real_right^2 + grad_tz_imag_right^2))/k_samp_no_ad'
    block = sample_material_right
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
  [q_n_gb_flux_left]
    type = PointValue
    variable = flux_x_left
    point = '0 0 ${flux_depth}'
  []
  [q_n_gb_flux_right]
    type = PointValue
    variable = flux_x_right
    point = '0 0 ${flux_depth}'
  []
[]



[VectorPostprocessors]
  [flux_profile_x_left]
    type = LineValueSampler
    variable = flux_x_left
    start_point = '-30 0 ${flux_depth}'
    end_point = '0 0 ${flux_depth}'
    num_points = 5000
    sort_by = x
  []
  [flux_profile_y_left]
    type = LineValueSampler
    variable = flux_y_left
    start_point = '-30 0 ${flux_depth}'
    end_point = '0 0 ${flux_depth}'
    num_points = 5000
    sort_by = x
  []
  [flux_profile_z_left]
    type = LineValueSampler
    variable = flux_z_left
    start_point = '-30 0 ${flux_depth}'
    end_point = '0 0 ${flux_depth}'
    num_points = 5000
    sort_by = x
  []
  
  
  
  
  [flux_profile_x_right]
    type = LineValueSampler
    variable = flux_x_right
    start_point = '0 0 ${flux_depth}'
    end_point = '30 0 ${flux_depth}'
    num_points = 5000
    sort_by = x
  []
  [flux_profile_y_right]
    type = LineValueSampler
    variable = flux_y_right
    start_point = '0 0 ${flux_depth}'
    end_point = '30 0 ${flux_depth}'
    num_points = 5000
    sort_by = x
  []
  [flux_profile_z_right]
    type = LineValueSampler
    variable = flux_z_right
    start_point = '0 0 ${flux_depth}'
    end_point = '30 0 ${flux_depth}'
    num_points = 5000
    sort_by = x
  []
[]




[Functions]
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
    block = 'sample_material_left sample_material_right'
    prop_names = 'rho_samp c_samp k_samp'
    prop_values = '${rho_si} ${c_si} ${kappa_bulk_si}'
  []
  [simulation_frequency]
    type = ADGenericFunctionMaterial
	prop_names = omega
    prop_values = angular_frequency
	block = 'transducer_material sample_material_left sample_material_right'
  []
  
  [k_samp_for_aux]
    type = MaterialADConverter
    ad_props_in = k_samp
    reg_props_out = k_samp_no_ad
	block = 'sample_material_left sample_material_right'
  []
[]

[BCs]
  [ambient_temperature_left_real]
    type = DirichletBC
    variable = temp_samp_left_real
    boundary = 'bottom_surface'
    value = 0
  []
  [ambient_temperature_right_real]
    type = DirichletBC
    variable = temp_samp_right_real
    boundary = 'bottom_surface'
    value = 0
  []
  [ambient_temperature_left_imag]
    type = DirichletBC
    variable = temp_samp_left_imag
    boundary = 'bottom_surface'
    value = 0
  []
  [ambient_temperature_right_imag]
    type = DirichletBC
    variable = temp_samp_right_imag
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


#Global Parameters
x0_val = 0
y0_val = 0
freq_val = 1e6

transducer_thickness = 0.09
probe_radius = 1.34
pump_radius = 1.53
pump_power = 0.01
pump_absorbance = 1

kappa_bulk_si = 130e-6
rho_si = 2.329e-15
c_si = 0.6891e3

au_si_conductance = -3e-5
au_si_conductance_positive = 3e-5

si_si_conductance = -5.6e-4
si_si_conductance_positive = 5.6e-4

kappa_bulk_au = 215e-6
rho_au = 19.3e-15
c_au = 0.1287e3

theta_deg = 75
theta_rad = ${fparse (theta_deg/180)*pi}

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
	combinatorial_geometry = '(x < ((-tan(${theta_rad})) * z)) & (z < 0.0)'
	block_id = 2
  []
  
  [right_sample_side]
    type = ParsedSubdomainMeshGenerator
	input = left_sample_side
	combinatorial_geometry = '(x > ((-tan(${theta_rad})) * z)) & (z < 0.0)'
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
    boundary = 'boundary_conductance'
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
    boundary = 'boundary_conductance'
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
    boundary = 'boundary_conductance'
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
    boundary = 'boundary_conductance'
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
    variable = temp_samp_right_imag
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
[]

[AuxKernels]
  [average_surface_temperature_real]
    type = ParsedAux
    variable = avg_surf_temp_real
    coupled_variables = 'temp_trans_real'
	constant_names = 'x0 y0 Rprobe pi'
	constant_expressions = '${x0_val} ${y0_val} ${probe_radius} 3.14159265359'
	use_xyzt = true
	expression = '((temp_trans_real)/(pi*(Rprobe^2)))*exp((-((x-x0)^2+(y-y0)^2))/(Rprobe^2))'
	block = transducer_material
  []
  [average_surface_temperature_imag]
    type = ParsedAux
    variable = avg_surf_temp_imag
    coupled_variables = 'temp_trans_imag'
	constant_names = 'x0 y0 Rprobe pi'
	constant_expressions = '${x0_val} ${y0_val} ${probe_radius} 3.14159265359'
	use_xyzt = true
	expression = '((temp_trans_imag)/(pi*(Rprobe^2)))*exp((-((x-x0)^2+(y-y0)^2))/(Rprobe^2))'
	block = transducer_material
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

[Functions]
  [heat_source_function]
    type = ADParsedFunction
    expression = '-((Q0*absorbance)/(pi*(Rpump^2)))*exp((-((x-x0)^2+(y-y0)^2))/(Rpump^2))'
    symbol_names = 'x0 y0 Rpump Q0 absorbance'
    symbol_values = '${x0_val} ${y0_val} ${pump_radius} ${pump_power} ${pump_absorbance}'
  []
  [angular_frequency]
	type = ADParsedFunction
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
  [heat_source_material]
    type = ADGenericFunctionMaterial
    prop_names = heat_source_mat
    prop_values = heat_source_function
  []
[]

[BCs]
  [ambient_temperature_left_real]
    type = DirichletBC
    variable = temp_samp_left_real
    boundary = 'bottom_surface'
    value = 0
  []
  [ambient_temperature_left_real]
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
    type = FunctionNeumannBC
	variable = temp_trans_real
	boundary = 'top_pump_area'
	function = heat_source_function
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
  interval = 1
  #execute_on = 'initial timestep_end'
  print_linear_residuals = false
  csv = true
  exodus = false
  [pgraph]
    type = PerfGraphOutput
    execute_on = 'final'  # Default is "final"
    level = 1             # Default is 1
  []
[]

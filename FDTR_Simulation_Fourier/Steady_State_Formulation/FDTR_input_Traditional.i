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
kappa_gb_si = 56.52e-6
rho_si = 2.329e-15
c_si = 0.6891e3
au_si_conductance = -3e-5
au_si_conductance_positive = 3e-5
kappa_bulk_au = 215e-6
rho_au = 19.3e-15
c_au = 0.1287e3

[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = FDTR_mesh.msh
  []
  [sample_block_bottom]
    type = SubdomainBoundingBoxGenerator
    input = sample_mesh
    block_id = 1
    top_right = '160 80 -0.6'
    bottom_left = '-160 -80 -40'
  []
  [grain_boundary_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_bottom
    block_id = 2
    top_right = '160 80 -0.5'
    bottom_left = '-160 -80 -0.6'
  []
  [sample_block_top]
    type = SubdomainBoundingBoxGenerator
    input = grain_boundary_block
    block_id = 3
    top_right = '160 80 0'
    bottom_left = '-160 -80 -0.5'
  []
  [transducer_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_top
    block_id = 4	
    top_right = '160 80 ${transducer_thickness}'
    bottom_left = '-160 -80 0'
  []
  
  [rename]
    type = RenameBlockGenerator
    old_block = '1 2 3 4'
    new_block = 'sample_material_bottom gb_material sample_material_top transducer_material'
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
    paired_block = sample_material_top
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
	block = 'sample_material_bottom gb_material sample_material_top'
  []
  [temp_samp_imag]
    order = FIRST
    family = LAGRANGE
	block = 'sample_material_bottom gb_material sample_material_top'
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
	
	block = 'sample_material_bottom sample_material_top'
  []
  [heat_conduction_sample_imag]
    type = HeatConductionSteadyImag
	
    variable = temp_samp_imag
	real_temp = temp_samp_real
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = 'sample_material_bottom sample_material_top'
  []
  
  
  [heat_conduction_gb_real]
    type = HeatConductionSteadyReal
	
    variable = temp_samp_real
	imaginary_temp = temp_samp_imag
	
	thermal_conductivity = k_gb
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = 'gb_material'
  []
  [heat_conduction_gb_imag]
    type = HeatConductionSteadyImag
	
    variable = temp_samp_imag
	real_temp = temp_samp_real
	
	thermal_conductivity = k_gb
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = 'gb_material'
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
    block = 'sample_material_bottom sample_material_top gb_material'
    prop_names = 'rho_samp c_samp k_samp k_gb'
    prop_values = '${rho_si} ${c_si} ${kappa_bulk_si} ${kappa_gb_si}'
  []
  [simulation_frequency]
    type = ADGenericFunctionMaterial
	prop_names = omega
    prop_values = angular_frequency
	block = 'transducer_material sample_material_bottom sample_material_top gb_material'
  []
  [heat_source_material]
    type = ADGenericFunctionMaterial
    prop_names = heat_source_mat
    prop_values = heat_source_function
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

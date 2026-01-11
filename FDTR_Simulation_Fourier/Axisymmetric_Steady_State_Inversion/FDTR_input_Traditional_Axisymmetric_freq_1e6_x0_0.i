#Global Parameters
freq_val = 1e6

transducer_thickness = 0.09
k_trans_z = 215e-6
k_trans_r = 215e-6
rho_trans = 19.3e-15
c_trans = 128.7


sample_thickness = 40
k_samp_z = 130e-6
k_samp_r = 130e-6

k_gb_z = 56.52e-6
k_gb_r = 56.52e-6

rho_samp = 2.329e-15
c_samp = 689.1

conductance_12 = 3e-5

probe_radius = 1.34
pump_radius = 1.53
pump_power = 0.01

w_Probe = ${fparse probe_radius * sqrt(2)}
w_Pump = ${fparse pump_radius * sqrt(2)}

pump_absorbance = 1


si_distance = 1
gb_thickness = 0.01

block_3_val = ${fparse -si_distance}
block_2_val = ${fparse -si_distance-gb_thickness}

[Mesh]
  coord_type = RZ
  [sample_mesh]
    type = FileMeshGenerator
    file = FDTR_mesh.msh
  []
  [sample_block_bottom]
    type = SubdomainBoundingBoxGenerator
    input = sample_mesh
    block_id = 1
    top_right = '40 ${block_2_val} 0'
    bottom_left = '0 -40 0'
  []
  [grain_boundary_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_bottom
    block_id = 2
    top_right = '40 ${block_3_val} 0'
    bottom_left = '0 ${block_2_val} 0'
  []
  [sample_block_top]
    type = SubdomainBoundingBoxGenerator
    input = grain_boundary_block
    block_id = 3
    top_right = '40 0 0'
    bottom_left = '0 ${block_3_val} 0'
  []
  [transducer_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_top
    block_id = 4	
    top_right = '40 ${transducer_thickness} 0'
    bottom_left = '0 0 0'
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
	combinatorial_geometry = '(y > ${transducer_thickness}-1e-8) & (y < ${transducer_thickness}+1e-8)'
	new_sideset_name = top_pump_area
  []
  
  [applied_pump_sample]
    type = ParsedGenerateSideset
	input = applied_pump_area
	combinatorial_geometry = '(y > 0.0-1e-8) & (y < 0.0+1e-8)'
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
	combinatorial_geometry = '((y > -${sample_thickness}-1e-8) & (y < -${sample_thickness}+1e-8))'
	new_sideset_name = bottom_surface
  []
  
  [center_side_boundary]
    type = ParsedGenerateSideset
	input = bottom_area
	combinatorial_geometry = '((x > 0-1e-8) & (x < 0+1e-8))'
	new_sideset_name = center_side
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
    type = HeatConductionSteadyRealAnisotropic
	
    variable = temp_trans_real
	imaginary_temp = temp_trans_imag
	
	thermal_conductivity = k_trans
	heat_capacity = c_trans
	omega = omega
	density = rho_trans 
	
	block = transducer_material
  []
  [heat_conduction_transducer_imag]
    type = HeatConductionSteadyImagAnisotropic
	
    variable = temp_trans_imag
	real_temp = temp_trans_real
	
	thermal_conductivity = k_trans
	heat_capacity = c_trans
	omega = omega
	density = rho_trans 
	
	block = transducer_material
  []
  
  
  [heat_conduction_sample_real]
    type = HeatConductionSteadyRealAnisotropic
	
    variable = temp_samp_real
	imaginary_temp = temp_samp_imag
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = 'sample_material_top sample_material_bottom'
  []
  [heat_conduction_sample_imag]
    type = HeatConductionSteadyImagAnisotropic
	
    variable = temp_samp_imag
	real_temp = temp_samp_real
	
	thermal_conductivity = k_samp
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = 'sample_material_top sample_material_bottom'
  []
  
  
  [heat_conduction_gb_real]
    type = HeatConductionSteadyRealAnisotropic
	
    variable = temp_samp_real
	imaginary_temp = temp_samp_imag
	
	thermal_conductivity = k_gb
	heat_capacity = c_samp
	omega = omega
	density = rho_samp
	
	block = 'gb_material'
  []
  [heat_conduction_gb_imag]
    type = HeatConductionSteadyImagAnisotropic
	
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
	conductance = -${conductance_12}
	
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
	conductance = ${conductance_12}
	
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
	constant_names = 'w_Probe pi'
	constant_expressions = '${w_Probe} 3.14159265359'
	use_xyzt = true
	expression = '((2 * temp_trans_real)/(pi*(w_Probe^2)))*exp((-2 * ((x)^2))/(w_Probe^2))'
	block = transducer_material
  []
  [average_surface_temperature_imag]
    type = ParsedAux
    variable = avg_surf_temp_imag
    coupled_variables = 'temp_trans_imag'
	constant_names = 'w_Probe pi'
	constant_expressions = '${w_Probe} 3.14159265359'
	use_xyzt = true
	expression = '((2 * temp_trans_imag)/(pi*(w_Probe^2)))*exp((-2 * ((x)^2))/(w_Probe^2))'
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
    prop_names = 'rho_trans c_trans'
    prop_values = '${rho_trans} ${c_trans}'
  []
  [transducer_kappa]
    type = ADGenericConstantRankTwoTensor
    tensor_name = k_trans
    # tensor values are column major-ordered
    tensor_values = '${k_trans_r} 0 0 0 ${k_trans_r} 0 0 0 ${k_trans_z}'
	block = transducer_material
  []
  
  
  [basic_sample_materials]
    type = ADGenericConstantMaterial
    block = 'sample_material_top sample_material_bottom gb_material'
    prop_names = 'rho_samp c_samp'
    prop_values = '${rho_samp} ${c_samp}'
  []
  [sample_kappa]
    type = ADGenericConstantRankTwoTensor
    tensor_name = k_samp
    # tensor values are column major-ordered
    tensor_values = '${k_samp_r} 0 0 0 ${k_samp_r} 0 0 0 ${k_samp_z}'
	block = 'sample_material_top sample_material_bottom'
  []
  [gb_kappa]
    type = ADGenericConstantRankTwoTensor
    tensor_name = k_gb
    # tensor values are column major-ordered
    tensor_values = '${k_gb_r} 0 0 0 ${k_gb_r} 0 0 0 ${k_gb_z}'
	block = gb_material
  []
  
  
  [simulation_frequency]
    type = ADGenericFunctionMaterial
	prop_names = omega
    prop_values = angular_frequency
	block = 'transducer_material sample_material_top sample_material_bottom gb_material'
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
    type = PumpConcentricGaussianAxisymmetric
	variable = temp_trans_real
	boundary = 'top_pump_area'
	
	pump_power = ${pump_power}
	absorbance = ${pump_absorbance}
	pump_spot_size = ${w_Pump}
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
  exodus = false
[]


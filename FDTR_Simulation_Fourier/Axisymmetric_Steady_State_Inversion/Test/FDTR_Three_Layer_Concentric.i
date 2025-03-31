#Global Parameters
freq_val = 1e6

transducer_thickness = 0.09
k_trans_z = 215e-6
k_trans_r = 215e-6
rho_trans = 19.3e-15
c_trans = 128.7


sample_thickness_2 = 1.005
k_samp_z_2 = 130e-6
k_samp_r_2 = 130e-6
rho_samp_2 = 2.329e-15
c_samp_2 = 689.1


sample_thickness_3 = 38.995
k_samp_z_3 = 130e-6
k_samp_r_3 = 130e-6
rho_samp_3 = 2.329e-15
c_samp_3 = 689.1


conductance_12 = 3e-5
conductance_23 = 3e-5


probe_radius = 1.34
pump_radius = 1.53
pump_power = 0.01


pump_absorbance = 1

mesh_bottom = ${fparse -sample_thickness_2-sample_thickness_3}


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
    top_right = '40 0 -${sample_thickness_2}'
    bottom_left = '0 0 ${mesh_bottom}'
  []
  [sample_block_top]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_bottom
    block_id = 2
    top_right = '40 0 0'
    bottom_left = '0 0 -${sample_thickness_2}'
  []
  [transducer_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_top
    block_id = 3	
    top_right = '40 0 ${transducer_thickness}'
    bottom_left = '0 0 0'
  []
  
  [rename]
    type = RenameBlockGenerator
    old_block = '1 2 3'
    new_block = 'sample_material_bottom sample_material_top transducer_material'
    input = transducer_block
  []
  
  [applied_pump_area]
    type = ParsedGenerateSideset
	input = rename
	combinatorial_geometry = '(z > ${transducer_thickness}-1e-8) & (z < ${transducer_thickness}+1e-8)'
	new_sideset_name = top_pump_area
  []
  
  [applied_pump_sample]
    type = ParsedGenerateSideset
	input = applied_pump_area
	combinatorial_geometry = '(z > 0.0-1e-8) & (z < 0.0+1e-8)'
	new_sideset_name = sample_pump_area
  []
  
  [conductance_area_12]	
    type = SideSetsBetweenSubdomainsGenerator
    input = applied_pump_sample
    primary_block = transducer_material
    paired_block = sample_material_top
    new_boundary = 'boundary_conductance_12'
  []
  
  [conductance_area_23]	
    type = SideSetsBetweenSubdomainsGenerator
    input = conductance_area_12
    primary_block = sample_material_top
    paired_block = sample_material_bottom
    new_boundary = 'boundary_conductance_23'
  []
    
  [bottom_area]
    type = ParsedGenerateSideset
	input = conductance_area_23
	combinatorial_geometry = '((z > ${mesh_bottom}-1e-8) & (z < ${mesh_bottom}+1e-8))'
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
  [temp_samp_real_top]
    order = FIRST
    family = LAGRANGE
	block = sample_material_top
  []
  [temp_samp_imag_top]
    order = FIRST
    family = LAGRANGE
	block = sample_material_top
  []
  [temp_samp_real_bottom]
    order = FIRST
    family = LAGRANGE
	block = sample_material_bottom
  []
  [temp_samp_imag_bottom]
    order = FIRST
    family = LAGRANGE
	block = sample_material_bottom
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
  
  
  [heat_conduction_sample_real_top]
    type = HeatConductionSteadyRealAnisotropic
	
    variable = temp_samp_real_top
	imaginary_temp = temp_samp_imag_top
	
	thermal_conductivity = k_samp_2
	heat_capacity = c_samp_2
	omega = omega
	density = rho_samp_2
	
	block = sample_material_top
  []
  [heat_conduction_sample_imag_top]
    type = HeatConductionSteadyImagAnisotropic
	
    variable = temp_samp_imag_top
	real_temp = temp_samp_real_top
	
	thermal_conductivity = k_samp_2
	heat_capacity = c_samp_2
	omega = omega
	density = rho_samp_2
	
	block = sample_material_top
  []
  
  
  [heat_conduction_sample_real_bottom]
    type = HeatConductionSteadyRealAnisotropic
	
    variable = temp_samp_real_bottom
	imaginary_temp = temp_samp_imag_bottom
	
	thermal_conductivity = k_samp_3
	heat_capacity = c_samp_3
	omega = omega
	density = rho_samp_3
	
	block = sample_material_bottom
  []
  [heat_conduction_sample_imag_bottom]
    type = HeatConductionSteadyImagAnisotropic
	
    variable = temp_samp_imag_bottom
	real_temp = temp_samp_real_bottom
	
	thermal_conductivity = k_samp_3
	heat_capacity = c_samp_3
	omega = omega
	density = rho_samp_3
	
	block = sample_material_bottom
  []
[]

[InterfaceKernels]
  [interface_real_12]
    type = SideSetHeatTransferKernel
    variable = temp_trans_real
    neighbor_var = temp_samp_real_top
    boundary = 'boundary_conductance_12'
	conductance = -${conductance_12}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [interface_imag_12]
    type = SideSetHeatTransferKernel
    variable = temp_trans_imag
    neighbor_var = temp_samp_imag_top
    boundary = 'boundary_conductance_12'
	conductance = ${conductance_12}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
    [interface_real_23]
    type = SideSetHeatTransferKernel
    variable = temp_samp_real_top
    neighbor_var = temp_samp_real_bottom
    boundary = 'boundary_conductance_23'
	conductance = -${conductance_23}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [interface_imag_23]
    type = SideSetHeatTransferKernel
    variable = temp_samp_imag_top
    neighbor_var = temp_samp_imag_bottom
    boundary = 'boundary_conductance_23'
	conductance = ${conductance_23}
	
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
	constant_names = 'Rprobe pi'
	constant_expressions = '${probe_radius} 3.14159265359'
	use_xyzt = true
	expression = '((temp_trans_real)/(pi*(Rprobe^2)))*exp((-(x^2))/(Rprobe^2))'
	block = transducer_material
  []
  [average_surface_temperature_imag]
    type = ParsedAux
    variable = avg_surf_temp_imag
    coupled_variables = 'temp_trans_imag'
	constant_names = 'Rprobe pi'
	constant_expressions = '${probe_radius} 3.14159265359'
	use_xyzt = true
	expression = '((temp_trans_imag)/(pi*(Rprobe^2)))*exp((-(x^2))/(Rprobe^2))'
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
    expression = '-((Q0*absorbance)/(pi*(Rpump^2)))*exp(-(x^2)/(Rpump^2))'
    symbol_names = 'Rpump Q0 absorbance'
    symbol_values = '${pump_radius} ${pump_power} ${pump_absorbance}'
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
    prop_names = 'rho_trans c_trans'
    prop_values = '${rho_trans} ${c_trans}'
	block = transducer_material
  []
  [transducer_kappa]
    type = ADGenericConstantRankTwoTensor
    tensor_name = k_trans
    # tensor values are column major-ordered
    tensor_values = '${k_trans_r} 0 0 0 ${k_trans_r} 0 0 0 ${k_trans_z}'
	block = transducer_material
  []
  
  
  [basic_sample_materials_2]
    type = ADGenericConstantMaterial
    prop_names = 'rho_samp_2 c_samp_2'
    prop_values = '${rho_samp_2} ${c_samp_2}'
	block = 'sample_material_top'
  []
  [sample_kappa_2]
    type = ADGenericConstantRankTwoTensor
    tensor_name = k_samp_2
    # tensor values are column major-ordered
    tensor_values = '${k_samp_r_2} 0 0 0 ${k_samp_r_2} 0 0 0 ${k_samp_z_2}'
	block = 'sample_material_top sample_material_bottom'
  []
  
  
  [basic_sample_materials_3]
    type = ADGenericConstantMaterial
    prop_names = 'rho_samp_3 c_samp_3'
    prop_values = '${rho_samp_3} ${c_samp_3}'
	block = 'sample_material_top sample_material_bottom'
  []
  [sample_kappa_3]
    type = ADGenericConstantRankTwoTensor
    tensor_name = k_samp_3
    # tensor values are column major-ordered
    tensor_values = '${k_samp_r_3} 0 0 0 ${k_samp_r_3} 0 0 0 ${k_samp_z_3}'
	block = 'sample_material_bottom'
  []
  
  
  
  [simulation_frequency]
    type = ADGenericFunctionMaterial
	prop_names = omega
    prop_values = angular_frequency
	block = 'transducer_material sample_material_top sample_material_bottom'
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
    variable = temp_samp_real_bottom
    boundary = 'bottom_surface'
    value = 0
  []
  [ambient_temperature_imag]
    type = DirichletBC
    variable = temp_samp_imag_bottom
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
  exodus = true
  [pgraph]
    type = PerfGraphOutput
    execute_on = 'final'  # Default is "final"
    level = 1             # Default is 1
  []
[]

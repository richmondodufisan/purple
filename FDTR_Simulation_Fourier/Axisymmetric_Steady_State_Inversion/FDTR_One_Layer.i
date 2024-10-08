#Global Parameters
x0_val = 0
y0_val = 0
freq_val = 1e6

transducer_thickness = 0.09
probe_radius = 1.34
pump_radius = 1.53
pump_power = 0.01
pump_absorbance = 1

kappa_bulk_au = 215e-6
rho_au = 19.3e-15
c_au = 0.1287e3

[Problem]
  coord_type = RZ
[]

[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = FDTR_mesh.msh
  []
  [applied_pump_area]
    type = ParsedGenerateSideset
	input = sample_mesh
	combinatorial_geometry = '(z > ${transducer_thickness}-1e-8) & (z < ${transducer_thickness}+1e-8)'
	new_sideset_name = top_pump_area
  []
  [bottom_area]
    type = ParsedGenerateSideset
	input = applied_pump_area
	combinatorial_geometry = '((z > -40-1e-8) & (z < -40+1e-8))'
	new_sideset_name = bottom_surface
  []
[]

[Variables]
  [temp_real]
    order = FIRST
    family = LAGRANGE
  []
  [temp_imag]
    order = FIRST
    family = LAGRANGE
  []
[]

[Kernels]
  [heat_conduction_real]
    type = HeatConductionSteadyReal
	
    variable = temp_real
	imaginary_temp = temp_imag
	
	thermal_conductivity = k_trans
	heat_capacity = c_trans
	omega = omega
	density = rho_trans 
  []
  [heat_conduction_imag]
    type = HeatConductionSteadyImag
	
    variable = temp_imag
	real_temp = temp_real
	
	thermal_conductivity = k_trans
	heat_capacity = c_trans
	omega = omega
	density = rho_trans 
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
    coupled_variables = 'temp_real'
	constant_names = 'x0 y0 Rprobe pi'
	constant_expressions = '${x0_val} ${y0_val} ${probe_radius} 3.14159265359'
	use_xyzt = true
	expression = '((temp_real)/(pi*(Rprobe^2)))*exp((-((x-x0)^2+(y-y0)^2))/(Rprobe^2))'
  []
  [average_surface_temperature_imag]
    type = ParsedAux
    variable = avg_surf_temp_imag
    coupled_variables = 'temp_imag'
	constant_names = 'x0 y0 Rprobe pi'
	constant_expressions = '${x0_val} ${y0_val} ${probe_radius} 3.14159265359'
	use_xyzt = true
	expression = '((temp_imag)/(pi*(Rprobe^2)))*exp((-((x-x0)^2+(y-y0)^2))/(Rprobe^2))'
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
    prop_names = 'rho_trans c_trans k_trans'
    prop_values = '${rho_au} ${c_au} ${kappa_bulk_au}'
  []
  [simulation_frequency]
    type = ADGenericFunctionMaterial
	prop_names = omega
    prop_values = angular_frequency
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
    variable = temp_real
    boundary = 'bottom_surface'
    value = 0
  []
  [ambient_temperature_imag]
    type = DirichletBC
    variable = temp_imag
    boundary = 'bottom_surface'
    value = 0
  [] 
  [heat_source_term_real]
    type = FunctionNeumannBC
	variable = temp_real
	boundary = 'top_pump_area'
	function = heat_source_function
  []
  [heat_source_term_imag]
    type = NeumannBC
	variable = temp_imag
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

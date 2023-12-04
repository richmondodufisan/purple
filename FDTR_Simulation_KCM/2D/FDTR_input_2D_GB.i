#Global Parameters
x0_val = -15

freq_val = 1e6
dphase = 0.2
tp = 1
transducer_thickness = 0.09
probe_radius = 1.34
pump_radius = 1.53
pump_power = 0.01
pump_absorbance = 1
room_temperature = 293.15

rho_c_transducer = 2.48391e-12
k_transducer = 215e-6

rho_c_sample = 1.6049139e-12
tau_sample = 42e-12
nonlocal_length = 0.185
alpha_sample = 2

gb_width_val = 0.1
kappa_bulk_sample = 130e-6
kappa_gb_sample = 56.52e-6

interface_conductance_val = 3e-5

theta_deg = 0
theta_rad = ${fparse (theta_deg/180)*pi}

period = ${fparse 1/freq_val}
dt_val = ${fparse 5.0*(dphase/360.0)*period*tp}
dt_val_min = ${fparse 0.5*(dphase/360.0)*period*tp}

start_period = 0.0
start_val = ${fparse 2.2*period*tp*(start_period/2.0)}

end_period = 10.0
t_val = ${fparse 2.2*period*tp*(end_period/2.0)}

[Mesh]
  second_order = true

  [sample_mesh]
    type = FileMeshGenerator
    file = FDTR_mesh_x0_-15_theta_0.msh
  []
  [sample_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_mesh
    block_id = 1
    top_right = '40 0 0'
    bottom_left = '-40 -40 0'
  []
  [transducer_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block
    block_id = 2	
    top_right = '40 ${transducer_thickness} 0'
    bottom_left = '-40 0 0'
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
	combinatorial_geometry = '(y > ${transducer_thickness}-1e-8) & (y < ${transducer_thickness}+1e-8) & (((x-x0)^2) < 64)'
	constant_names = 'x0'
	constant_expressions = '${x0_val}'
	new_sideset_name = top_pump_area
  []
  
  [applied_pump_sample]
    type = ParsedGenerateSideset
	input = applied_pump_area
	combinatorial_geometry = '(y > 0.0-1e-8) & (y < 0.0+1e-8) & (((x-x0)^2) < 64)'
	constant_names = 'x0'
	constant_expressions = '${x0_val}'
	new_sideset_name = sample_pump_area
  []
  
  [top_no_pump]
    type = ParsedGenerateSideset
	input = applied_pump_sample
	combinatorial_geometry = '(y > ${transducer_thickness}-1e-8) & (y < ${transducer_thickness}+1e-8) & (((x-x0)^2) >= 64)'
	constant_names = 'x0'
	constant_expressions = '${x0_val}'
	new_sideset_name = top_no_pump_area
  []
  
  [conductance_area]	
    type = SideSetsBetweenSubdomainsGenerator
    input = top_no_pump
    primary_block = transducer_material
    paired_block = sample_material
    new_boundary = 'boundary_conductance'
  []
    
  [bottom_area]
    type = ParsedGenerateSideset
	input = conductance_area
	combinatorial_geometry = '((y > -40-1e-8) & (y < -40+1e-8))'
	new_sideset_name = bottom_surface
  []
  
  [side_areas]
    type = ParsedGenerateSideset
	input = bottom_area
	combinatorial_geometry = '((x > -40-1e-8) & (x < -40+1e-8)) | ((x > 40-1e-8) & (x < 40+1e-8))'
	new_sideset_name = side_surfaces
  []
[]

[Variables]
  [q_samp_x]
    order = SECOND
    family = LAGRANGE
	block = sample_material
  []
  
  [q_samp_y]
    order = SECOND
    family = LAGRANGE
	block = sample_material
  []
  
  [q_samp_z]
    order = SECOND
    family = LAGRANGE
	block = sample_material
  []
  
  [q_trans_x]
    order = SECOND
    family = LAGRANGE
	block = transducer_material
  []
  
  [q_trans_y]
    order = SECOND
    family = LAGRANGE
	block = transducer_material
  []
  
  [q_trans_z]
    order = SECOND
    family = LAGRANGE
	block = transducer_material
  []
  
  [temp_samp]
    order = FIRST
    family = LAGRANGE
	block = sample_material
  []
  
  [temp_trans]
    order = FIRST
    family = LAGRANGE
	block = transducer_material
  []
[]


[Kernels]
  [heat_x_trans]
    type = FourierHeatEquation
    variable = q_trans_x
	temperature = temp_trans
	component_flux = 0
	thermal_conductivity = k_trans
	block = transducer_material
  []
  [heat_y_trans]
    type = FourierHeatEquation
    variable = q_trans_y
	temperature = temp_trans
	component_flux = 1
	thermal_conductivity = k_trans
	block = transducer_material
  []
  [heat_z_trans]
    type = FourierHeatEquation
    variable = q_trans_z
	temperature = temp_trans
	component_flux = 2
	thermal_conductivity = k_trans
	block = transducer_material
  []


  [diffuse_trans]
    type = DiffusionTemperature
    variable = temp_trans
	
	q_x = q_trans_x
	q_y = q_trans_y
	q_z = q_trans_z
	
	block = transducer_material
  []
  
  
  [diffuse_trans_time]
    type = DiffusionTemperatureTimeDerivative
    variable = temp_trans
	rho_c = rho_c_trans
	block = transducer_material
  []
  
  
  [heat_x_samp]
    type = KCMHeatEquation
    variable = q_samp_x
	temperature = temp_samp
	component_flux = 0
	
	thermal_conductivity = k_samp
	length_scale = l_nonlocal
	alpha = alpha
		
	q_x = q_samp_x
	q_y = q_samp_y
	q_z = q_samp_z
	
	block = sample_material
  []
  [heat_y_samp]
    type = KCMHeatEquation
    variable = q_samp_y
	temperature = temp_samp
	component_flux = 1
	
	thermal_conductivity = k_samp
	length_scale = l_nonlocal
	alpha = alpha
		
	q_x = q_samp_x
	q_y = q_samp_y
	q_z = q_samp_z
	
	block = sample_material
  []
  [heat_z_samp]
    type = KCMHeatEquation
    variable = q_samp_z
	temperature = temp_samp
	component_flux = 2
	
	thermal_conductivity = k_samp
	length_scale = l_nonlocal
	alpha = alpha
		
	q_x = q_samp_x
	q_y = q_samp_y
	q_z = q_samp_z
	
	block = sample_material
  []
  
  
  
  [diffuse_samp]
    type = DiffusionTemperature
    variable = temp_samp
	
	q_x = q_samp_x
	q_y = q_samp_y
	q_z = q_samp_z
	
	block = sample_material
  []
  
  
  
  [diffuse_samp_time]
    type = DiffusionTemperatureTimeDerivative
    variable = temp_samp
	rho_c = rho_c_samp
	block = sample_material
  []
[]

[InterfaceKernels]
  [gap_01]
    type = SideSetHeatTransferKernel
    variable = temp_trans
    neighbor_var = temp_samp
    boundary = 'boundary_conductance'
	conductance = ${interface_conductance_val}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
[]

[AuxVariables]
  [avg_surf_temp]
  []
  [sample_avg_surf_temp]
  []
  [bulk_gb_dist]
    order = FIRST
    family = MONOMIAL
  []
[]

[AuxKernels]
  [average_surface_temperature]
    type = ParsedAux
    variable = avg_surf_temp
    coupled_variables = 'temp_trans'
	constant_names = 'x0 Rprobe T0 pi'
	constant_expressions = '${x0_val} ${probe_radius} ${room_temperature} 3.14159265359'
	use_xyzt = true
	expression = '((temp_trans-T0)/(pi*(Rprobe^2)))*exp((-((x-x0)^2))/(Rprobe^2))'
	block = transducer_material
  []
  [sample_average_surface_temperature]
    type = ParsedAux
    variable = sample_avg_surf_temp
    coupled_variables = 'temp_samp'
	constant_names = 'x0 Rprobe T0 pi'
	constant_expressions = '${x0_val} ${probe_radius} ${room_temperature} 3.14159265359'
	use_xyzt = true
	expression = '((temp_samp-T0)/(pi*(Rprobe^2)))*exp((-((x-x0)^2))/(Rprobe^2))'
	block = sample_material
  []
  [visualize_gb]
    type = ADMaterialRealAux
	variable = bulk_gb_dist
	property = k_samp
	block = sample_material
  []
[]

[Postprocessors]
  [integral_trans]
    type = SideIntegralVariablePostprocessor
    boundary = 'top_pump_area'
    variable = avg_surf_temp
  []
  [integral_samp]
    type = SideIntegralVariablePostprocessor
    boundary = 'sample_pump_area'
    variable = sample_avg_surf_temp
  []
[]


[Functions]
  [heat_source_function]
    type = ADParsedFunction
    expression = '((((Q0 * absorbance) / (pi * (Rpump ^ 2))) * exp(-(((x - x0) ^ 2) / (Rpump ^ 2))) * 0.5 * (1 - cos((2 * pi * freq * t)))))'
    symbol_names = 'x0 Rpump Q0 absorbance freq'
    symbol_values = '${x0_val} ${pump_radius} ${pump_power} ${pump_absorbance} ${freq_val}'
  []
  [grain_boundary_function]
    type = ADParsedFunction
	expression = 'if ( (x<((-gb_width/(2*cos(theta)))+(abs(y)*tan(theta)))) | (x>((gb_width/(2*cos(theta)))+(abs(y)*tan(theta)))), k_bulk, k_gb)'
	symbol_names = 'gb_width theta k_bulk k_gb'
	symbol_values = '${gb_width_val} ${theta_rad} ${kappa_bulk_sample} ${kappa_gb_sample}'
  []
[]


[Materials]
  [basic_transducer_materials]
    type = ADGenericConstantMaterial
    block = transducer_material
    prop_names = 'rho_c_trans k_trans'
    prop_values = '${rho_c_transducer} ${k_transducer}'
  []
  [basic_sample_materials]
    type = ADGenericConstantMaterial
    block = sample_material
    prop_names = 'rho_c_samp tau l_nonlocal alpha'
    prop_values = '${rho_c_sample} ${tau_sample} ${nonlocal_length} ${alpha_sample}'
  []
  [thermal_conductivity_sample]
    type = ADGenericFunctionMaterial
    prop_names = k_samp
    prop_values = grain_boundary_function
	block = sample_material
  []
  [heat_source_material]
    type = ADGenericFunctionMaterial
    prop_names = heat_source_mat
    prop_values = heat_source_function
  []
[]

[BCs]
  [ambient_temperature]
    type = DirichletBC
    variable = temp_samp
    boundary = 'bottom_surface'
    value = ${room_temperature}
  []
  [heat_source_term]
    type = FunctionNeumannBC
	variable = temp_trans
	boundary = 'top_pump_area'
	function = heat_source_function
  []
[]

[ICs]
  [initial_temperature_sample]
    type = ConstantIC
	variable = temp_samp
	value = ${room_temperature}
	block = sample_material
  []
  [initial_temperature_doping]
    type = ConstantIC
	variable = temp_trans
	value = ${room_temperature}
	block = transducer_material
  []
[]

[Preconditioning]
  [preconditioner]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Transient
  solve_type = 'NEWTON'

  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
  scaling_group_variables = 'q_samp_x q_samp_y q_samp_z; q_trans_x q_trans_y q_trans_z'

  dtmin = ${dt_val_min}
  dtmax= ${dt_val}
  
  start_time = ${start_val}
  end_time = ${t_val}
   
  [TimeStepper]
    type = IterationAdaptiveDT
    optimal_iterations = 15
    iteration_window = 3
    linear_iteration_ratio = 100
    growth_factor=1.5
    cutback_factor=0.5
    dt = ${dt_val}
  []
  [Predictor]
    type = SimplePredictor
    scale = 1.0
    skip_after_failed_timestep = true
  []
[]

[Debug]
  show_var_residual_norms = true
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
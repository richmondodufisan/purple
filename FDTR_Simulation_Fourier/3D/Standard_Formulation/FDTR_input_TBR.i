#Global Parameters
x0_val = 0
y0_val = 0
freq_val = 1e6
dphase = 0.2
tp = 1
transducer_thickness = 0.09
probe_radius = 1.34
pump_radius = 1.53
pump_power = 0.01
pump_absorbance = 1
room_temperature = 293.15

kappa_bulk_si = 130e-6

rho_si = 2.329e-15
c_si = 0.6891e3

au_si_conductance = 3e-5
gb_conductance = 1e-3

kappa_bulk_au = 215e-6
rho_au = 19.3e-15
c_au = 0.1287e3




period = ${fparse 1/freq_val}
dt_val = ${fparse 5.0*(dphase/360.0)*period*tp}
dt_val_min = ${fparse 0.5*(dphase/360.0)*period*tp}

start_period = 0.0
start_val = ${fparse 2.2*period*tp*(start_period/2.0)}

end_period = 10.0
t_val = ${fparse 2.2*period*tp*(end_period/2.0)}

[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = FDTR_mesh.msh
  []
  
  [sample_block_left]
    type = SubdomainBoundingBoxGenerator
    input = sample_mesh
    block_id = 1
    top_right = '0 20 0'
    bottom_left = '-40 -20 -40'
  []
  
  [sample_block_right]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_left
    block_id = 2
    top_right = '40 20 0'
    bottom_left = '0 -20 -40'
  []
  
  [transducer_block]
    type = SubdomainBoundingBoxGenerator
    input = sample_block_right
    block_id = 3	
    top_right = '40 20 ${transducer_thickness}'
    bottom_left = '-40 -20 0'
  []
  
  [rename]
    type = RenameBlockGenerator
    old_block = '1 2 3'
    new_block = 'sample_material_left sample_material_right transducer_material'
    input = transducer_block
  []
  
  [applied_pump_area]
    type = ParsedGenerateSideset
	input = rename
	combinatorial_geometry = '(z > ${transducer_thickness}-1e-8) & (z < ${transducer_thickness}+1e-8) & (((x-x0)^2 + (y-y0)^2)< 64)'
	constant_names = 'x0 y0'
	constant_expressions = '${x0_val} ${y0_val}'
	new_sideset_name = top_pump_area
  []
  
  [applied_pump_sample]
    type = ParsedGenerateSideset
	input = applied_pump_area
	combinatorial_geometry = '(z > 0.0-1e-8) & (z < 0.0+1e-8) & (((x-x0)^2 + (y-y0)^2)< 64)'
	constant_names = 'x0 y0'
	constant_expressions = '${x0_val} ${y0_val}'
	new_sideset_name = sample_pump_area
  []
  
  [top_no_pump]
    type = ParsedGenerateSideset
	input = applied_pump_sample
	combinatorial_geometry = '(z > ${transducer_thickness}-1e-8) & (z < ${transducer_thickness}+1e-8) & (((x-x0)^2 + (y-y0)^2) >= 64)'
	constant_names = 'x0 y0'
	constant_expressions = '${x0_val} ${y0_val}'
	new_sideset_name = top_no_pump_area
  []
  
  [conductance_area_1]	
    type = SideSetsBetweenSubdomainsGenerator
    input = top_no_pump
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
  
  [conductance_area_3]	
    type = SideSetsBetweenSubdomainsGenerator
    input = conductance_area_2
    primary_block = sample_material_left
    paired_block = sample_material_right
    new_boundary = 'grain_boundary'
  []
    
  [bottom_area]
    type = ParsedGenerateSideset
	input = conductance_area_3
	combinatorial_geometry = '((z > -40-1e-8) & (z < -40+1e-8))'
	new_sideset_name = bottom_surface
  []
  
  [side_areas]
    type = ParsedGenerateSideset
	input = bottom_area
	combinatorial_geometry = '((x > -40-1e-8) & (x < -40+1e-8)) | ((x > 40-1e-8) & (x < 40+1e-8)) | ((y > -20-1e-8) & (y < -20+1e-8)) | ((y > 20-1e-8) & (y < 20+1e-8))'
	new_sideset_name = side_surfaces
  []
[]

[Variables]
  [temp_trans]
    order = FIRST
    family = LAGRANGE
	block = transducer_material
  []
  [temp_samp_left]
    order = FIRST
    family = LAGRANGE
	block = sample_material_left
  []
  [temp_samp_right]
    order = FIRST
    family = LAGRANGE
	block = sample_material_right
  []
[]

[Kernels]
  [heat_conduction_transducer]
    type = ADHeatConduction
    variable = temp_trans
	thermal_conductivity = k_trans
	block = transducer_material
  []
  [heat_conduction_sample_left]
    type = ADHeatConduction
    variable = temp_samp_left
	thermal_conductivity = k_samp
	block = sample_material_left
  []
  [heat_conduction_sample_right]
    type = ADHeatConduction
    variable = temp_samp_right
	thermal_conductivity = k_samp
	block = sample_material_right
  []
  [heat_conduction_time_dep_transducer]
    type = ADHeatConductionTimeDerivative
    variable = temp_trans
	density_name = rho_trans
	specific_heat = c_trans
	block = transducer_material
  []
  [heat_conduction_time_dep_sample_left]
    type = ADHeatConductionTimeDerivative
    variable = temp_samp_left
	density_name = rho_samp
	specific_heat = c_samp
	block = sample_material_left
  []
  [heat_conduction_time_dep_sample_right]
    type = ADHeatConductionTimeDerivative
    variable = temp_samp_right
	density_name = rho_samp
	specific_heat = c_samp
	block = sample_material_right
  []
[]

[InterfaceKernels]
  [sample_trans_left]
    type = SideSetHeatTransferKernel
    variable = temp_trans
    neighbor_var = temp_samp_left
    boundary = 'trans_left_sample_boundary'
	conductance = ${au_si_conductance}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [sample_trans_right]
    type = SideSetHeatTransferKernel
    variable = temp_trans
    neighbor_var = temp_samp_right
    boundary = 'trans_right_sample_boundary'
	conductance = ${au_si_conductance}
	
	Tbulk_mat = 0
	h_primary = 0
	h_neighbor = 0
	emissivity_eff_primary = 0
	emissivity_eff_neighbor = 0
  []
  
  [sample_sample_gb]
    type = SideSetHeatTransferKernel
    variable = temp_samp_left
    neighbor_var = temp_samp_right
    boundary = 'grain_boundary'
	conductance = ${gb_conductance}
	
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
[]

[AuxKernels]
  [average_surface_temperature]
    type = ParsedAux
    variable = avg_surf_temp
    coupled_variables = 'temp_trans'
	constant_names = 'x0 y0 Rprobe T0 pi'
	constant_expressions = '${x0_val} ${y0_val} ${probe_radius} ${room_temperature} 3.14159265359'
	use_xyzt = true
	expression = '((temp_trans-T0)/(pi*(Rprobe^2)))*exp((-((x-x0)^2+(y-y0)^2))/(Rprobe^2))'
	block = transducer_material
  []
[]

[Postprocessors]
  [integral_trans]
    type = SideIntegralVariablePostprocessor
    boundary = 'top_pump_area'
    variable = avg_surf_temp
  []
[]

[Functions]
  [heat_source_function]
    type = ADParsedFunction
    expression = '((((Q0*absorbance)/(pi*(Rpump^2)))*exp((-((x-x0)^2+(y-y0)^2))/(Rpump^2)))*0.5*(1-cos((2*pi*freq*t))))'
    symbol_names = 'x0 y0 Rpump Q0 absorbance freq'
    symbol_values = '${x0_val} ${y0_val} ${pump_radius} ${pump_power} ${pump_absorbance} ${freq_val}'
  []
[]

[Materials]
  [basic_transducer_materials]
    type = ADGenericConstantMaterial
    block = transducer_material
    prop_names = 'rho_trans c_trans k_trans'
    prop_values = '${rho_au} ${c_au} ${kappa_bulk_au}'
  []
  [basic_sample_materials_left]
    type = ADGenericConstantMaterial
    block = sample_material_left
    prop_names = 'rho_samp c_samp k_samp'
    prop_values = '${rho_si} ${c_si} ${kappa_bulk_si}'
  []
  [basic_sample_materials_right]
    type = ADGenericConstantMaterial
    block = sample_material_right
    prop_names = 'rho_samp c_samp k_samp'
    prop_values = '${rho_si} ${c_si} ${kappa_bulk_si}'
  []
  [heat_source_material]
    type = ADGenericFunctionMaterial
    prop_names = heat_source_mat
    prop_values = heat_source_function
  []
[]

[BCs]
  [heat_source_term]
    type = FunctionNeumannBC
	variable = temp_trans
	boundary = 'top_pump_area'
	function = heat_source_function
  []
[]

[ICs]
  [initial_temperature_sample_left]
    type = ConstantIC
	variable = temp_samp_left
	value = ${room_temperature}
	block = sample_material_left
  []
  [initial_temperature_sample_right]
    type = ConstantIC
	variable = temp_samp_right
	value = ${room_temperature}
	block = sample_material_right
  []
  [initial_temperature_doping]
    type = ConstantIC
	variable = temp_trans
	value = ${room_temperature}
	block = transducer_material
  []
[]

[Preconditioning]
  [smp]
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
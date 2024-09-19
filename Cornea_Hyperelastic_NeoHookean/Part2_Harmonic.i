#Global Parameters
freq_val = 10e3
omega = ${fparse 2 * pi * freq_val}


shear_modulus_val = 100000
poissons_ratio_val = 0.49


density = 1000
c_shear = ${fparse sqrt(shear_modulus_val/density)}


bulk_modulus = ${fparse ((2 * shear_modulus_val) * (1 + poissons_ratio_val))/(3 * (1 - (2 * poissons_ratio_val)))}
c_pressure = ${fparse sqrt((bulk_modulus + ((4.0/3.0)*shear_modulus_val))/density)}


mechanical_impedance = ${fparse density*((c_shear + c_pressure)/2.0)}


h_plate = 0.001
l_plate = ${fparse 30 * h_plate}
mid_height = ${fparse h_plate/2}
number_of_points = ${fparse l_plate/0.000025}

excitation_val = ${fparse (h_plate/10)}
dt_val = ${fparse excitation_val/100}

[GlobalParams]
  large_kinematics = true
[]

[Mesh]
  second_order = true
  [sample_mesh]
    type = FileMeshGenerator
    file = Part1_Stretch_out.e
	use_for_exodus_restart = true
  []
[]

[Variables]
  [disp_x_real]
    order = SECOND
    family = LAGRANGE
  []
  [disp_y_real]
    order = SECOND
  []
  [disp_x_imag]
    order = SECOND
    family = LAGRANGE
  []
  [disp_y_imag]
    order = SECOND
    family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_x_real]
    type = TotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x_real disp_y_real'
    variable = disp_x_real
	base_name = real
  []
  
  [div_sig_y_real]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_real disp_y_real'
    variable = disp_y_real
	base_name = real
  []
  
  [reaction_x_real]
    type = ADReaction
	variable = disp_x_real
	rate = ${fparse -omega*omega*density}
  []
  
  [reaction_y_real]
    type = ADReaction
	variable = disp_y_real
	rate = ${fparse -omega*omega*density}
  []
  
  
  
  
  [div_sig_x_imag]
    type = TotalLagrangianStressDivergence
	component = 0
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_x_imag
	base_name = imag
  []
  
  [div_sig_y_imag]
    type = TotalLagrangianStressDivergence
	component = 1
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_y_imag
	base_name = imag
  []
  
  [reaction_x_imag]
    type = ADReaction
	variable = disp_x_imag
	rate = ${fparse -omega*omega*density}
  []
  
  [reaction_y_imag]
    type = ADReaction
	variable = disp_y_imag
	rate = ${fparse -omega*omega*density}
  []
[]

[AuxVariables]
  [disp_x]
    initial_from_file_var = disp_x
    initial_from_file_timestep = LATEST
  []
  [disp_y]
    initial_from_file_var = disp_y
    initial_from_file_timestep = LATEST
  []
[]

[AuxKernels]
  [x_displacement]
    type = ParsedAux
    variable = disp_x
    coupled_variables = 'disp_x_real disp_x_imag'
	expression = 'sqrt(disp_x_real^2 + disp_x_imag^2)'
  []
  [y_displacement]
    type = ParsedAux
    variable = disp_y
    coupled_variables = 'disp_y_real disp_y_imag'
	expression = 'sqrt(disp_y_real^2 + disp_y_imag^2)'
  []
[]

[Postprocessors]
  [displace_y_real]
    type = PointValue
    variable = disp_y_real
    point = '0.002 0.001 0'
  []
  
  [displace_y_imag]
    type = PointValue
    variable = disp_y_imag
    point = '0.002 0.001 0'
  []
[]

[VectorPostprocessors]
  [wave_profile]
    type = LineValueSampler
    variable = disp_y
    start_point = '0.002 ${mid_height} 0'
    end_point = '${fparse l_plate - 0.002} ${mid_height} 0'
    num_points = ${number_of_points}
    sort_by = x
  []
[]

[Materials]
  [strain_energy_real]
    type = ComputeStrainEnergyNeoHookeanNearlyIncompressible
    mu_0 = ${shear_modulus_val}
	poissons_ratio = ${poissons_ratio_val}
	base_name = real
  []
  
  [strain_real]
    type = ComputeLagrangianStrain
	displacements = 'disp_x_real disp_y_real'
	base_name = real
  []
  
  [stress_real]
    type = ComputeStressNeoHookean
	base_name = real
  []
  
  
  [strain_energy_imag]
    type = ComputeStrainEnergyNeoHookeanNearlyIncompressible
    mu_0 = ${shear_modulus_val}
	poissons_ratio = ${poissons_ratio_val}
	base_name = imag
  []
  
  [strain_imag]
    type = ComputeLagrangianStrain
	displacements = 'disp_x_imag disp_y_imag'
	base_name = imag
  []
  
  [stress_imag]
    type = ComputeStressNeoHookean
	base_name = imag
  []
[]

[BCs]
  [harmonic_perturbation_real]
    type = FunctionDirichletBC
    variable = disp_y_real
    boundary = 'loading_point'
	function = 't'
	preset = false
  []
  
  [harmonic_perturbation_imag]
    type = DirichletBC
    variable = disp_y_imag
    boundary = 'loading_point'
    value = 0
	preset = false
  []
  
  [low_reflecting_boundary_x_real]
    type = CoupledVarNeumannBC
	variable = disp_x_real
	boundary = 'right'
	v = disp_x_imag
	coef = ${fparse omega*mechanical_impedance}
  []
  [low_reflecting_boundary_x_imag]
    type = CoupledVarNeumannBC
	variable = disp_x_imag
	boundary = 'right'
	v = disp_x_real
	coef = ${fparse -omega*mechanical_impedance}
  []
  
  [low_reflecting_boundary_y_real]
    type = CoupledVarNeumannBC
	variable = disp_y_real
	boundary = 'right'
	v = disp_y_imag
	coef = ${fparse omega*mechanical_impedance}
  []
  [low_reflecting_boundary_y_imag]
    type = CoupledVarNeumannBC
	variable = disp_y_imag
	boundary = 'right'
	v = disp_y_real
	coef = ${fparse -omega*mechanical_impedance}
  []
[]

[Executioner]
  type = Transient
  solve_type = 'NEWTON'
  line_search = 'none'
  
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'

  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
  
  start_time = 0.0
  end_time = ${excitation_val}
   
  [TimeStepper]
    type = IterationAdaptiveDT
    optimal_iterations = 15
    iteration_window = 3
    linear_iteration_ratio = 100
    growth_factor=1.5
    cutback_factor=0.5
    dt = ${dt_val}
  []
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

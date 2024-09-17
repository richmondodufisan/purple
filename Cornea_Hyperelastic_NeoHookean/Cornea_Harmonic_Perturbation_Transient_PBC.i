#Global Parameters
freq_val = 10e3
#omega = ${fparse -2 * pi * freq_val}
n_periods = 5
total_time = ${fparse (1/freq_val) * n_periods}
dt_val = ${fparse total_time/1000}

shear_modulus_val = 100000
poissons_ratio_val = 0.49
density = 1000

h_plate = 0.001
l_plate = ${fparse 0.2/(freq_val/1e3)}
mid_height = ${fparse h_plate/2}
number_of_points = ${fparse int(l_plate/0.00001)}

[GlobalParams]
  stabilize_strain = true
  large_kinematics = true
  displacements = 'disp_x disp_y'
[]

[Mesh]
  second_order = true
  [sample_mesh]
    type = FileMeshGenerator
    file = Cornea_Stretch_out.e
	use_for_exodus_restart = true
  []
[]

[Variables]
  [disp_x]
    order = SECOND
    family = LAGRANGE
	initial_from_file_var = disp_x
    initial_from_file_timestep = LATEST
  []
  [disp_y]
    order = SECOND
    family = LAGRANGE
	initial_from_file_var = disp_y
    initial_from_file_timestep = LATEST
  []
[]

[Kernels]
  [stress_x]
	type = DynamicStressDivergenceTensors
    variable = disp_x
    component = 0
	zeta = 0
  []
  [stress_y]
	type = DynamicStressDivergenceTensors
    variable = disp_y
    component = 1
	zeta = 0
  []
  [inertia_x]
    type = InertialForce
    variable = disp_x
	density = density
	eta = 0
  []
  [inertia_y]
    type = InertialForce
    variable = disp_y
	density = density
	eta = 0
  []
[]

[Postprocessors]
  [displace_y]
    type = PointValue
    variable = disp_y
    point = '${l_plate} 0.001 0'
  []
[]

[VectorPostprocessors]
  [wave_profile]
    type = LineValueSampler
    variable = disp_y
    start_point = '0 ${mid_height} 0'
    end_point = '${l_plate} ${mid_height} 0'
    num_points = ${number_of_points}
    sort_by = x
  []
[]

[Functions]
  [perturbation_function]
    type = ADParsedFunction
    expression = 'A * cos(2 * pi * freq * t)'
    symbol_names = 'A freq'
    symbol_values = '${fparse (h_plate/10)} ${freq_val}'
  []
[]


[Materials]
  [strain_energy_real]
    type = ComputeStrainEnergyNeoHookeanNearlyIncompressible
    mu_0 = ${shear_modulus_val}
	poissons_ratio = ${poissons_ratio_val}
  []
  
  [strain_real]
    type = ComputeLagrangianStrain
	displacements = 'disp_x disp_y'
  []
  
  [stress_real]
    type = ComputeStressNeoHookean
  []
  
  [density]
    type = GenericConstantMaterial
    prop_names = 'density'
    prop_values = '${density}'
  []
  
  [old_system_conversion]
    type = CauchyStressWrapper
  []
[]

[BCs]
  [harmonic_perturbation]
    type = ADFunctionDirichletBC
    variable = disp_y
    boundary = 'loading_point'
    function = perturbation_function
	preset = false
  []
  
  [Periodic]
    [periodic_boundary_y]
      variable = disp_y
      auto_direction = 'x'
    []
  []
[]



[Executioner]
  type = Transient
  solve_type = NEWTON
  
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'
  
  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  
  timestep_tolerance = 1e-6
  
  start_time = 0.0
  end_time = ${total_time}
  dt = ${dt_val}
  
  automatic_scaling = true
  line_search = none
  
  [TimeIntegrator]
    type = NewmarkBeta
    beta = 0.25
    gamma = 0.5
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

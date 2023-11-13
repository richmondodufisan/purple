[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = simple_box.msh
  []
[]

[Variables]
  [q_x]
    order = SECOND
    family = LAGRANGE
  []
  [q_y]
    order = SECOND
    family = LAGRANGE
  []
  [q_z]
    order = SECOND
    family = LAGRANGE
  []
  [temperature]
    order = FIRST
    family = LAGRANGE
  []
[]


[Kernels]
  [heat_x]
    type = FourierHeatEquation
    variable = q_x
	temperature = temperature
	component_flux = 0
	thermal_conductivity = k_val
  []
  [heat_y]
    type = FourierHeatEquation
    variable = q_y
	temperature = temperature
	component_flux = 1
	thermal_conductivity = k_val
  []
  [heat_z]
    type = FourierHeatEquation
    variable = q_z
	temperature = temperature
	component_flux = 2
	thermal_conductivity = k_val
  []
  [diffuse]
    type = DiffusionTemperature
    variable = temperature
	
	q_x = q_x
	q_y = q_y
	q_z = q_z
  []
[]

[Materials]
  [simulation_constants]
    type = ADGenericConstantMaterial
    prop_names = 'k_val'
    prop_values = '1.0'
  []
[]

[BCs]
  [left_val]
    type = DirichletBC
    variable = temperature
    boundary = 'right'
    value = 1
  []
  [right_val]
    type = DirichletBC
	variable = temperature
	boundary = 'left'
	value = 0
  []
[]

[Preconditioning]
  [smp]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Steady
  solve_type = 'PJFNK'

  petsc_options_iname = '-pc_type   -pc_hypre_type    -ksp_type     -ksp_gmres_restart  -pc_hypre_boomeramg_strong_threshold -pc_hypre_boomeramg_agg_nl -pc_hypre_boomeramg_agg_num_paths -pc_hypre_boomeramg_max_levels -pc_hypre_boomeramg_coarsen_type -pc_hypre_boomeramg_interp_type -pc_hypre_boomeramg_P_max -pc_hypre_boomeramg_truncfactor'
  petsc_options_value = 'hypre      boomeramg         gmres         301                  0.6                                  4                          5                                 25                             Falgout                          ext+i                           1                         0.3'

  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20

  line_search = 'none'

  automatic_scaling=true
  compute_scaling_once =true
  verbose=false

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
  exodus = true
  [pgraph]
    type = PerfGraphOutput
    execute_on = 'final'  # Default is "final"
    level = 1             # Default is 1
  []
[]
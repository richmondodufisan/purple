[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = simple_box.msh
  []
[]

[Variables]
  [temperature]
    order = FIRST
    family = LAGRANGE
  []
[]


[Kernels]
  [diffuse]
    type = ADHeatConduction
    variable = temperature
	thermal_conductivity = k_val
  []
[]

[Postprocessors]
  [central_temp]
    type = PointValue
    variable = temperature
    point = '5 5 2.5'
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
  
  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 300
  nl_max_its = 20

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
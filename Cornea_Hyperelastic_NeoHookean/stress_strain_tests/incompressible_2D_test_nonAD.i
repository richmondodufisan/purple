# Global Parameters
shear_modulus_val = 100000
l_bar = 0.1         # Domain length in x
h_bar = 0.1         # Domain length in y
right_disp_val = 0.002  # Applied displacement in x

[GlobalParams]
  large_kinematics = true
  use_displaced_mesh = true
[]

[Mesh]
  type = GeneratedMesh
  dim = 2
  nx = 10
  ny = 10
  xmin = 0.0
  xmax = ${l_bar}
  ymin = 0.0
  ymax = ${h_bar}
  second_order = true
[]

[Variables]
  [disp_x]
    family = LAGRANGE
    order = SECOND
  []
  [disp_y]
    family = LAGRANGE
    order = SECOND
  []
  [pressure]
    family = LAGRANGE
    order = FIRST
  []
[]

[Kernels]
  # Divergence of stress for the x-displacement equation
  [div_stress_x]
    type = TLStressDivergenceIncompressible
    component = 0
    displacements = 'disp_x disp_y'
    variable = disp_x
    pressure = pressure
  []
  # Divergence of stress for the y-displacement equation
  [div_stress_y]
    type = TLStressDivergenceIncompressible
    component = 1
    displacements = 'disp_x disp_y'
    variable = disp_y
    pressure = pressure
  []
  # Incompressibility kernel (pressure equation)
  [incompressibility]
    type = TLIncompressibilityPressure
    variable = pressure
    displacements = 'disp_x disp_y'
  []
[]

[Materials]
  [stress]
    type = ComputeStressIncompressibleNeoHookean
    mu = ${shear_modulus_val}
    pressure = pressure
  []
  [strain]
    type = ComputeLagrangianStrain
    displacements = 'disp_x disp_y'
  []
[]

[BCs]
  [left_fixed_x]
    type = ADDirichletBC
    variable = disp_x
    boundary = 'left'
    value = 0.0
  []
  [left_fixed_y]
    type = ADDirichletBC
    variable = disp_y
    boundary = 'left'
    value = 0.0
  []
  [right_disp_x]
    type = ADDirichletBC
    variable = disp_x
    boundary = 'right'
    value = ${right_disp_val}
  []
  [pressure_fix]
    type = ADDirichletBC
    variable = pressure
    boundary = 'right'
    value = 0.0
  []
[]

[Postprocessors]
  [pressure_integral]
    type = ElementIntegralVariablePostprocessor
    variable = pressure
    execute_on = 'initial timestep_begin linear'
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
  l_max_its = 20
  nl_max_its = 30
[]

[Outputs]
  csv = true
  exodus = true
  perf_graph = true
[]

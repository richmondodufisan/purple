# Global Parameters
shear_modulus_val = 100000
l_bar = 0.1  # Length of the 1D bar
right_disp_val = 0.002  # Applied displacement

[GlobalParams]
  large_kinematics = true
  use_displaced_mesh = true
[]

[Mesh]
  type = GeneratedMesh
  dim = 1
  nx = 10  # 10 elements in 1D
  xmin = 0.0
  xmax = ${l_bar}
  second_order = true
[]

[Variables]
  [disp_x]
    order = SECOND
    family = LAGRANGE
  []
  [pressure]
    order = FIRST
    family = LAGRANGE
  []
[]

[Kernels]
  [div_stress_x]
    type = ADStressDivergenceTensors
    component = 0
    displacements = 'disp_x'
    variable = disp_x
  []
  [incompressibility]
    type = ADIncompressibilityConstraint
    variable = pressure
  []
[]

[Materials]
  [stress]
    type = ADComputeStressIncompressibleNeoHookean
    mu = ${shear_modulus_val}
    pressure = pressure
  []
  [ad_convert]
    type = RankTwoTensorMaterialADConverter
	reg_props_in = 'deformation_gradient'
	ad_props_out = 'ad_deformation_gradient'
  []
  [wrapper]
    type = ADCauchyStressWrapper
  []
  [strain]
    type = ComputeLagrangianStrain
    displacements = 'disp_x'
  []
[]

[BCs]
  [left_fixed]
    type = ADDirichletBC
    variable = disp_x
    boundary = 'left'
    value = 0
  []
  [right_disp]
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

[Executioner]
  type = Steady
  solve_type = 'NEWTON'


  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'

  nl_rel_tol = 1e-8
  nl_abs_tol = 1e-8
  l_tol = 1e-5
  l_max_its = 3
  nl_max_its = 3
[]

[Outputs]
  csv = true
  exodus = true
  perf_graph = true
[]

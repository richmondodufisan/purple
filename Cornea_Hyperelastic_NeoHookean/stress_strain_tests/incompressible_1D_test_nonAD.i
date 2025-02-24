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
  #[lambda]
   # family = SCALAR
   # order = FIRST
 # []
[]

[Kernels]
  [div_stress_x]
    type = TLStressDivergenceIncompressible
    component = 0
    displacements = 'disp_x'
    variable = disp_x
	pressure = pressure
  []
  [incompressibility]
    type = TLIncompressibilityPressure
    variable = pressure
    displacements = 'disp_x'
  []
  #[sk_lm]
   # type = ScalarLagrangeMultiplier
   # variable = pressure
   # lambda = lambda
 # []
[]

#[ScalarKernels]
  #[constraint]
   # type = AverageValueConstraint
   # variable = lambda
   # pp_name = pressure_integral
   # value = 0.0
  #[]
#[]


[AuxVariables]
  [strain_xx]
    order = CONSTANT
    family = MONOMIAL
  []
  [strain_yy]
    order = CONSTANT
    family = MONOMIAL
  []

  [stress_xx]
    order = CONSTANT
    family = MONOMIAL
  []
  [stress_yy]
    order = CONSTANT
    family = MONOMIAL
  []
  
  [j]
    order = CONSTANT
    family = MONOMIAL
  []
[]

[AuxKernels]
  [jacobian]
    type = RankTwoScalarAux
    rank_two_tensor = deformation_gradient
    variable = j
	scalar_type = ThirdInvariant
  []
  [stress_xx]
    type = RankTwoAux
    rank_two_tensor = cauchy_stress
    variable = stress_xx
    index_i = 0
    index_j = 0
  []
  [stress_yy]
    type = RankTwoAux
    rank_two_tensor = cauchy_stress
    variable = stress_yy
    index_i = 1
    index_j = 1
  []

  [strain_xx]
    type = RankTwoAux
    rank_two_tensor = total_strain
    variable = strain_xx
    index_i = 0
    index_j = 0
  []
  [strain_yy]
    type = RankTwoAux
    rank_two_tensor = total_strain
    variable = strain_yy
    index_i = 1
    index_j = 1
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
#  [pressure_fix]
#    type = ADDirichletBC
#    variable = pressure
#    boundary = 'right'
#    value = 0.0
#  []
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

  nl_rel_tol = 1e-12
  nl_abs_tol = 1e-12
  l_tol = 1e-10
  l_max_its = 300
  nl_max_its = 20
[]

[Outputs]
  csv = true
  exodus = true
  perf_graph = true
[]

[Mesh]
  [beam_mesh]
    type = FileMeshGenerator
    file = three-point-bending-3D-3.inp
  []
[]

[GlobalParams]
  volumetric_locking_correction = false
  displacements = 'disp_x disp_y disp_z'
  order = FIRST
  family = LAGRANGE
[]

[Variables]
  [disp_x]
  []
  [disp_y]
  []
  [disp_z]
  []
[]

[Kernels]
  [div_sig_x]
    type = ConcreteGradientDamageMomentum
    variable = disp_x
    component_disp = 0
	save_in = force_x
  []
  [div_sig_y]
    type = ConcreteGradientDamageMomentum
    variable = disp_y
    component_disp = 1
	save_in = force_y
  []
  [div_sig_z]
    type = ConcreteGradientDamageMomentum
    variable = disp_z
    component_disp = 2
	save_in = force_z
  []
  [nonlocal_damage_kernel]
    type = ConcreteGradientEnhancement
    variable = nonlocal_equivalent_strain
  []
[]

[AuxVariables]
  [damage]
    order = CONSTANT
    family = MONOMIAL
  []
  [force_x]
  []
  [force_y]
  []
  [force_z]
  []
[]


[Postprocessors]
  [bot_react_z]
    type = NodalSum
    variable = force_z
    boundary = top-line
  []
  [displace_z]
    type = PointValue
    variable = disp_z
    point = '0 0 200'
  []
[]

[AuxKernels]
  [damage_kernel]
    type = ADMaterialRealAux
    property = damage
    variable = damage
    execute_on = timestep_end
  []
[]



[Materials]
  [elasticity_tensor]
    type = ADComputeIsotropicElasticityTensor
    youngs_modulus = 30000
    poissons_ratio = 0.2
  []
  
  [strain]
    type = ADComputeSmallStrain
  []
  
  [stress]
    type = ADComputeLinearElasticStress
  []
  
  [modified_von_mises]
    type = ConcreteGradientDamageMaterialLOCAL
    nu = 0.2
    kappa_0 = 1.21e-4
    alpha = 0.9999
    beta = 385
    k = 10
  []
[]

[BCs]
  [bottom_x]
    type = DirichletBC
    variable = disp_x
    boundary = 'bottom-left bottom-right'
    value = 0
  []
  [bottom_y]
    type = DirichletBC
    variable = disp_y
    boundary = 'bottom-left'
    value = 0
  []
  [bottom_z]
    type = DirichletBC
    variable = disp_z
    boundary = 'bottom-left bottom-right'
    value = 0
  []
  [load]
    type = FunctionDirichletBC
    variable = disp_z
    boundary = 'top-line'
    function = '-1 * t'
    preset = false
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

  dtmin = 1e-5
  dtmax= 2.5e-2
  
  start_time = 0.0
  end_time = 2.5

  num_steps = 1000
  [TimeStepper]
    type = IterationAdaptiveDT
    optimal_iterations = 15
    iteration_window = 3
    linear_iteration_ratio = 100
    growth_factor=1.5
    cutback_factor=0.5
    dt = 2.5e-2
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
  exodus = true
  [pgraph]
    type = PerfGraphOutput
    execute_on = 'final'  # Default is "final"
    level = 1             # Default is 1
  []
[]
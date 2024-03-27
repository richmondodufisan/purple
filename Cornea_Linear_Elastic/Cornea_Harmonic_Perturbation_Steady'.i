#Global Parameters
freq_val = 1e6
youngs_modulus_val = 60e3
poissons_ratio_val = 0.4999
shear_modulus_val = ${fparse (youngs_modulus_val/(2*(1+poissons_ratio_val)))}

stretch_ratio = 1.1
l_plate = 0.02
right_disp_val = ${fparse (stretch_ratio - 1)*l_plate}

[Mesh]
  [sample_mesh]
    type = FileMeshGenerator
    file = cornea_rectangle.msh
  []
[]

[Variables]
  [disp_x]
    order = FIRST
    family = LAGRANGE
  []
  [disp_y]
    order = FIRST
    family = LAGRANGE
  []
[]

[Kernels]
  [div_sig_x]
    type = ADStressDivergenceTensors
	component = 0
	displacements = 'disp_x disp_y'
    variable = disp_x
  []
  
  [div_sig_y]
    type = ADStressDivergenceTensors
	component = 1
	displacements = 'disp_x disp_y'
    variable = disp_y
  []
[]

[Postprocessors]
  [displace_x]
    type = PointValue
    variable = disp_y
    point = '0.002 0.001 0'
  []
[]

[Materials]
  [elasticity_tensor]
    type = ADComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
  []
  
  [strain]
    type = ADComputeFiniteStrain
	displacements = 'disp_x disp_y'
  []
  
  [stress]
    type = ADComputeFiniteStrainElasticStress
  []
[]

[BCs]
  [left_x]
    type = DirichletBC
    variable = disp_x
    boundary = 'left'
    value = 0
  []
  [right_x]
    type = DirichletBC
    variable = disp_x
    boundary = 'right'
    value = ${right_disp_val}
  []
  [bottom_y]
    type = DirichletBC
    variable = disp_y
    boundary = 'bottom'
    value = 0
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
  l_max_its = 300
  nl_max_its = 20
  
  automatic_scaling = true
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

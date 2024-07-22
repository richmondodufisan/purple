#Global Parameters
freq_val = 10e3
youngs_modulus_val = 60e3
poissons_ratio_val = 0.4999
shear_modulus_val = ${fparse (youngs_modulus_val/(2*(1+poissons_ratio_val)))}
density = 1000
shear_wave_speed = ${fparse sqrt(shear_modulus_val/density)}
mechanical_impedance = ${fparse density*(shear_wave_speed/2)}

h_plate = 0.001
l_plate = 0.02
mid_height = ${fparse h_plate/2}
number_of_points = ${fparse l_plate/0.000025}

[GlobalParams]
  volumetric_locking_correction = true
[]

[Mesh]
  second_order = true
  [sample_mesh]
    type = FileMeshGenerator
    file = Cornea_Stretch_out.e
  []
[]

[Variables]
  [disp_x_real]
    order = SECOND
    family = LAGRANGE
  []
  [disp_y_real]
    order = SECOND
    family = LAGRANGE
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
    type = ADStressDivergenceTensors
	component = 0
	displacements = 'disp_x_real disp_y_real'
    variable = disp_x_real
	base_name = real
  []
  
  [div_sig_y_real]
    type = ADStressDivergenceTensors
	component = 1
	displacements = 'disp_x_real disp_y_real'
    variable = disp_y_real
	base_name = real
  []
  
  [reaction_x_real]
    type = ADReaction
	variable = disp_x_real
	rate = ${fparse -freq_val*freq_val*density}
  []
  
  [reaction_y_real]
    type = ADReaction
	variable = disp_y_real
	rate = ${fparse -freq_val*freq_val*density}
  []
  
  
  
  
  [div_sig_x_imag]
    type = ADStressDivergenceTensors
	component = 0
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_x_imag
	base_name = imag
  []
  
  [div_sig_y_imag]
    type = ADStressDivergenceTensors
	component = 1
	displacements = 'disp_x_imag disp_y_imag'
    variable = disp_y_imag
	base_name = imag
  []
  
  [reaction_x_imag]
    type = ADReaction
	variable = disp_x_imag
	rate = ${fparse -freq_val*freq_val*density}
  []
  
  [reaction_y_imag]
    type = ADReaction
	variable = disp_y_imag
	rate = ${fparse -freq_val*freq_val*density}
  []
[]

[AuxVariables]
  [disp_x]
  []
  [disp_y]
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
    start_point = '0 ${mid_height} 0'
    end_point = '${l_plate} ${mid_height} 0'
    num_points = ${number_of_points}
    sort_by = x
  []
[]

[Materials]
  [elasticity_tensor_real]
    type = ADComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
	base_name = real
  []
  
  [strain_real]
    type = ADComputeIncrementalSmallStrain
	displacements = 'disp_x_real disp_y_real'
	base_name = real
  []
  
  [stress_real]
    type = ADComputeFiniteStrainElasticStress
	base_name = real
  []
  
  
  [elasticity_tensor_imag]
    type = ADComputeIsotropicElasticityTensor
    youngs_modulus = ${youngs_modulus_val}
    poissons_ratio = ${poissons_ratio_val}
	base_name = imag
  []
  
  [strain_imag]
    type = ADComputeFiniteStrain
	displacements = 'disp_x_imag disp_y_imag'
	base_name = imag
  []
  
  [stress_imag]
    type = ADComputeFiniteStrainElasticStress
	base_name = imag
  []
[]

[BCs]
  [harmonic_perturbation_real]
    type = DirichletBC
    variable = disp_y_real
    boundary = 'loading_point'
    value = ${fparse (h_plate/10)}
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
	coef = ${fparse freq_val*mechanical_impedance}
  []
  [low_reflecting_boundary_x_imag]
    type = CoupledVarNeumannBC
	variable = disp_x_imag
	boundary = 'right'
	v = disp_x_real
	coef = ${fparse -freq_val*mechanical_impedance}
  []
  
  [low_reflecting_boundary_y_real]
    type = CoupledVarNeumannBC
	variable = disp_y_real
	boundary = 'right'
	v = disp_y_imag
	coef = ${fparse freq_val*mechanical_impedance}
  []
  [low_reflecting_boundary_y_imag]
    type = CoupledVarNeumannBC
	variable = disp_y_imag
	boundary = 'right'
	v = disp_y_real
	coef = ${fparse -freq_val*mechanical_impedance}
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
  line_search = none
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

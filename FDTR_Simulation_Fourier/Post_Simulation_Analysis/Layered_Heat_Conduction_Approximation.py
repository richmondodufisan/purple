import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.integrate import quad_vec
import math
import cmath
import pdb

# This is a helper file for calculating phase and temperature increase in FDTR experiments
# It is assumed that thermal transport is within the diffusive regime, hence Fourier's equation applies
# This is the analytical solution for radial heat transfer as detailed in the thesis of AJ Schmidt (2008)
# The calc_thermal_response should be used to find the phase and amplitude given the appropriate material properties



# To use in another file, include the line: 
# "from Layered_Heat_Conduction import calc_thermal_response"



# Input arguments for calc_thermal_response:

# N_layers: The number of layers. Must be an unsigned (positive) integer value

# layer_props: This should be a NumPy array of arrays. The arrays should be organized in descending order,
# i.e, from the bottom to the top (e.g [layer3, layer2, layer1]). Each layer array should contain the following material
# properties: [h (layer thickness), k_z (cross plane thermal conductivity), k_r (in plane/radial thermal conductivity),
# rho (density), c (heat capacity)]

# interface_props: this is an array of the interface conductances between layers. There should be one less
# conductance than the number of layers (e.g 1 interface conductance for a 2-layer system)

# r_pump: radius of the pump laser

# r_probe: radius of the probe laser

# calib_constants: additional constants to calibrate model if comparing to FEM simulations. 
# The calibration is done on the pump and probe radii.
# If using experimental data, set each value to 1 (i.e calib_constants = [1, 1])

# freq: frequency of the input signal (pump laser)

# pump_power: the pump power, Q0



# Integral in Equation 3.5
def integrand(x, N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq):

  # Checks to ensure data is properly submitted/formatted
  
  if (len(layer_props) != N_layers):
    raise RuntimeError("Size of layer properties and number of layers do not match")
    
  if (len(interface_props) != (N_layers - 1)):
    raise RuntimeError("Incorrect number of interface properties")

  ConductionMatrix = np.array([[1, 0], [0, 1]])
  
  for i in range(N_layers):
  
    h = layer_props[i][0]
    k_z = layer_props[i][1]
    k_r = layer_props[i][2]
    rho = layer_props[i][3]
    c = layer_props[i][4]
    
    # Equation 3.44  
    gamma = cmath.sqrt((k_r * (x**2) + rho * c * 1j * 2 * np.pi * freq)/k_z)
    
    # Equation 3.34  
    A = 1.0
    B = (-1.0/(k_z * gamma)) * np.tanh(gamma * h)
    C = -k_z * gamma * np.tanh(gamma * h)
    D = 1.0
    
    HeatLayer = np.array([[A, B], [C, D]])

    ConductionMatrix = ConductionMatrix @ HeatLayer
    
    if (i < (N_layers - 1)):
    
      # Equation 3.38
      G = interface_props[i]
      InterfaceLayer = np.array([[1, -(1.0/G)], [0, 1]])
      
      ConductionMatrix = ConductionMatrix @ InterfaceLayer
    
    
  C_total = ConductionMatrix[1][0]
  D_total = ConductionMatrix[1][1]

  # calibration constants to account for mesh sensitivity
  # 1 W/m.K corresponds to ~0.0005 radians change in phase
  # therefore, we need to have accuracy to at least 4.d.p
  # more would be even better

  beta1 = calib_consts[0]
  r_pump = r_pump*beta1

  beta2 = calib_consts[1]
  r_pump = r_pump*beta2
  
  # Integral part of Equation 3.5
  return x * (-D_total/C_total) * np.exp((2 * (-x**2) * (r_pump**2 + r_probe**2))/8.0)
  
  

def calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power):
  result, error = quad_vec(integrand, 0, 3000001, args=(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq))

  # Hankel space variable, Equation 3.5
  H = (pump_power/(2 * np.pi)) * result

  phase = math.atan(H.imag/H.real)
  amplitude = cmath.sqrt(H.real**2 + H.imag**2).real

  return phase, amplitude
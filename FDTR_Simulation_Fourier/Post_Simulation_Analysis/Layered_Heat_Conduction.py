import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.integrate import quad_vec
import math
import cmath
import pdb

# This is the integrand in eq 3.5 of the thesis of AJ Schmidt (2008)
# for calculating the analytical fourier response in the Hankel Space

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
    
    gamma = cmath.sqrt((k_r * (x**2) + rho * c * 1j * 2 * np.pi * freq)/k_z)
    
    A = np.cosh(gamma * h)
    B = (-1.0/(k_z * gamma)) * np.sinh(gamma * h)
    C = -k_z * gamma * np.sinh(gamma * h)
    D = np.cosh(gamma * h)
    
    HeatLayer = np.array([[A, B], [C, D]])

    ConductionMatrix = ConductionMatrix @ HeatLayer
    
    if (i < (N_layers - 1)):
    
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

  return x * (-D_total/C_total) * np.exp((2 * (-x**2) * (r_pump**2 + r_probe**2))/8.0)
  
  

def calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power):
  result, error = quad_vec(integrand, 0, 5000001, args=(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq))

  H = (pump_power/(2 * np.pi)) * result

  phase = math.atan(H.imag/H.real)
  amplitude = cmath.sqrt(H.real**2 + H.imag**2).real

  return phase, amplitude
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.integrate import quad_vec
import math
import cmath
import pdb
from scipy.integrate import dblquad
from scipy.special import i0,j0 

# This is a helper file for calculating phase and temperature increase in FDTR experiments
# It is assumed that thermal transport is within the diffusive regime, hence Fourier's equation applies
# This is the analytical solution for radial heat transfer as detailed in the thesis of AJ Schmidt (2008)
# The calc_thermal_response should be used to find the phase and amplitude given the appropriate material properties


# To use in another file, include the line: 
# "from Layered_Heat_Conduction_Beam_Offset import calc_thermal_response"


# Input arguments for calc_thermal_response:

# N_layers: The number of layers. Must be an unsigned (positive) integer value

# layer_props: This should be a NumPy array of arrays. The arrays should be organized in descending order,
# i.e, from the bottom to the top (e.g [layer3, layer2, layer1]). Each layer array should contain the following material
# properties: [h (layer thickness), kappa_z (cross plane thermal conductivity), kappa_r (in plane/radial thermal conductivity),
# rho (density), c (heat capacity)]

# interface_props: this is an array of the interface conductances between layers. There should be one less
# conductance than the number of layers (e.g 1 interface conductance for a 2-layer system)

# r_pump: radius of the pump laser

# r_probe: radius of the probe laser

# x0 (UNIQUE TO BEAM OFFSET): This is a modification of the model to account for beam offsets as detailed in Feser 2012
# It was found that numerical integration of the approximation (ring profile) was faster than the analytical solution
# Furthermore, the Hankel transform is defined differently in Feser 2012 (i.e * J(2*pi*k*r)) as opposed to (* J(k*r))
# in Schmidt 2008

# calib_constants: additional constants to calibrate model if comparing to FEM simulations. 
# The calibration is done on the pump and probe radii.
# If using experimental data, set each value to 1 (i.e calib_constants = [1, 1])

# freq: frequency of the input signal (pump laser)

# pump_power: the pump power, Q0


# Define the integrand with respect to r (i.e S(k) = Hankel Transform of S(r))
# Slightly adjusted version of equation 12 in Feser 2012 to provide
# a normalized ring-shaped profile, to keep consistent with 
# Schmidt 2008
def integrand_r(r, x0, r_probe, k):
    exponent_term = np.exp(-2 * (r**2 + x0**2) / r_probe**2)
    bessel_i_term = i0(4 * x0 * r / r_probe**2)
    bessel_j_term = j0(k * r)
    return (4 / r_probe**2) * exponent_term * bessel_i_term * bessel_j_term * r


# Integral in Equation 3.5
def integrand_k(k, N_layers, layer_props, interface_props, r_pump, r_probe, x0, calib_consts, freq):

  # Checks to ensure data is properly submitted/formatted
  
  if (len(layer_props) != N_layers):
    raise RuntimeError("Size of layer properties and number of layers do not match")
    
  if (len(interface_props) != (N_layers - 1)):
    raise RuntimeError("Incorrect number of interface properties")

  ConductionMatrix = np.array([[1, 0], [0, 1]])
  
  for i in range(N_layers):
  
    h = layer_props[i][0]
    kappa_z = layer_props[i][1]
    kappa_r = layer_props[i][2]
    rho = layer_props[i][3]
    c = layer_props[i][4]
    
    # Equation 3.44  
    gamma = cmath.sqrt((kappa_r * (k**2) + rho * c * 1j * 2 * np.pi * freq)/kappa_z)
    
    # Equation 3.34  
    A = 1.0
    B = (-1.0/(kappa_z * gamma)) * np.tanh(gamma * h)
    C = -kappa_z * gamma * np.tanh(gamma * h)
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
  
  # converting from 1/e beam waist to 1/e^2 beam waist
  r_pump = r_pump * np.sqrt(2)
  r_probe = r_probe * np.sqrt(2)

  # calibration constants to account for mesh sensitivity  
  # Only use calibration in extreme cases where a fine mesh is not an option
  # For most applications, ignore this

  beta1 = calib_consts[0]
  r_pump = r_pump*beta1

  beta2 = calib_consts[1]
  r_pump = r_pump*beta2
  
  # G(k) * P(k)
  G_k_P_k = (-D_total/C_total) * np.exp((-k**2 * r_pump**2)/8)
  
  r_bound = 50*r_probe
  S_k, _ = quad(integrand_r, 0, r_bound, args=(x0, r_probe, k))
  
  # G(k) is solution to 3D heat equation in frequency domain + hankel space
  # P(k) is applied harmonic heat source
  # S(k) is normalized probe
  
  return  S_k * G_k_P_k * k


def calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, x0, calib_consts, freq, pump_power):
  result, error = quad_vec(integrand_k, 0, 10000001, args=(N_layers, layer_props, interface_props, r_pump, r_probe, x0, calib_consts, freq))

  # Thermal response in frequency domain, Equation 3.5
  H = (pump_power/(2 * np.pi)) * result

  phase = math.atan(H.imag/H.real)
  amplitude = cmath.sqrt(H.real**2 + H.imag**2).real

  return phase, amplitude
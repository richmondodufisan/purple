import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.integrate import quad_vec
from scipy.special import i0,j0 
import math
import cmath
import pdb

# This is a helper file for calculating phase and temperature increase in FDTR experiments
# It is assumed that thermal transport is within the diffusive regime, hence Fourier's equation applies
# This is the analytical solution for radial heat transfer with an offset, using an unnormalized ring-shaped super gaussian

# The calc_thermal_response function should be used to find the phase and amplitude given the appropriate material properties



# To use in another file, include the line: 
# "from Layered_Heat_Conduction_ConcentricGaussian import calc_thermal_response"

# This is a modification to allow for offset beam positions


# Input arguments for calc_thermal_response:

# N_layers: The number of layers. Must be an unsigned (positive) integer value

# layer_props: This should be a NumPy array of arrays. The arrays should be organized in descending order,
# i.e, from the bottom to the top (e.g [layer3, layer2, layer1]). Each layer array should contain the following material
# properties IN ORDER: [h (layer thickness), kappa_z (cross plane thermal conductivity), kappa_r (in plane/radial thermal conductivity),
# rho (density), c (heat capacity)]

# interface_props: this is an array of the interface conductances between layers. There should be one less
# conductance than the number of layers (e.g 1 interface conductance for a 2-layer system)

# w_pump: radius of the pump laser

# w_probe: radius of the probe laser

# freq: frequency of the input signal (pump laser)

# pump_power: the pump power, Q0 * absorbance

# r0: the beam offset

# order: the order of the super gaussian





# Expression for normalized gaussian based on 1/e^2 beam waist

# Coarse Integrator (I don't care about accuracy of amplitude)
# Hence normalization factor can be offset

def coarse_integrate(func, a, b, N=10):
    r_vals = np.linspace(a, b, N)
    y_vals = func(r_vals)
    return np.trapz(y_vals, r_vals)

# Super-Gaussian Pump Profile
def normalized_pump_profile(r, r0, w, n):
    # Unnormalized super-Gaussian ring profile * r (for 2D integration)
    return np.exp(-2 * ((r - r0) / w) ** n) * r

# Pump Integrand for Hankel Transform 
def pump_integrand_to_hankel(r, r0, w, k, n):
    # Integrand: normalized super-Gaussian * Bessel function J0(k r)
    
    # Compute normalization with coarse integration
    integrand = lambda r_vals: normalized_pump_profile(r_vals, r0, w, n)
    integral_result = coarse_integrate(integrand, 0, r0 + 10 * w, N=10)
    
    normalization = 1.0 / (2 * np.pi * integral_result)
    
    # Unnormalized pump profile (for actual integrand)
    P_r = np.exp(-2 * ((r - r0) / w) ** n)
    
    return normalization * P_r * r * j0(k * r)
    
    
    
def probe_integrand_to_hankel(r, w, k):
    
    exponent_term = np.exp(  (-2 * (r**2))   /   (w**2)   )
  
    prefactor = 2 / (np.pi * (w**2))
    
    # Pump gaussian in r
    S_r = prefactor * exponent_term
    
    return S_r * r * j0(k * r)





def integrand(k, N_layers, layer_props, interface_props, w_pump, w_probe, r0, n, freq):

  # Checks to ensure data is properly submitted/formatted
  
  if (len(layer_props) != N_layers):
    raise RuntimeError("Size of layer properties and number of layers do not match")
    
  if (len(interface_props) != (N_layers - 1)):
    raise RuntimeError("Incorrect number of interface properties")
    


  # Bounds for numerical integral, large number
  # Contributions beyond 8x the pump/probe radius are negligible
  r_bound = 10*w_pump
  
  # Pump Gaussian in Hankel Space 
  P_k, _ = quad(pump_integrand_to_hankel, 0, r_bound, args=(r0, w_pump, k, n))
  S_k, _ = quad(probe_integrand_to_hankel, 0, r_bound, args=(w_probe, k))
  


  # Calculate Thermal Response Matrix
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
  
  G_k = (-D_total/C_total)
  

  return S_k * G_k * P_k * k * 2 * np.pi
  




def calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, r0, order, freq, pump_power):


  # Converting from 1/e beam waist to 1/e^2 beam waist
  # Comment out if using 1/e beam waist
  w_pump = w_pump * np.sqrt(2)
  w_probe = w_probe * np.sqrt(2)



  result, error = quad_vec(integrand, 0, 10000001, args=(N_layers, layer_props, interface_props, w_pump, w_probe, r0, order, freq))
  
  H = pump_power * result

  # phase = math.atan2(H.imag, H.real)
  phase = math.atan(H.imag / H.real)
  amplitude = cmath.sqrt(H.real**2 + H.imag**2).real

  return phase, amplitude
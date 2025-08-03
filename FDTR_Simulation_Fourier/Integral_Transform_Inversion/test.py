import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from Layered_Heat_Conduction_Beam_Offset import calc_thermal_response
from Layered_Heat_Conduction import calc_thermal_response
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import pdb
import csv
import math


# File for calculating phase and amplitude for any parameters (for checking)
# Mostly for debugging purposes

freq = 1.0 # in MHz
kappa = 130.0 # in W/(m.K)
conductance_12 = 30e6 # in W/(m2.K)
conductance_23 = 30e6 # in W/(m2.K)

# ################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY, BEAM OFFSET #####################################

# # Define other parameters required by calc_thermal_response function
# N_layers = 2
# layer2 = [40e-6, kappa, kappa, 2329, 689.1]
# layer1 = [9e-8, 215, 215, 19300, 128.7]
# layer_props = np.array([layer2, layer1])
# interface_props = [conductance]
# r_probe = 1.34e-6
# r_pump = 1.53e-6
# x0 = 2e-6
# pump_power = 0.01
# calib_consts = [1, 1] # no calibration
# freq = freq * 1e6

# # Calculate analytical phase 
# phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, x0, calib_consts, freq, pump_power)

# print("----------------------------------------------------------------------------------------------")
# print("Phase: " + str(phase)) 
# print("Amplitude: " + str(amplitude)) 
# print("----------------------------------------------------------------------------------------------")

# ################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################



################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################

# Define other parameters required by calc_thermal_response function
N_layers = 3
layer3 = [39.91e-6, kappa, kappa, 2329, 689.1]
layer2 = [90e-9, kappa, kappa, 2329, 689.1]
layer1 = [90e-9, 215, 215, 19300, 128.7]
layer_props = np.array([layer3, layer2, layer1])
interface_props = [conductance_23, conductance_12]
r_probe = 1.34e-6
r_pump = 1.53e-6
pump_power = 0.01
freq = freq * 1e6

# Calculate analytical phase 
phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, freq, pump_power)

print("----------------------------------------------------------------------------------------------")
print("Phase: " + str(phase)) 
print("Amplitude: " + str(amplitude)) 
print("----------------------------------------------------------------------------------------------")

################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################





import torch
from Layered_Heat_Conduction_PyTorch import calc_thermal_response_torch

# Define constants and convert units
freq = 1.0 * 1e6  # Hz
kappa = 130.0
conductance_12 = 30e6
conductance_23 = 30e6

# Define 3-layer system (thickness [m], k_z, k_r, rho, c)
layer3 = [39.91e-6, kappa, kappa, 2329, 689.1]
layer2 = [90e-9, kappa, kappa, 2329, 689.1]
layer1 = [90e-9, 215, 215, 19300, 128.7]
layer_props = [layer3, layer2, layer1]
interface_props = [conductance_23, conductance_12]

# Torch-ify everything
layer_props_torch = [
    [torch.tensor(v, dtype=torch.float32) for v in layer] for layer in layer_props
]
interface_props_torch = [
    torch.tensor(g, dtype=torch.float32) for g in interface_props
]

# Define geometry
r_probe = torch.tensor(1.34e-6, dtype=torch.float32)
r_pump = torch.tensor(1.53e-6, dtype=torch.float32)
pump_power = torch.tensor(0.01, dtype=torch.float32)
freq_torch = torch.tensor(freq, dtype=torch.float32)

# Compute thermal response
phase, amplitude = calc_thermal_response_torch(
    N_layers=3,
    layer_props=layer_props_torch,
    interface_props=interface_props_torch,
    w_pump=r_pump,
    w_probe=r_probe,
    freq=freq_torch,
    pump_power=pump_power,
    device='cpu'
)

print("----------------------------------------------------------------------------------------------")
print("Phase (radians):", phase)
print("Amplitude:", amplitude)
print("----------------------------------------------------------------------------------------------")





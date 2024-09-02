import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction_Beam_Offset import calc_thermal_response
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import pdb
import csv
import math


# File for calculating phase and amplitude for any parameters (for checking)
# Mostly for debugging purposes

freq = 1 # in MHz
kappa = 130 # in W/(m.K)
conductance = 3e7 # in W/(m2.K)

################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY, BEAM OFFSET #####################################

# Define other parameters required by calc_thermal_response function
N_layers = 2
layer2 = [40e-6, kappa, kappa, 2329, 689.1]
layer1 = [9e-8, 215, 215, 19300, 128.7]
layer_props = np.array([layer2, layer1])
interface_props = [conductance]
r_probe = 1.34e-6
r_pump = 1.53e-6
x0 = 0
pump_power = 0.01
calib_consts = [1, 1] # no calibration
freq = freq * 1e6

# Calculate analytical phase 
phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, x0, calib_consts, freq, pump_power)

print("----------------------------------------------------------------------------------------------")
print("Phase: " + str(phase)) 
print("Amplitude: " + str(amplitude)) 
print("----------------------------------------------------------------------------------------------")

################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################




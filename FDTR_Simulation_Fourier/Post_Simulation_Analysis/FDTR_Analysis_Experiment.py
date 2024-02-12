import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
from Phase_Extraction_Cosine_Fit import calculate_phase_amplitude
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import math

import pdb


############################################# READING IN AND ORGANIZING DATA #############################################

# Read the CSV files into pandas DataFrames
FDTR_data = pd.read_csv('./Point2.csv', skiprows=0, names=['frequency', 'phase'])

# FDTR_data['frequency'] = FDTR_data['frequency'] * 1e6 # Convert to Hz (EDIT: Do not convert here, will be converted elsewhere)
FDTR_data['phase'] = FDTR_data['phase'] * (math.pi/180) # Convert to radians

############################################# END READING IN AND ORGANIZING DATA #############################################



############################################# FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################

def fit_function_FDTR(freqs, k_Si, conductance):
    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, k_Si, k_Si, 2329, 689.1]
        layer1 = [9e-8, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [conductance]
        r_probe = 1.34e-6
        r_pump = 1.53e-6
        pump_power = 0.01
        calib_consts = [1, 1] # no calibration
        # calib_consts = [1,1] # default
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        phases.append(phase)
        
    return np.array(phases)


# Fit the actual simulation data
thermal_conductivity = []
interface_conductance = []

FDTR_freq = np.array(FDTR_data['frequency'])
FDTR_phase = np.array(FDTR_data['phase'])

    
# popt = optimized params (kappa and conductance), pcov = covariance (not needed, except maybe for debugging)
popt, pcov = curve_fit(
    fit_function_FDTR,
    FDTR_freq,   # Frequency data
    FDTR_phase,  # Phase data
    p0=(130, 3e7), # Initial guesses
    bounds=([0, 1e7], [300, 5e7]),  # Set bounds for k_Si and conductance
    method='trf',  # Use Trust Region Reflective algorithm
    maxfev=10000,  # Maximum number of function evaluations
    ftol=1e-12,   # Set the tolerance on the relative error in the function values
    xtol=1e-12,   # Set the tolerance on the relative error in the parameter values
    gtol=1e-12    # Set the tolerance on the norm of the gradient
)

k_Si_opt, conductance_opt = popt
perr = np.sqrt(np.diag(pcov))   # Standard Deviation of solution, diagonal elements of pcov are the variances of each param with itself

# Find MSE
residuals = FDTR_phase - fit_function_FDTR(FDTR_freq, *popt)
mse = np.mean(residuals**2)

thermal_conductivity.append(k_Si_opt)
interface_conductance.append(conductance_opt)
 
print("----------------------------------------------------------------------------------------------")
print("Thermal Conductivity = " + str(thermal_conductivity))
print("Interface Conductance = " + str(interface_conductance))
print("MSE = " + str(mse))

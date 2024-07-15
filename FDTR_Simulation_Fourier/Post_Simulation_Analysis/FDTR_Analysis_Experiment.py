import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction_Approximation import calc_thermal_response
from Phase_Extraction_Cosine_Fit import calculate_phase_amplitude
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import math

import pdb

# This code is for calculating thermal properties (thermal conductivity and interface conductance) from experimental data
# The code is for point measurements, and assumes that the necessary data points are in the same folder with the same file prefix,
# with a number at the end denoting which sample it is. The "num_files" variable denotes how many files to read.

# For some samples, higher frequencies enter the non-Fourier regime, and need to be removed before fitting. The "cutoff"
# variable within the "process_file" function is responsible for adjusting the number of points to cut off.

##################################################### FUNCTION DEFINITIONS ###################################################

# Two-Layer FDTR Function

def fit_function_FDTR(freqs, k_Si, conductance):
    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [100e-6, k_Si, k_Si, 2630, 741.79]
        layer1 = [133e-9, 194, 194, 19300, 126.4]
        layer_props = np.array([layer2, layer1])
        interface_props = [conductance]
        r_probe = 1.249e-6
        r_pump = 2.216e-6
        pump_power = 1.5
        calib_consts = [1, 1] # no calibration
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        phases.append(phase)
        
    return np.array(phases)
    

# Three-Layer FDTR Function

# def fit_function_FDTR(freqs, k_Si, conductance):
    # phases = []

    # for freq in freqs:
        # # Define other parameters required by calc_thermal_response function
        # N_layers = 3
        # layer3 = [100e-6, k_Si, k_Si, 2329, 689.1]              #Si
        # layer2 = [1000e-9, 2.748, 2.748, 2630, 741.79]           #SiO2
        # layer1 = [133e-9, 194, 194, 19300, 126.4]               #Au
        # layer_props = np.array([layer3, layer2, layer1])
        # interface_props = [conductance, 43.873e6]
        # r_probe = 1.249e-6
        # r_pump = 2.216e-6
        # pump_power = 1.5
        # calib_consts = [1, 1] # no calibration
        # freq = freq * 1e6

        # # Calculate analytical phase 
        # phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        # phases.append(phase)
        
    # return np.array(phases)
    
    
def process_file(file_path):
    # Read the CSV file into a pandas DataFrame
    FDTR_data = pd.read_csv(file_path, skiprows=1, names=['frequency', 'phase'])
    FDTR_data['phase'] = FDTR_data['phase'] * (math.pi / 180)  # Convert to radians
    
    
    # cutoff_start = 20 # number of points to cutoff from the start
    # FDTR_data = FDTR_data[cutoff_start:]
    
    
    cutoff_end = 15 # number of points to cutoff from the end
    FDTR_data = FDTR_data[:-cutoff_end]

    # Perform the curve fitting
    popt, pcov = curve_fit(
        fit_function_FDTR,
        FDTR_data['frequency'],   # Frequency data
        FDTR_data['phase'],  # Phase data
        p0=(130, 100e6), # Initial guesses
        bounds=([0, 10e6], [300, 500e6]),  # Set bounds for kappa and conductance
        method='trf',  # Use Trust Region Reflective algorithm
        maxfev=10000,  # Maximum number of function evaluations
        ftol=1e-12,   # Set the tolerance on the relative error in the function values
        xtol=1e-12,   # Set the tolerance on the relative error in the parameter values
        gtol=1e-12    # Set the tolerance on the norm of the gradient
    )
    
    return FDTR_data, popt
    
##################################################### END FUNCTION DEFINITIONS ###################################################






##################################################### READ DATA AND PERFORM FITTING ###################################################

# Specify the folder and number of files
folder_path = './Rosemary_SiO2_Standard'  
num_files = 6  # Specify the number of files

# Initialize subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

# Loop through each file
for i in range(num_files):
    file_path = os.path.join(folder_path, f'Results_SiSi_interface_{i + 1}.csv')
    FDTR_data, popt = process_file(file_path)
    kappa_opt, conductance_opt = popt
    
    # Generate fitted data
    FDTR_phase_fitted = fit_function_FDTR(FDTR_data['frequency'], kappa_opt, conductance_opt)
    
    # Calculate the mean square error
    mse = np.mean((FDTR_data['phase'] - FDTR_phase_fitted) ** 2)
    
    # Plot the data points and the fitted line, excluding the last point
    axes[i].scatter(FDTR_data['frequency'][:-1], FDTR_data['phase'][:-1], label='Data Points', color='blue')
    axes[i].plot(FDTR_data['frequency'][:-1], FDTR_phase_fitted[:-1], label='Fitted Line', color='red')
    axes[i].set_xscale('log')  # Set the x-axis to a logarithmic scale
    axes[i].set_xlabel('Frequency')
    axes[i].set_ylabel('Phase')
    axes[i].legend()
    axes[i].set_title(f'kappa: {kappa_opt:.2f} W/(m.K), conductance: {(conductance_opt/1e6):.2f} MW/(m^2.K) \nMSE: {mse:.2e}')

plt.subplots_adjust(wspace=0.3, hspace=0.5)

save_path = f'{folder_path}_NIST.png'
plt.savefig(save_path)

plt.show()
##################################################### END READ DATA AND PERFORM FITTING ###################################################
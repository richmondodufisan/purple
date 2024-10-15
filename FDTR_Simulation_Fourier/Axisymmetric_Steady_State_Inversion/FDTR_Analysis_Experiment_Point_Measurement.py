import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Two_Layer_Inversion import calc_thermal_response
from scipy.optimize import curve_fit
import math

import pdb

# This code is for calculating thermal properties (thermal conductivity and interface conductance) from experimental data
# The code is for point measurements, and assumes that the necessary data points are in the same folder with the same file prefix,
# with a number at the end denoting which sample it is. The "num_files" variable denotes how many files to read.

# For some samples, higher frequencies enter the non-Fourier regime, and need to be removed before fitting. The "cutoff"
# variable within the "process_file" function is responsible for adjusting the number of points to cut off.

# Please see the documentation in Layered_Heat_Conduction to understand how material properties are passed to calc_thermal_response'



##################################################### FUNCTION DEFINITIONS ###################################################

# In the fit_function_FDTR function, we pass the fitting properties as an array
# These are the material properties that are fit.
# If you need to fit more at the same time, you need to change:

# Bounds & Initial Guesses for the fitting (under READ DATA AND PERFORM FITTING section)
# fit_function_FDTR (right here, under FUNCTION DEFINITIONS)
# extraction of fitted results (under READ DATA AND PERFORM FITTING section)
# plotting results (under READ DATA AND PERFORM FITTING section), adjust the title to show additional fitted properties


# I have also added the comment "CHANGE IF CHANGING FITTING PROPERTIES" to each of those locations to make them searchable






# Two-Layer FDTR Function

def fit_function_FDTR(freqs, fitting_properties):
    phases = []
    
    # CHANGE IF CHANGING FITTING PROPERTIES
    kappa_2, conductance_12 = fitting_properties  # Adjust the fitting parameters as needed

    for freq in freqs:       
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, kappa_2, kappa_2, 2630, 741.79]
        layer1 = [133e-9, 194, 194, 19300, 126.4]
        layer_props = np.array([layer2, layer1])
        interface_props = [conductance_12]
        r_probe = 1.249e-6
        r_pump = 2.216e-6
        pump_power = 1.5
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, freq, pump_power)

        phases.append(phase)
        
    return np.array(phases)



# Process a single CSV file and perform fitting
def process_file(file_path, initial_guesses, bounds_lower, bounds_upper):

    # Read the CSV file into a pandas DataFrame
    FDTR_data = pd.read_csv(file_path, skiprows=1, names=['frequency', 'phase'])
    FDTR_data['phase'] = FDTR_data['phase'] * (math.pi / 180)  # Convert to radians
    
    
    
    # Optional: Cutoff points from the start and end of the data
    
    cutoff_end = 13  # Number of points to cutoff from the end
    FDTR_data = FDTR_data[:-cutoff_end]
    
    # cutoff_start = 14 # number of points to cutoff from the start
    # FDTR_data = FDTR_data[cutoff_start:]



    # Perform the curve fitting using the flexible fitting properties
    popt, pcov = curve_fit(
        lambda freqs, *fitting_properties: fit_function_FDTR(freqs, fitting_properties),
        FDTR_data['frequency'],   # Frequency data
        FDTR_data['phase'],  # Phase data
        p0=initial_guesses,  # Initial guesses for the fitting properties
        bounds=(bounds_lower, bounds_upper),  # Bounds for the fitting properties
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

# Define initial guesses and bounds for the fitting properties
# CHANGE IF CHANGING FITTING PROPERTIES

initial_guesses = [3, 40e6]  # Initial guesses for k_Si and conductance (you can add more fitting properties)
bounds_lower = [0, 10e6]     # Lower bounds for the fitting properties
bounds_upper = [300, 500e6]  # Upper bounds for the fitting properties

# Initialize subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

# Loop through each file
for i in range(num_files):
    file_path = os.path.join(folder_path, f'Results_SiSi_interface_{i + 1}.csv')
    
    # Process the file and perform the fitting
    FDTR_data, popt = process_file(file_path, initial_guesses, bounds_lower, bounds_upper)
    
    # Extract the fitted parameters (adjust based on the number of fitting properties)
    # CHANGE IF CHANGING FITTING PROPERTIES
    kappa_opt, conductance_opt = popt
    
    # Generate fitted data using the optimized parameters
    FDTR_phase_fitted = fit_function_FDTR(FDTR_data['frequency'], popt)
    
    # Calculate the mean square error
    mse = np.mean((FDTR_data['phase'] - FDTR_phase_fitted) ** 2)
    
    # Plot the data points and the fitted line, excluding the last point
    axes[i].scatter(FDTR_data['frequency'][:-1], FDTR_data['phase'][:-1], label='Data Points', color='blue')
    axes[i].plot(FDTR_data['frequency'][:-1], FDTR_phase_fitted[:-1], label='Fitted Line', color='red')
    axes[i].set_xscale('log')  # Set the x-axis to a logarithmic scale
    axes[i].set_xlabel('Frequency (MHz)', fontsize=15)
    axes[i].set_ylabel('Phase (Radians)', fontsize=15)
    axes[i].legend()
    
    # CHANGE IF CHANGING FITTING PROPERTIES
    axes[i].set_title(f'κ: {kappa_opt:.2f} W/(m.K), G: {(conductance_opt/1e6):.2f} MW/(m^2.K) \nMSE: {mse:.2e}', fontsize=15)
    axes[i].tick_params(axis='both', which='major', labelsize=15)

# Adjust the layout of the subplots
plt.subplots_adjust(wspace=0.3, hspace=0.5)

# Save the figure
save_path = f'{folder_path}.png'
plt.savefig(save_path)

plt.show()

##################################################### END READ DATA AND PERFORM FITTING ###################################################

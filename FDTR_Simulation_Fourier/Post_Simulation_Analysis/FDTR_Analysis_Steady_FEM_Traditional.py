import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import pdb
import csv
import math

############################################# READING IN AND ORGANIZING DATA #############################################

# Read the CSV files into pandas DataFrames
calibration_data = pd.read_csv('FDTR_CALIBRATION_out_theta_0.csv', skiprows=1, names=['x0', 'frequency', 'imag_part', 'real_part'])
FDTR_data = pd.read_csv('FDTR_input_Traditional_out_1_5_um.csv', skiprows=1, names=['x0', 'frequency', 'imag_part', 'real_part'])
theta_angle = "0" # for output file name change

# Extract lists of unique frequencies (in MHz) and unique x0 values
calib_freq_vals = calibration_data['frequency'].unique().tolist()
calib_x0_val = calibration_data['x0'].unique()[0] # Should be only one value

# Extract lists of unique frequencies (in MHz) and unique x0 values
FDTR_freq_vals = FDTR_data['frequency'].unique().tolist()
FDTR_x0_vals = FDTR_data['x0'].unique().tolist()

# Skip first sampled frequency
# FDTR_freq_vals = FDTR_freq_vals[1:]
# calib_freq_vals = calib_freq_vals[1:]

############################################# END READING IN AND ORGANIZING DATA #############################################








############################################# CALCULATING PHASE VALUES FROM DATA #############################################

# List of phase values for each frequency
calib_phase_vals = []

# Calculate phases of all datasets
for freq in calib_freq_vals:

    # Filter the original DataFrame to get the subset DataFrame for the specific (x0, frequency) pair
    subset_df = calibration_data[(calibration_data['x0'] == calib_x0_val) & (calibration_data['frequency'] == freq)][['imag_part', 'real_part']]

    # Check if subset_df is not empty
    if not subset_df.empty:
    
        # Calculate phase and amplitude
        imag_val = subset_df['imag_part'].iloc[0]
        real_val = subset_df['real_part'].iloc[0]
        
        phase = math.atan2(imag_val, real_val)
    
        amplitude = math.sqrt(imag_val**2 + real_val**2)

        # Save phase values
        calib_phase_vals.append(phase)



# Dictionary of actual data. Each x0 value has a list phases for every frequency
# Key is x0 value, Value is list of phases for all frequencies
# Formatted this way to make thermal conductivity fitting easier
FDTR_phase_data = {} 

for x0 in FDTR_x0_vals:
    phase_vals = []
    
    for freq in FDTR_freq_vals:
        
        # Filter the original DataFrame to get the subset DataFrame for the specific (x0, frequency) pair
        subset_df = FDTR_data[(FDTR_data['x0'] == x0) & (FDTR_data['frequency'] == freq)][['imag_part', 'real_part']]
        
        # Check if subset_df is not empty
        if not subset_df.empty:
        
            # Calculate phase and amplitude
            imag_val = subset_df['imag_part'].iloc[0]
            real_val = subset_df['real_part'].iloc[0]
            
            phase = math.atan2(imag_val, real_val)
        
            amplitude = math.sqrt(imag_val**2 + real_val**2)
        
            # Save phase values
            phase_vals.append(phase)
        
    FDTR_phase_data[x0] = phase_vals


# Make a phase plot
# First, regroup phases by frequency
phase_by_freq = []

for i in range(0, len(FDTR_freq_vals)):
    phase_values = []
    
    for x0 in FDTR_x0_vals:
        phase_values.append(FDTR_phase_data[x0][i])

    phase_by_freq.append(phase_values)
    
# print(FDTR_freq_vals)
    
# Next, subtract all phase values by the value of the phase furthest from the GB    
for i in range(0, len(FDTR_freq_vals)):
    arr = np.array(phase_by_freq[i])
    relative_phase = arr - arr[0]
    plt.plot(FDTR_x0_vals, relative_phase, marker='o', markersize=5, label=str(FDTR_freq_vals[i]) + "MHz")

plt.xlabel('Pump/Probe Position')
plt.ylabel('Relative Phase')
plt.title("Relative Phase vs Position")
plt.legend(title='Frequencies')
plt.grid(True)
plt.savefig(f"Phase_Profile_Theta_{theta_angle}.png", bbox_inches='tight')
plt.show()
    
############################################# END CALCULATING PHASE VALUES FROM DATA #############################################








############################################# CALIBRATING ANALYTICAL MODEL TO MESH REFINEMENT #############################################

calib_k_Si = 130

def fit_function_calib(freqs, beta1, beta2):
    global calib_k_Si
    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, calib_k_Si, calib_k_Si, 2329, 689.1]
        layer1 = [9e-8, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [3e7]
        r_probe = 1.34e-6
        r_pump = 1.53e-6
        pump_power = 0.01
        calib_consts = [beta1, beta2]
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        phases.append(phase)
        
    return np.array(phases)

freq_data = np.array(calib_freq_vals)
phase_data = np.array(calib_phase_vals)

# Initial guess for calibration constants
initial_guess = [1, 1]

calib_consts_optimized, _ = curve_fit(fit_function_calib, freq_data, phase_data, p0=initial_guess, maxfev=5000, ftol=1e-12, xtol=1e-12, gtol=1e-12)

print("----------------------------------------------------------------------------------------------")
print("Optimized calibration constants:", calib_consts_optimized) 
print("Calibrated phases: " + str(fit_function_calib(freq_data, *calib_consts_optimized)))
print("Simulation phases: " + str(phase_data))
print("----------------------------------------------------------------------------------------------")

############################################# END CALIBRATING ANALYTICAL MODEL TO MESH REFINEMENT #############################################







############################################# FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################

# Define wrapper function and material properties for fitting actual data
def fit_function_FDTR(freqs, G):
    phases = []
    global calib_consts_optimized

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 3
        layer3 = [38.45e-6, 130, 130, 2329, 689.1]
        layer2 = [1.55e-6, 130, 130, 2329, 689.1]
        layer1 = [9e-8, 215, 215, 19300, 128.7]
        layer_props = np.array([layer3, layer2, layer1])
        interface_props = [G, 3e7]
        r_probe = 1.34e-6
        r_pump = 1.53e-6
        pump_power = 0.01
        # calib_consts = calib_consts_optimized # optimized to mesh refinement
        calib_consts = [1,1] # default i.e no calibration
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        phases.append(phase)
        
    return np.array(phases)



# Fit the actual simulation data
FDTR_freq = np.array(FDTR_freq_vals)

interface_conductance = 0 # initialize outside the loop

counter = 0

# code is copied from GibbsExcess version hence the loop
# but it should only be one value
for x0 in FDTR_x0_vals:

    FDTR_phase = np.array(FDTR_phase_data[x0])

    # popt = optimized params (conductance), pcov = covariance (not needed, except maybe for debugging)
    popt, pcov = curve_fit(
        fit_function_FDTR,
        FDTR_freq,   # Frequency data
        FDTR_phase,  # Phase data
        method='trf',  # Use Trust Region Reflective algorithm
        maxfev=10000,  # Maximum number of function evaluations
        ftol=1e-12,   # Set the tolerance on the relative error in the function values
        xtol=1e-12,   # Set the tolerance on the relative error in the parameter values
        gtol=1e-12    # Set the tolerance on the norm of the gradient
    )
    
    interface_conductance = popt[0] # only one value anyway

    # Plot phase/frequency fit for one location
    if (counter == 0):
        fitted_phase_vals = fit_function_FDTR(FDTR_freq, interface_conductance)
        
        plt.figure()
        plt.plot(FDTR_freq, fitted_phase_vals, marker='v', linestyle='solid', color='purple', markersize=8, label = "analytical model")
        plt.plot(FDTR_freq, FDTR_phase, marker='v', linestyle='solid', color='green', markersize=8, label = "simulation")
        plt.xlabel('Frequency')
        plt.ylabel('Phase (radians)')
        plt.title("Sample phase/frequency fit, θ = " + str(theta_angle))
        plt.grid(True)
        plt.legend()
        plt.savefig(f"Phase_Fit_{theta_angle}.png", bbox_inches='tight')
        plt.show()
    
    counter = counter + 1


resistance = 1/interface_conductance

print("----------------------------------------------------------------------------------------------")
print("Resistance = " + str(resistance))
print("----------------------------------------------------------------------------------------------")

############################################# END FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################
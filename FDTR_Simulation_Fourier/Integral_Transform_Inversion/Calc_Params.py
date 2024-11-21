import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import pdb
import csv
import math


# File for calculating phase and amplitude for any parameters (for checking)
# Mostly for debugging purposes

freq = 10 # in MHz
kappa = 1.8 # in W/(m.K)
# conductance = 3e7 # in W/(m2.K)
conductance = 13e6 # in W/(m2.K)

################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################

# Define other parameters required by calc_thermal_response function
# N_layers = 2
# layer2 = [40e-6, kappa, kappa, 2329, 689.1]
# layer1 = [9e-8, 215, 215, 19300, 128.7]
# layer_props = np.array([layer2, layer1])
# interface_props = [conductance]
# r_probe = 1.34e-6
# r_pump = 1.53e-6
# pump_power = 0.01
# calib_consts = [1, 1] # no calibration
# freq = freq * 1e6


N_layers = 2
layer2 = [100e-6, kappa, kappa, 6180, 249.06]
layer1 = [80e-9, 215, 215, 19300, 128.5]
layer_props = np.array([layer2, layer1])
interface_props = [conductance]
r_probe = 1.46e-6
r_pump = 1.987e-6
pump_power = 1.5
calib_consts = [1, 1] # no calibration
freq = freq * 1e6

# Calculate analytical phase 
phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)

print("----------------------------------------------------------------------------------------------")
print("Phase: " + str(phase) + " radians") 
print("Phase: " + str(phase * (180/np.pi)) + " degrees") 
print("Amplitude: " + str(amplitude)) 
print("----------------------------------------------------------------------------------------------")

################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################




# ################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FILE #####################################
# # Read the CSV files into pandas DataFrames
# calibration_data = pd.read_csv('FDTR_Two_Layer_axisymmetric_out.csv', skiprows=1, names=['x0', 'frequency', 'imag_part', 'real_part'])

# # Extract lists of unique frequencies (in MHz) and unique x0 values
# calib_freq_vals = calibration_data['frequency'].unique().tolist()
# calib_x0_val = calibration_data['x0'].unique()[0] # Should be only one value if using "calib" style file

# # Calculate phases of all datasets
# for freq in calib_freq_vals:

    # # Filter the original DataFrame to get the subset DataFrame for the specific (x0, frequency) pair
    # subset_df = calibration_data[(calibration_data['x0'] == calib_x0_val) & (calibration_data['frequency'] == freq)][['imag_part', 'real_part']]

    # # Check if subset_df is not empty
    # if not subset_df.empty:
    
        # # Calculate phase and amplitude
        # imag_val = subset_df['imag_part'].iloc[0]
        # real_val = subset_df['real_part'].iloc[0]
        
        # phase_file = math.atan2(imag_val, real_val)
    
        # amplitude_file = math.sqrt(imag_val**2 + real_val**2)

        # print("----------------------------------------------------------------------------------------------")
        # print("Frequency = " + str(freq) + ", x0 = " + str(calib_x0_val))
        # print("Phase: " + str(phase_file)) 
        # print("Amplitude: " + str(amplitude_file)) 
        # print("----------------------------------------------------------------------------------------------")
# ###########################END #########################




### REPEAT FOR SINGLE LAYER MODEL #####







# ################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################

# # Define other parameters required by calc_thermal_response function
# N_layers = 1
# layer1 = [40e6 + 90e9, 215, 215, 19300, 128.7]
# layer_props = np.array([layer1])
# interface_props = []
# r_probe = 1.34e-6
# r_pump = 1.53e-6
# pump_power = 0.01
# calib_consts = [1, 1] # no calibration
# freq = freq * 1e6

# # Calculate analytical phase 
# phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)

# print("----------------------------------------------------------------------------------------------")
# print("Phase: " + str(phase)) 
# print("Amplitude: " + str(amplitude)) 
# print("----------------------------------------------------------------------------------------------")

# ################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################




# ################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FILE #####################################
# # Read the CSV files into pandas DataFrames
# calibration_data = pd.read_csv('FDTR_One_Layer_axisymmetric_out.csv', skiprows=1, names=['x0', 'frequency', 'imag_part', 'real_part'])

# # Extract lists of unique frequencies (in MHz) and unique x0 values
# calib_freq_vals = calibration_data['frequency'].unique().tolist()
# calib_x0_val = calibration_data['x0'].unique()[0] # Should be only one value if using "calib" style file

# # Calculate phases of all datasets
# for freq in calib_freq_vals:

    # # Filter the original DataFrame to get the subset DataFrame for the specific (x0, frequency) pair
    # subset_df = calibration_data[(calibration_data['x0'] == calib_x0_val) & (calibration_data['frequency'] == freq)][['imag_part', 'real_part']]

    # # Check if subset_df is not empty
    # if not subset_df.empty:
    
        # # Calculate phase and amplitude
        # imag_val = subset_df['imag_part'].iloc[0]
        # real_val = subset_df['real_part'].iloc[0]
        
        # phase_file = math.atan2(imag_val, real_val)
    
        # amplitude_file = math.sqrt(imag_val**2 + real_val**2)

        # print("----------------------------------------------------------------------------------------------")
        # print("Frequency = " + str(freq) + ", x0 = " + str(calib_x0_val))
        # print("Phase: " + str(phase_file)) 
        # print("Amplitude: " + str(amplitude_file)) 
        # print("----------------------------------------------------------------------------------------------")
# ###########################END #########################


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
from Phase_Extraction_Cosine_Fit import calculate_phase_amplitude
from scipy.optimize import curve_fit
from scipy.integrate import trapz


############################################# READING IN AND ORGANIZING DATA #############################################

# Read the CSV files into pandas DataFrames
calibration_data = pd.read_csv('FDTR_CALIBRATION_out_theta_0.csv', skiprows=1, names=['x0', 'frequency', 'time', 'temp'])
FDTR_data = pd.read_csv('MOOSE_theta_0_iteration_10_refined.csv', skiprows=1, names=['x0', 'frequency', 'time', 'temp'])
theta_angle = 0

# Extract lists of unique frequencies (in MHz) and unique x0 values
calib_freq_vals = calibration_data['frequency'].unique().tolist()
calib_x0_val = calibration_data['x0'].unique()[0] # Should be only one value

FDTR_freq_vals = FDTR_data['frequency'].unique().tolist()
FDTR_x0_vals = FDTR_data['x0'].unique().tolist()

# End period of simulation
end_period = 5

############################################# END READING IN AND ORGANIZING DATA #############################################








############################################# CALCULATING PHASE VALUES FROM DATA #############################################

# List of phase values for each frequency
calib_phase_vals = []

# Calculate phases of all datasets
for freq in calib_freq_vals:

    # Filter the original DataFrame to get the subset DataFrame for the specific (x0, frequency) pair
    subset_df = calibration_data[(calibration_data['x0'] == calib_x0_val) & (calibration_data['frequency'] == freq)][['time', 'temp']]
    
    # Calculate phase and amplitude (we only need phase though)
    phase, amplitude = calculate_phase_amplitude(subset_df, end_period, freq)
    
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
        subset_df = FDTR_data[(FDTR_data['x0'] == x0) & (FDTR_data['frequency'] == freq)][['time', 'temp']]
        
        # Calculate phase and amplitude (we only need phase though)
        phase, amplitude = calculate_phase_amplitude(subset_df, end_period, freq)
        
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
    
# Next, subtract all phase values by the value of the phase furthest from the GB    
for i in range(0, len(FDTR_freq_vals)):
    arr = np.array(phase_by_freq[i])
    #relative_phase = arr - np.max(arr)
    relative_phase = arr - arr[0]

    plt.plot(FDTR_x0_vals, relative_phase, marker='o', markersize=5, label=str(FDTR_freq_vals[i]) + "MHz")

plt.xlabel('Pump/Probe Position')
plt.ylabel('Relative Phase')
plt.title("Relative Phase vs Position")
plt.legend(title='Frequencies')
plt.grid(True)
plt.savefig("Phase_Profile.png", bbox_inches='tight')
plt.show()
    
############################################# END CALCULATING PHASE VALUES FROM DATA #############################################








############################################# CALIBRATING ANALYTICAL MODEL TO MESH REFINEMENT #############################################

def fit_function_calib(freqs, beta1, beta2):
    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, 130, 130, 2329, 689.1]
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

print("----------------------------------------------------------------")
print("Optimized calibration constants:", calib_consts_optimized) 
print("Calculated phases: " + str(fit_function_calib(freq_data, *calib_consts_optimized)))
# print(freq_data)
print("Simulation phases: " + str(phase_data))
print("----------------------------------------------------------------")

############################################# END CALIBRATING ANALYTICAL MODEL TO MESH REFINEMENT #############################################







############################################# FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################

def fit_function_FDTR(freqs, k_Si, conductance):
    phases = []
    global calib_consts_optimized

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
        calib_consts = calib_consts_optimized # optimized to mesh refinement
        # calib_consts = [1,1] # default
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        phases.append(phase)
        
    return np.array(phases)

FDTR_freq = np.array(FDTR_freq_vals)

thermal_conductivity = []
interface_conductance = []

for x0 in FDTR_x0_vals:

    FDTR_phase = np.array(FDTR_phase_data[x0])
    
    # popt = optimized params (kappa and conductance), pcov = covariance (not needed, except maybe for debugging)
    popt, pcov = curve_fit(
        fit_function_FDTR,
        FDTR_freq,   # Frequency data
        FDTR_phase,  # Phase data
        p0=(130, 3e7), # Initial guesses
        bounds=([100, 1e7], [200, 5e7]),  # Set bounds for k_Si and conductance
        method='trf',  # Use Trust Region Reflective algorithm
        maxfev=10000,  # Maximum number of function evaluations
        ftol=1e-12,   # Set the tolerance on the relative error in the function values
        xtol=1e-12,   # Set the tolerance on the relative error in the parameter values
        gtol=1e-12    # Set the tolerance on the norm of the gradient
    )
    
    k_Si_opt, conductance_opt = popt
    
    thermal_conductivity.append(k_Si_opt)
    interface_conductance.append(conductance_opt)
 
# print(thermal_conductivity)
 

plt.plot(FDTR_x0_vals, thermal_conductivity, marker='o', linestyle='--', color='black', markersize=8)
plt.xlabel('Pump/Probe Position')
plt.ylabel('Thermal Conductivity (W/(m.K)')
plt.title("Thermal Conductivity Profile, θ = " + str(theta_angle))
plt.grid(True)
plt.savefig("Thermal_Conductivity_Profile.png", bbox_inches='tight')
plt.show()

# Invert to integrate under curve
ydata = (1/np.array(thermal_conductivity)) 

# Find minimum value and create a constant line
y_min = np.min(ydata)
ydata_const = np.full(len(ydata), y_min)

# Convert to micrometers
xdata = np.array(FDTR_x0_vals).astype(float) * 1e-6

# Integrate and subtract difference from integral of constant line
resistance = trapz(ydata, x=xdata) - trapz(ydata_const, x=xdata) 


print("Resistance = " + str(resistance))
print("----------------------------------------------------------------")

############################################# END FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################
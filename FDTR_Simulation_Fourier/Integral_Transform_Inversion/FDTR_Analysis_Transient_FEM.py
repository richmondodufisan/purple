import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
from Phase_Extraction_Cosine_Fit import calculate_phase_amplitude
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import pdb
import csv

############################################# READING IN AND ORGANIZING DATA #############################################

# Read the CSV files into pandas DataFrames
FDTR_data = pd.read_csv('FDTR_input_out_theta_0.csv', skiprows=1, names=['x0', 'frequency', 'time', 'temp'])
theta_angle = "0" # for output file name change


FDTR_freq_vals = FDTR_data['frequency'].unique().tolist()
FDTR_x0_vals = FDTR_data['x0'].unique().tolist()

# Skip first sampled frequency
# FDTR_freq_vals = FDTR_freq_vals[1:]

# End period of simulation
end_period = 4

############################################# END READING IN AND ORGANIZING DATA #############################################








############################################# CALCULATING PHASE VALUES FROM DATA #############################################


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
        w_probe = 0.63e-6
        w_pump = 0.71e-6
        pump_power = 0.01
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, freq, pump_power)
        phases.append(phase)
        
    return np.array(phases)


# Fit the actual simulation data
FDTR_freq = np.array(FDTR_freq_vals)

thermal_conductivity = []
interface_conductance = []

counter = 0

for x0 in FDTR_x0_vals:

    FDTR_phase = np.array(FDTR_phase_data[x0])
    #pdb.set_trace()
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
    
    if (counter == 0):
        fitted_phase_vals = fit_function_FDTR(FDTR_freq, k_Si_opt, conductance_opt)
        
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
    
    thermal_conductivity.append(k_Si_opt)
    interface_conductance.append(conductance_opt)
 

# print(thermal_conductivity)


# Now, adjust all thermal conductivites according to calibration
thermal_conductivity = np.array(thermal_conductivity)    
 

plt.plot(FDTR_x0_vals, thermal_conductivity, marker='o', linestyle='--', color='black', markersize=8)
plt.xlabel('Pump/Probe Position')
plt.ylabel('Thermal Conductivity (W/(m.K)')
plt.title("Thermal Conductivity Profile, θ = " + str(theta_angle))
plt.grid(True)
plt.savefig(f"Thermal_Conductivity_Profile_Theta_{theta_angle}.png", bbox_inches='tight')
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
print("----------------------------------------------------------------------------------------------")

############################################# END FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################




############################################# EXPORT DATA TO CSV #############################################

# Specify the file name
file_name = f"Thermal_Conductivity_Profile_Theta_{theta_angle}.csv"

# Write data to CSV
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['FDTR_x0_vals', 'thermal_conductivity'])
    # Write data rows
    for x0, tc in zip(FDTR_x0_vals, thermal_conductivity):
        writer.writerow([x0, tc])

print("CSV file of Thermal Conductivity data has been written successfully.")
print("----------------------------------------------------------------------------------------------")
############################################# END EXPORT DATA TO CSV #############################################
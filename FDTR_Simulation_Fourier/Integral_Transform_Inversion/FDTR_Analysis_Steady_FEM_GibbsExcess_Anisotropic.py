import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from Layered_Heat_Conduction import calc_thermal_response
# from Layered_Heat_Conduction_BesselRing import calc_thermal_response
from Layered_Heat_Conduction_SuperGaussianRing import calc_thermal_response
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import pdb
import csv
import math




############################################# READING IN AND ORGANIZING DATA #############################################

# Define input filename
input_filename = 'FDTR_input_GibbsExcess_StepFunction_SuperGaussianRing_5um_out_theta_0.csv'

# Create a base name for output by stripping 'FDTR_input_' and file extension
output_basename = input_filename.replace('FDTR_input_', '').replace('.csv', '')
theta_angle = 0

# Read the CSV
FDTR_data = pd.read_csv(input_filename, skiprows=1, names=['x0', 'frequency', 'imag_part', 'real_part'])


# Extract lists of unique frequencies (in MHz) and unique x0 values
FDTR_freq_vals = FDTR_data['frequency'].unique().tolist()
FDTR_x0_vals = FDTR_data['x0'].unique().tolist()

# Skip first sampled frequency
# FDTR_freq_vals = FDTR_freq_vals[:-5]

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
        subset_df = FDTR_data[(FDTR_data['x0'] == x0) & (FDTR_data['frequency'] == freq)][['imag_part', 'real_part']]
        
        # Check if subset_df is not empty
        if not subset_df.empty:
        
            # Calculate phase and amplitude
            imag_val = subset_df['imag_part'].iloc[0]
            real_val = subset_df['real_part'].iloc[0]
            
            phase = math.atan2(imag_val, real_val)
            # phase = math.atan(imag_val/real_val)
        
            amplitude = math.sqrt(imag_val**2 + real_val**2)
        
            # Save phase values
            phase_vals.append(phase)
            
            # pdb.set_trace()
        
    FDTR_phase_data[x0] = phase_vals

# pdb.set_trace()
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
plt.savefig(f"Phase_Profile_{output_basename}.png", bbox_inches='tight')
plt.show()
    
############################################# END CALCULATING PHASE VALUES FROM DATA #############################################








############################################# FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################

# Define wrapper function and material properties for fitting actual data
def fit_function_FDTR(freqs, kappa_z, kappa_r):
    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, kappa_z, kappa_r, 2329, 689.1]
        layer1 = [9e-8, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [30e6]
        w_probe = 1.34e-6
        w_pump = 1.53e-6
        pump_power = 0.01
        offset = 5e-6
        order = 2.0
        freq = freq * 1e6

        # Calculate analytical phase 
        # phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, freq, pump_power)
        
        # phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, freq, pump_power)
        
        phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, order, freq, pump_power)
        
        phases.append(phase)
    
    phases = np.array(phases)
    
    # Ensure phase values are smooth/continuous
    phases = np.unwrap(phases)
    
    return np.array(phases)


# Fit the actual simulation data
FDTR_freq = np.array(FDTR_freq_vals)

thermal_conductivity_z = []
thermal_conductivity_r = []

counter = 0

for x0 in FDTR_x0_vals:

    FDTR_phase = np.array(FDTR_phase_data[x0])
    
    # Unwrap phase to prevent discontinuities
    FDTR_phase = np.unwrap(FDTR_phase)
    
    #pdb.set_trace()
    # popt = optimized params (kappa), pcov = covariance (not needed, except maybe for debugging)
    popt, pcov = curve_fit(
        fit_function_FDTR,
        FDTR_freq,   # Frequency data
        FDTR_phase,  # Phase data
        p0=(130, 130), # Initial guesses
        bounds=([0, 0], [300, 300]),  # Set bounds for the radial and transverse conductivities
        method='trf',  # Use Trust Region Reflective algorithm
        maxfev=10000,  # Maximum number of function evaluations
        ftol=1e-12,   # Set the tolerance on the relative error in the function values
        xtol=1e-12,   # Set the tolerance on the relative error in the parameter values
        gtol=1e-12    # Set the tolerance on the norm of the gradient
    )
    
    kappa_z_opt = popt[0]
    kappa_r_opt = popt[1]
    
    # pdb.set_trace()
    # Plot phase/frequency fit for one location
    if (counter == 0):
        fitted_phase_vals = fit_function_FDTR(FDTR_freq, kappa_z_opt, kappa_r_opt)
        
        plt.figure()
        plt.plot(FDTR_freq, fitted_phase_vals, marker='v', linestyle='solid', color='purple', markersize=8, label = "analytical model")
        plt.plot(FDTR_freq, FDTR_phase, marker='v', linestyle='solid', color='green', markersize=8, label = "simulation")
        plt.xlabel('Frequency')
        plt.ylabel('Phase (radians)')
        plt.title("Sample phase/frequency fit, θ = " + str(theta_angle))
        plt.grid(True)
        plt.legend()
        plt.savefig(f"Phase_Fit_{output_basename}.png", bbox_inches='tight')
        plt.show()
    
    counter = counter + 1
    
    thermal_conductivity_z.append(kappa_z_opt)
    thermal_conductivity_r.append(kappa_r_opt)



plt.figure()
plt.plot(FDTR_x0_vals, thermal_conductivity_z, marker='o', linestyle='--', color='black', markersize=8)
plt.xlabel('Pump/Probe Position (μm)', fontsize=15)
plt.ylabel('Thermal Conductivity (W/(m.K))', fontsize=15)
plt.title("Thermal Conductivity Profile, θ = " + str(theta_angle) + " (vertical (z) component)")
plt.grid(True)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
# plt.ylim(126.9, 130.15)
plt.tight_layout()
plt.savefig(f"Thermal_Conductivity_Profile_{output_basename}_z.png", bbox_inches='tight')
plt.show()


plt.figure()
plt.plot(FDTR_x0_vals, thermal_conductivity_r, marker='o', linestyle='--', color='black', markersize=8)
plt.xlabel('Pump/Probe Position (μm)', fontsize=15)
plt.ylabel('Thermal Conductivity (W/(m.K))', fontsize=15)
plt.title("Thermal Conductivity Profile, θ = " + str(theta_angle) + " (radial (r) component)")
plt.grid(True)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
# plt.ylim(126.9, 130.15)
plt.tight_layout()
plt.savefig(f"Thermal_Conductivity_Profile_{output_basename}_r.png", bbox_inches='tight')
plt.show()



def compute_net_resistance(x_array, kappa_array, label="z"):
    # Split at x = 0
    left_mask = x_array < 0
    right_mask = x_array > 0

    x_left = x_array[left_mask]
    x_right = x_array[right_mask]

    kappa_left = kappa_array[left_mask]
    kappa_right = kappa_array[right_mask]

    # Define bulk κ as farthest from the interface
    kappa_bulk_left = kappa_left[0]        # x = min
    kappa_bulk_right = kappa_right[-1]     # x = max

    # Invert to resistivity
    rho_left = 1 / kappa_left
    rho_right = 1 / kappa_right
    rho_bulk_left = 1 / kappa_bulk_left
    rho_bulk_right = 1 / kappa_bulk_right

    # Deviations from bulk
    delta_rho_left = rho_left - rho_bulk_left
    delta_rho_right = rho_right - rho_bulk_right

    # Integrate
    resistance_left = trapz(np.maximum(delta_rho_left, 0), x=x_left)
    boost_left = trapz(np.maximum(-delta_rho_left, 0), x=x_left)
    net_left = resistance_left - boost_left

    resistance_right = trapz(np.maximum(delta_rho_right, 0), x=x_right)
    boost_right = trapz(np.maximum(-delta_rho_right, 0), x=x_right)
    net_right = resistance_right - boost_right

    total_resistance = resistance_left + resistance_right
    total_boost = boost_left + boost_right
    total_net = net_left + net_right

    print("----------------------------------------------------------------------------------------------")
    print(f"{label.upper()} COMPONENT")
    print("LEFT SIDE:")
    print(f"  Bulk κ = {kappa_bulk_left:.4f}, 1/κ = {rho_bulk_left:.4e}")
    print(f"  Resistance  = {resistance_left:.4e}")
    print(f"  Boost       = {boost_left:.4e}")
    print(f"  Net         = {net_left:.4e}")
    print()
    print("RIGHT SIDE:")
    print(f"  Bulk κ = {kappa_bulk_right:.4f}, 1/κ = {rho_bulk_right:.4e}")
    print(f"  Resistance  = {resistance_right:.4e}")
    print(f"  Boost       = {boost_right:.4e}")
    print(f"  Net         = {net_right:.4e}")
    print()
    print("TOTAL:")
    print(f"  Resistance  = {total_resistance:.4e}")
    print(f"  Boost       = {total_boost:.4e}")
    print(f"  Net         = {total_net:.4e}")
    print("----------------------------------------------------------------------------------------------")

# Run the analysis for both z and r conductivities
x_array = np.array(FDTR_x0_vals).astype(float) * 1e-6  # meters

compute_net_resistance(x_array, np.array(thermal_conductivity_z), label="z")
compute_net_resistance(x_array, np.array(thermal_conductivity_r), label="r")



############################################# END FITTING THERMAL CONDUCTIVITY FROM ACTUAL DATA #############################################








########################################### EXPORT DATA TO CSV ################################################

# File name
csv_filename = f"Thermal_Conductivity_Profile_{output_basename}.csv"

# Convert x positions to microns for export
x_positions_um = np.array(FDTR_x0_vals).astype(float)

# Convert conductivity lists to arrays
kappa_z_array = np.array(thermal_conductivity_z)
kappa_r_array = np.array(thermal_conductivity_r)

# Combine all into a single 2D array
export_data = np.column_stack((x_positions_um, kappa_z_array, kappa_r_array))

# Create a DataFrame for easy export
df_export = pd.DataFrame(export_data, columns=["Position (µm)", "Kappa_z (W/m·K)", "Kappa_r (W/m·K)"])

# Save to CSV
df_export.to_csv(csv_filename, index=False)

print(f"Thermal conductivity data exported to {csv_filename}")

print("----------------------------------------------------------------------------------------------")
########################################### END EXPORT DATA TO CSV #############################################
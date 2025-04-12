import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from Layered_Heat_Conduction_BesselRing import calc_thermal_response
from Layered_Heat_Conduction_SuperGaussianRing import calc_thermal_response
import math

# === USER INPUTS ===
offset_list = np.linspace(0e-6, 50e-6, 50)  # offsets in meters (e.g., 0 to 15 microns)
fixed_frequency = 10e6  # Frequency in Hz (e.g., 10 MHz)
perturbation = 0.0005   # Small perturbation for sensitivity calculation

# === Thermal Parameters ===
kappa_r_val = 130      # Thermal conductivity (r-direction)
kappa_z_val = 130      # Thermal conductivity (z-direction)
G_val = 30e6           # Interface Conductance



# === FDTR Model Function ===
def FDTR_function(freqs, kappa_z, kappa_r, G, offset):
    phases = []

    for freq in freqs:
        N_layers = 2
        layer2 = [40e-6, kappa_z, kappa_r, 2329, 689.1]
        layer1 = [90e-9, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [G]
        w_probe = 1.34e-6
        w_pump = 1.53e-6
        pump_power = 0.01
        
        order = 2.0

        # phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, freq, pump_power)
        phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, order, freq, pump_power)
        
        # convert to degrees to avoid phase wrapping issues
        phase = phase * (180/np.pi)
        
        # keep within 0 and 360
        phase = phase % 360
        
        phases.append(phase)
        
    return np.array(phases)



# === Sensitivity Calculation using Finite Difference in log-space ===
def finite_difference_log(FDTR_function, freq_range, param_name, param_value, perturbation, kwargs):
    param_2low = param_value * (1 - 2 * perturbation)
    param_1low = param_value * (1 - perturbation)
    param_1high = param_value * (1 + perturbation)
    param_2high = param_value * (1 + 2 * perturbation)

    kwargs_2low = kwargs.copy(); kwargs_2low[param_name] = param_2low
    kwargs_1low = kwargs.copy(); kwargs_1low[param_name] = param_1low
    kwargs_1high = kwargs.copy(); kwargs_1high[param_name] = param_1high
    kwargs_2high = kwargs.copy(); kwargs_2high[param_name] = param_2high

    phase_2low = FDTR_function(freq_range, **kwargs_2low)
    phase_1low = FDTR_function(freq_range, **kwargs_1low)
    phase_1high = FDTR_function(freq_range, **kwargs_1high)
    phase_2high = FDTR_function(freq_range, **kwargs_2high)
    
    # log_phase_2low = np.log(phase_2low)
    # log_phase_1low = np.log(phase_1low)
    # log_phase_1high = np.log(phase_1high)
    # log_phase_2high = np.log(phase_2high)

    log_1low = np.log(param_1low)
    log_1high = np.log(param_1high)

    sensitivity = (-phase_2high + 8*phase_1high - 8*phase_1low + phase_2low) / (6 * (log_1high - log_1low))
    
    # relative_sensitivity = (-log_phase_2high + 8*log_phase_1high - 8*log_phase_1low + log_phase_2low) / (6 * (log_1high - log_1low))

    return sensitivity






# ############ PLOT OFFSET VS SENSITIVITY ###################

# Sensitivity_kappa_r_list = []
Sensitivity_kappa_z_list = []



for offset in offset_list:
    params = {
        "kappa_z": kappa_z_val,
        "kappa_r": kappa_r_val,
        "G": G_val,
        "offset": offset
    }

    freqs = np.array([fixed_frequency])  # Single frequency as array

    # sens_kappa_r = finite_difference_log(FDTR_function, freqs, "kappa_r", kappa_r_val, perturbation, params)[0]
    sens_kappa_z = finite_difference_log(FDTR_function, freqs, "kappa_z", kappa_z_val, perturbation, params)[0]


    # Sensitivity_kappa_r_list.append(sens_kappa_r)
    Sensitivity_kappa_z_list.append(sens_kappa_z)



# === Plotting ===
# plt.figure(figsize=(10, 6))
# plt.plot(np.array(offset_list)*1e6, Sensitivity_kappa_r_list, label=r'$\kappa_{r}$ (Si)', linestyle='--', linewidth=3)
# plt.grid(True)
# plt.xlabel('Offset (μm)', fontsize=14)
# plt.ylabel('Relative Sensitivity', fontsize=14)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.title(f'Relative Sensitivity vs Offset for $\\kappa_{{r}}$ (Si) at {fixed_frequency/1e6:.1f} MHz', fontsize=16)
# plt.legend(fontsize=14)
# plt.tight_layout()
# plt.savefig(f'sensitivity_vs_offset_kappa_r_{int(fixed_frequency/1e6)}MHz_1.png')
# plt.show()




plt.figure(figsize=(10, 6))
plt.plot(np.array(offset_list)*1e6, Sensitivity_kappa_z_list, label=r'$\kappa_{z}$ (Si)', linestyle='--', linewidth=3)
plt.grid(True)
plt.xlabel('Offset (μm)', fontsize=14)
plt.ylabel('Relative Sensitivity', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title(f'Sensitivity vs Offset for $\\kappa_{{z}}$ (Si) at {fixed_frequency/1e6:.1f} MHz', fontsize=16)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig(f'sensitivity_vs_offset_kappa_z_{int(fixed_frequency/1e6)}MHz_1.png')
plt.show()









############ PLOT OFFSET VS PHASE ###################

# phase_list = []

# for offset in offset_list:
    # params = {
        # "kappa_z": kappa_z_val,
        # "kappa_r": kappa_r_val,
        # "G": G_val,
        # "offset": offset
    # }

    # freqs = np.array([fixed_frequency])  # Single frequency
    # phase = FDTR_function(freqs, **params)[0]  # Get the phase at the fixed frequency
    # phase_list.append(phase)

# # === Plot Phase vs Offset ===
# plt.figure(figsize=(10, 6))
# plt.plot(np.array(offset_list)*1e6, phase_list, 'o', linewidth=1)
# plt.grid(True)
# plt.xlabel('Offset (μm)', fontsize=14)
# plt.ylabel('Phase (radians)', fontsize=14)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.title(f'Phase vs Offset at {fixed_frequency/1e6:.1f} MHz', fontsize=16)
# plt.tight_layout()
# plt.savefig(f'phase_vs_offset_{int(fixed_frequency/1e6)}MHz.png')
# plt.show()

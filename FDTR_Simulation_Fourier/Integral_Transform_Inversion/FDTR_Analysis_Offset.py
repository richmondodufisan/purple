import numpy as np
import matplotlib.pyplot as plt
from Layered_Heat_Conduction_BesselRing import calc_thermal_response

# Define the frequency for sensitivity analysis (1 MHz)
freq_1MHz = np.array([1e6])  # 1 MHz in Hz

# Define the range of offsets to test (e.g., from 1 μm to 20 μm)
offset_values = np.linspace(1e-6, 20e-6, 50)  # 50 points from 1 μm to 20 μm

# Thermal Properties
G_val = 30 * 1e6  # interface conductance
kappa_r_val = 130  # thermal conductivity r
kappa_z_val = 130  # thermal conductivity z
perturbation = 0.0005  # Small perturbation for sensitivity calculation


def FDTR_function(freqs, kappa_z, kappa_r, G, offset):
    """ Computes phase response for given parameters. """
    phases = []
    for freq in freqs:
        N_layers = 2
        layer2 = [40e-6, kappa_z, kappa_r, 2329, 689.1]  # Si layer
        layer1 = [90e-9, 215, 215, 19300, 128.7]  # Au layer
        layer_props = np.array([layer2, layer1])
        interface_props = [G]
        w_probe = 1.34e-6
        w_pump = 1.53e-6
        pump_power = 0.01
        
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, freq, pump_power)
        phases.append(phase)
    
    return np.array(phases)


def finite_difference_log(FDTR_function, freq_range, param_name, param_value, perturbation, kwargs, offset):
    """ Computes sensitivity using four-point central differencing on a logarithmic scale. """
    param_2low = param_value * (1 - 2 * perturbation)  
    param_1low = param_value * (1 - perturbation)     
    param_1high = param_value * (1 + perturbation)     
    param_2high = param_value * (1 + 2 * perturbation) 

    # Compute perturbed values
    kwargs_2low = kwargs.copy()
    kwargs_1low = kwargs.copy()
    kwargs_1high = kwargs.copy()
    kwargs_2high = kwargs.copy()

    kwargs_2low[param_name] = param_2low
    kwargs_1low[param_name] = param_1low
    kwargs_1high[param_name] = param_1high
    kwargs_2high[param_name] = param_2high

    # Compute phase responses
    phase_2low = FDTR_function(freq_range, **kwargs_2low, offset=offset)
    phase_1low = FDTR_function(freq_range, **kwargs_1low, offset=offset)
    phase_1high = FDTR_function(freq_range, **kwargs_1high, offset=offset)
    phase_2high = FDTR_function(freq_range, **kwargs_2high, offset=offset)

    # Compute log differences
    log_2low = np.log(param_2low)
    log_1low = np.log(param_1low)
    log_1high = np.log(param_1high)
    log_2high = np.log(param_2high)

    # Compute sensitivity using four-point central differencing
    sensitivity = (-phase_2high + 8 * phase_1high - 8 * phase_1low + phase_2low) / (6 * (log_1high - log_1low))

    return sensitivity


# Store sensitivity values
sensitivity_kappa_r_values = []

# Compute sensitivity for different offsets
for offset in offset_values:
    params = {"kappa_z": kappa_z_val, "kappa_r": kappa_r_val, "G": G_val}
    sensitivity_kappa_r = finite_difference_log(FDTR_function, freq_1MHz, "kappa_r", kappa_r_val, perturbation, params, offset)
    
    sensitivity_kappa_r_values.append(sensitivity_kappa_r[0])  # Extract scalar value

# Plot sensitivity vs. offset
plt.figure(figsize=(10, 6))
plt.plot(offset_values * 1e6, sensitivity_kappa_r_values, marker='o', linestyle='-', linewidth=2)

# Labels and title
plt.xlabel('Offset (μm)', fontsize=14)
plt.ylabel('Sensitivity of $\\kappa_r$ (radians)', fontsize=14)
plt.title('Sensitivity of $\\kappa_r$ at 1 MHz as a Function of Offset', fontsize=16)
plt.grid(True)

# Adjust tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Display plot
plt.savefig("sensitivity_v_offset_kappa_r")
plt.show()

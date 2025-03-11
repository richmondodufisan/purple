import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response

exp_range = np.arange(-1, 2.3, 0.05)  # range of exponents as in experiments
freq_range = (10**exp_range)  # frequency range in MHz

# Thermal Properties to check sensitivity of:
G_val = 30 * 1e6  # interface conductance
kappa_iso_val = 130  # isotropic thermal conductivity


def FDTR_function(freqs, kappa_iso, G):

    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, kappa_iso, kappa_iso, 2329, 689.1]
        layer1 = [90e-9, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [G]
        w_probe = 1.34e-6
        w_pump = 1.53e-6
        pump_power = 0.01
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, freq, pump_power)
        
        # phase = phase * (180/np.pi)   # Toggle to plot sensitivity in degrees instead of radian
        phases.append(phase)
    
    return np.array(phases)


def finite_difference_log(FDTR_function, freq_range, param_name, param_value, perturbation, kwargs):

    # Computes sensitivity using finite difference with log-scaled perturbations.
    # The sensitivity is defined as d/d(log x) of the phase
    # Where x is the parameter investigated
    
    # Parameters:
        # FDTR_function : function - The function to evaluate.
        # freq_range : array - Frequency range for calculations.
        # param_name : str - The parameter to perturb.
        # param_value : float - The base value of the parameter.
        # perturbation : float - The percentage change (e.g., 0.1 for ±10%).
        # kwargs : dict - Dictionary of additional parameters for FDTR_function.

    # Returns:
        # Sensitivity (array) : d(phase) / d(log param)


    # TWO POINT CENTRAL DIFFERENCING
    # (f(x + h) - f(x - h))/2h
    # Perturbed values
    # param_low = param_value * (1 - perturbation)
    # param_high = param_value * (1 + perturbation)

    # # Create modified copies of kwargs for each perturbation
    # kwargs_low = kwargs.copy()
    # kwargs_high = kwargs.copy()
    
    # # Replace the parameter to be investigated (ONLY) by perturbed versions
    # kwargs_low[param_name] = param_low
    # kwargs_high[param_name] = param_high

    # # Compute phases at perturbed values
    # phase_low = FDTR_function(freq_range, **kwargs_low)
    # phase_high = FDTR_function(freq_range, **kwargs_high)

    # # Compute derivative with respect to log(parameter), central differencing
    # sensitivity = (phase_high - phase_low) / (np.log(param_high) - np.log(param_low))
    
    
    
    # FOUR POINT CENTRAL DIFFERENCING
    # (-f(x + 2h) + 8f(x + h) - 8f(x - h) + f(x - 2h))/12h
    # Define more perturbation points 
    param_2low = param_value * (1 - 2 * perturbation)  
    param_1low = param_value * (1 - perturbation)     
    param_1high = param_value * (1 + perturbation)     
    param_2high = param_value * (1 + 2 * perturbation) 

    # Create modified copies of kwargs for each perturbation
    kwargs_2low = kwargs.copy()
    kwargs_1low = kwargs.copy()
    kwargs_1high = kwargs.copy()
    kwargs_2high = kwargs.copy()

    # Assign perturbed values
    kwargs_2low[param_name] = param_2low
    kwargs_1low[param_name] = param_1low
    kwargs_1high[param_name] = param_1high
    kwargs_2high[param_name] = param_2high

    # Compute phases at perturbed values
    phase_2low = FDTR_function(freq_range, **kwargs_2low)
    phase_1low = FDTR_function(freq_range, **kwargs_1low)
    phase_1high = FDTR_function(freq_range, **kwargs_1high)
    phase_2high = FDTR_function(freq_range, **kwargs_2high)

    # Compute log differences
    log_2low = np.log(param_2low)
    log_1low = np.log(param_1low)
    log_1high = np.log(param_1high)
    log_2high = np.log(param_2high)

    # Compute derivative with respect to log(parameter), central differencing
    sensitivity = (-phase_2high + 8*phase_1high - 8*phase_1low + phase_2low) / (6 * (log_1high - log_1low))

    
    
    return sensitivity


# Define common parameters in a dictionary
# Name in quotes is the name in FDTR_function
# The dictionary binds the name in quotes to the values defined at the top of the code

params = {"kappa_iso": kappa_iso_val, "G": G_val}


# Compute sensitivities
# Input arguments: FDTR_function, frequency range, param name (in FDTR Function), param value, perturbation amount, dictionary of params

perturbation = 0.0005

Sensitivity_G = finite_difference_log(FDTR_function, freq_range, "G", G_val, perturbation, params)

Sensitivity_kappa = finite_difference_log(FDTR_function, freq_range, "kappa_iso", kappa_iso_val, perturbation, params)






# Make the sensitivity plot
plt.figure(figsize=(10, 6))
plt.plot(freq_range, Sensitivity_G, label=r'$G (Au-Si)$', linestyle='--', linewidth=3)  
plt.plot(freq_range, Sensitivity_kappa, label=r'$\kappa$ (isotropic, Si)', linestyle='--', linewidth=3) 
plt.xscale('log')
plt.grid(True)

# Adjust font size for axis labels and ticks
plt.xlabel('Frequency (MHz)', fontsize=14)
plt.ylabel('Sensitivity (radians)', fontsize=14)

# Adjust tick label font size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Set title and legend font size
plt.title('Sensitivity Plot for 90nm Au on Si', fontsize=16)
plt.legend(fontsize=14)

# Display and save plot
plt.savefig('sensitivity_isotropic.png')
plt.show()

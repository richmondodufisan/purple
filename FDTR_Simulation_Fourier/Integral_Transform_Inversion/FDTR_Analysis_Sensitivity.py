import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
import pdb
import csv
import math

exp_range = np.arange(-1, 2.2, 0.05) # range of exponents as in experiments

freq_range = (10**exp_range) # frequency range in MHz

# Thermal Properties to check sensitivity of:
G = 30 * 10e6      # interface conductance
kappa_iso = 130     # isotropic thermal conductivity


def FDTR_function(freqs, kappa_iso, G):
    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, kappa_iso, kappa_iso, 2329, 689.1]
        layer1 = [90e-9, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [G]
        r_probe = 1.34e-6
        r_pump = 1.53e-6
        pump_power = 0.01
        calib_consts = [1, 1] # no calibration
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        
        # phase = phase * (180/np.pi)   # Toggle to plot sensitivity in degrees instead of radians
        phases.append(phase)
        
    return np.array(phases)
    
    
# Calculate conductance sensitivity

phase_G_1 = FDTR_function(freq_range, kappa_iso, G*0.9)
phase_G_2 = FDTR_function(freq_range, kappa_iso, G*1.1)

Sensitivity_G = (phase_G_2 - phase_G_1)/(np.log(G * 1.1) - np.log(G * 0.9))

# Calculate isotropic kappa sensitivity

phase_kappa_1 = FDTR_function(freq_range, kappa_iso*0.9, G)
phase_kappa_2 = FDTR_function(freq_range, kappa_iso*1.1, G)

Sensitivity_kappa = (phase_kappa_2 - phase_kappa_1)/(np.log(kappa_iso * 1.1) - np.log(kappa_iso * 0.9))




# Make the sensitivity plot
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(freq_range, Sensitivity_G, label=r'$G_{Au-Si}$', linestyle='--')
plt.plot(freq_range, Sensitivity_kappa, label=r'$\kappa_{Si}$ (isotropic)', linestyle='--')
plt.xscale('log')
plt.grid('True')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Sensitivity (radians)')
plt.title('Sensitivity Plot for 90nm Au on Si')
plt.legend()
plt.show()


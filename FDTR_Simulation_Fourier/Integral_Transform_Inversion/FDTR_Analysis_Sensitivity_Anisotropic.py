import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction_BesselRing import calc_thermal_response
# from Layered_Heat_Conduction import calc_thermal_response
import pdb
import csv
import math

exp_range = np.arange(-1, 2.3, 0.05) # range of exponents as in experiments

freq_range = (10**exp_range) # frequency range in MHz

# Thermal Properties to check sensitivity of:
G = 30 * 10e6       # interface conductance
kappa_r = 130       # thermal conductivity r
kappa_z = 130       # thermal conductivity z


def FDTR_function(freqs, kappa_z, kappa_r, G):
    phases = []

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [40e-6, kappa_z, kappa_r, 2329, 689.1]
        layer1 = [90e-9, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [G]
        w_probe = 1.34e-6
        w_pump = 1.53e-6
        pump_power = 0.01
        freq = freq * 1e6
        
        offset = 7e-6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, freq, pump_power)
        # phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, freq, pump_power)
        
        # phase = phase * (180/np.pi)   # Toggle to plot sensitivity in degrees instead of radians
        phases.append(phase)
        
    return np.array(phases)
    
    
# Calculate conductance sensitivity
factor1 = 0.9
factor2 = 1.1


phase_G_1 = FDTR_function(freq_range, kappa_z, kappa_r, G*factor1)
phase_G_2 = FDTR_function(freq_range, kappa_z, kappa_r, G*factor2)

Sensitivity_G = (phase_G_2 - phase_G_1)/(np.log(G * factor2) - np.log(G * factor1))

# Calculate z kappa sensitivity

phase_kappa_z_1 = FDTR_function(freq_range, kappa_z*factor1, kappa_r, G)
phase_kappa_z_2 = FDTR_function(freq_range, kappa_z*factor2, kappa_r, G)

Sensitivity_kappa_z = (phase_kappa_z_2 - phase_kappa_z_1)/(np.log(kappa_z * factor2) - np.log(kappa_z * factor1))

# Calculate r kappa sensitivity

phase_kappa_r_1 = FDTR_function(freq_range, kappa_z, kappa_r*factor1, G)
phase_kappa_r_2 = FDTR_function(freq_range, kappa_z, kappa_r*factor2, G)

Sensitivity_kappa_r = (phase_kappa_r_2 - phase_kappa_r_1)/(np.log(kappa_r * factor2) - np.log(kappa_r * factor1))





# Make the sensitivity plot
plt.figure(figsize=(10, 6))
plt.plot(freq_range, Sensitivity_G, label=r'$G (Au-Si)$', linestyle='--', linewidth=3)  
plt.plot(freq_range, Sensitivity_kappa_r, label=r'$\kappa_{r}$ (Si)', linestyle='--', linewidth=3)
plt.plot(freq_range, Sensitivity_kappa_z, label=r'$\kappa_{z}$ (Si)', linestyle='--', linewidth=3)   
plt.xscale('log')
plt.grid(True)

# Adjust font size for axis labels and ticks
plt.xlabel('Frequency (MHz)', fontsize=14)
plt.ylabel('Sensitivity (radians)', fontsize=14)

# Adjust tick label font size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Set title and legend font size
plt.title('Sensitivity Plot for 90nm Au on Si, 7 micron offset', fontsize=16)
# plt.title('Sensitivity Plot for 90nm Au on Si, concentric beams', fontsize=16)
plt.legend(fontsize=14)

# Display and save plot
plt.savefig('sensitivity_offset_7um.png')
# plt.savefig('sensitivity_concentric.png')
plt.show()





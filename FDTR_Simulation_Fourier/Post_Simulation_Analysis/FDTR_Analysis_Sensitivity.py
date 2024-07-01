import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
from scipy.optimize import curve_fit
from scipy.integrate import trapz
import pdb
import csv
import math
from scipy.stats import linregress

frequency = 0.01e6

# Define ranges for k_r and k_z
k_r_values = np.linspace(126, 131, 50) 
k_z_values = np.linspace(126, 131, 50)

# Create a meshgrid for k_r and k_z
k_r_grid, k_z_grid = np.meshgrid(k_r_values, k_z_values)

# Initialize the phase grid
phase_grid = np.zeros_like(k_r_grid)

# Calculate phase for each combination of k_r and k_z
for i in range(len(k_r_values)):
    for j in range(len(k_z_values)):
        k_r = k_r_grid[j, i]
        k_z = k_z_grid[j, i]
        
        N_layers = 2
        layer2 = [40e-6, k_z, k_r, 2329, 689.1]
        layer1 = [9e-8, 215, 215, 19300, 128.7]
        layer_props = np.array([layer2, layer1])
        interface_props = [3e7]
        r_probe = 1.34e-6
        r_pump = 1.53e-6
        pump_power = 0.01
        calib_consts = [1, 1] # no calibration
        freq = frequency

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        phase_grid[j, i] = phase
        


# Plotting the heatmap
plt.figure(figsize=(8, 6))
plt.contourf(k_r_grid, k_z_grid, phase_grid, cmap='viridis')
plt.colorbar(label='Phase')
plt.xlabel('k_r')
plt.ylabel('k_z')
plt.title('Phase Response Heatmap: Frequency = ' + str((frequency/1e6)) + " MHz")
plt.grid(True)
plt.show()
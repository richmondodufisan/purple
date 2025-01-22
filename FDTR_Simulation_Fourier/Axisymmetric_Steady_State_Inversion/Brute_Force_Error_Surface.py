import numpy as np
import matplotlib.pyplot as plt
from Two_Layer_Phase import calc_thermal_response

# User-provided phase (radians) and frequency (MHz)
user_phase = -0.434182916418804  # Convert degrees to radians if provided in degrees
user_frequency = 1  # MHz

# Define the parameter space
kappa_values = np.linspace(0, 10, 100)  # Discretize kappa within bounds
conductance_values = np.linspace(1e6, 50e6, 100)  # Discretize conductance within bounds

# Initialize an error array
error_surface = np.zeros((len(kappa_values), len(conductance_values)))

# Calculate phase at each grid point and compute the error
for i, kappa in enumerate(kappa_values):
    for j, conductance in enumerate(conductance_values):
        # Calculate phase at this point using the same frequency as the user-provided point
        layer2 = [40e-6, kappa, kappa, 2630, 741.79]
        layer1 = [133e-9, 194, 194, 19300, 126.4]
        layer_props = np.array([layer2, layer1])
        interface_props = [conductance]
        r_probe = 1.249e-6
        r_pump = 2.216e-6
        pump_power = 1.5
        freq = user_frequency * 1e6  # Convert to Hz
        
        # Calculate the phase using the given model
        phase, _ = calc_thermal_response(2, layer_props, interface_props, r_pump, r_probe, freq, pump_power)
        
        # Compute the error (squared difference between the calculated and user-provided phase)
        error_surface[i, j] = (phase - user_phase) ** 2

# Plot the error surface
kappa_grid, conductance_grid = np.meshgrid(kappa_values, conductance_values)
plt.figure(figsize=(10, 8))
plt.contourf(kappa_grid, conductance_grid / 1e6, error_surface.T, levels=100, cmap='viridis')
plt.colorbar(label='Error (squared)')
plt.xlabel('Thermal Conductivity, κ (W/m·K)', fontsize=12)
plt.ylabel('Interface Conductance, G (MW/m²·K)', fontsize=12)
plt.title('Error Surface for Phase Fitting', fontsize=14)
plt.show()

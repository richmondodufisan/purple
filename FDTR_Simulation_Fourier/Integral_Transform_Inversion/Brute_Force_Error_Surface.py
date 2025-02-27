import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# from Layered_Heat_Conduction_BesselRing import calc_thermal_response
from Layered_Heat_Conduction_ConcentricGaussian import calc_thermal_response






# List of user-provided phases (radians) and frequencies (MHz)

# CONCENTRIC BEAM DATA
user_phases = [-0.10596058228041347, -0.1575436103508173, -0.24010833896857903, -0.3109678805719539, -0.3749534252544176, -0.4336496677733477, -0.6670588326830659, -0.9427065152310182, -1.0917640196738556, -1.1824180944615048, -1.242205644005724]  # User-provided phases in radians
user_frequencies = [1, 2, 4, 6, 8, 10, 20, 40, 60, 80, 100]  # Corresponding frequencies in MHz


# OFFSET BEAM DATA, 3um
# user_phases = [-0.23799598070042313, -0.3191473825836547, -0.43240560230778396, -0.5238783521854586, -0.6053949444186811, -0.6799793018202053, -0.9718570417488026, -1.2764150773604046, -1.4004094375266116, -1.454875385132239, -1.4807977410339046]  # User-provided phases in radians
# user_frequencies = [1, 2, 4, 6, 8, 10, 20, 40, 60, 80, 100]  # Corresponding frequencies in MHz


# Correct solution coordinates (example values, replace with your actual values)
correct_kappa_z = 130 
correct_kappa_r = 130 


# correct_conductance = 30e6






# Ensure that the number of phases matches the number of frequencies
assert len(user_phases) == len(user_frequencies), "Phases and frequencies must have the same length."

# Define the parameter space
kappa_z_values = np.linspace(100, 150, 30)  # Discretize kappa_z within bounds
kappa_r_values = np.linspace(100, 150, 30)  # Discretize kappa_r within bounds

# conductance_values = np.linspace(1e6, 59e6, 100)  # Discretize conductance within bounds

# Initialize the cumulative error array
error_surface = np.zeros((len(kappa_z_values), len(kappa_r_values)))





# Loop over each phase and frequency
for user_phase, user_frequency in zip(user_phases, user_frequencies):

    # Calculate phase at each grid point and compute the error for this frequency/phase pair
    for i, kappa_z in enumerate(kappa_z_values):
    
    
        for j, kappa_r in enumerate(kappa_r_values):
        
            # Define parameters required by calc_thermal_response function
            
            N_layers = 2
            layer2 = [40e-6, kappa_z, kappa_r, 2329, 689.1]
            layer1 = [9e-8, 215, 215, 19300, 128.7]
            layer_props = np.array([layer2, layer1])
            interface_props = [30e6]
            w_probe = 1.34e-6
            w_pump = 1.53e-6
            pump_power = 0.01
            offset = 3e-6
            freq = user_frequency * 1e6
            

            # Calculate the phase using the provided model
            phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, freq, pump_power)
            
            # phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, freq, pump_power)



            # Compute the error (squared difference between the calculated and user-provided phase)
            error_surface[i, j] += (phase - user_phase) ** 2  # Accumulate the error for this phase/frequency pair






# Plot the cumulative error surface as a 2D contour plot
kappa_z_grid, kappa_r_grid = np.meshgrid(kappa_z_values, kappa_r_values)

plt.figure(figsize=(10, 8))
plt.contourf(kappa_z_grid, kappa_r_grid, error_surface.T, levels=500, cmap='viridis')
plt.colorbar(label='Cumulative Error (MSE)')
plt.xlabel('Cross-Plane Thermal Conductivity, κ_z (W/m·K)', fontsize=12)
plt.ylabel('In-Plane Thermal Conductivity, κ_r (MW/m²·K)', fontsize=12)
plt.title('Cumulative Error Surface for Phase Fitting (2D)', fontsize=14)

# Add red "X" to mark the correct solution
plt.scatter(correct_kappa_z, correct_kappa_r, color='red', marker='x', s=100, label='Correct Solution')

# Show the legend
plt.legend()


plt.savefig('cumulative_error_plot_2D_Concentric.png')
# plt.savefig('cumulative_error_plot_2D_BesselRing_3um.png')
plt.show()




# Save error data to Excel
error_df = pd.DataFrame(error_surface, index=kappa_z_values, columns=kappa_r_values)
# error_df.to_excel("error_surface_data_bessel_3um.xlsx", sheet_name="Error Data")
error_df.to_excel("error_surface_data_concentric.xlsx", sheet_name="Error Data")

# Save kappa values to Excel
kappa_df = pd.DataFrame({"kappa_z": kappa_z_values, "kappa_r": kappa_r_values})
# kappa_df.to_excel("kappa_values_bessel_3um.xlsx", sheet_name="Kappa Values", index=False)
kappa_df.to_excel("kappa_values_concentric.xlsx", sheet_name="Kappa Values", index=False)















# # 3D Plot of the cumulative error surface
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111, projection='3d')

# # Plot the 3D surface
# surf = ax.plot_surface(kappa_grid, conductance_grid / 1e6, error_surface.T, cmap='viridis', edgecolor='none')

# # Add labels and title
# ax.set_xlabel('Thermal Conductivity, κ (W/m·K)', fontsize=12)
# ax.set_ylabel('Interface Conductance, G (MW/m²·K)', fontsize=12)
# ax.set_zlabel('Cumulative Error (MSE)', fontsize=12)
# ax.set_title('Cumulative Error Surface for Phase Fitting (3D)', fontsize=14)

# # Add a color bar
# fig.colorbar(surf, shrink=0.5, aspect=5)

# plt.savefig('cumulative_error_plot_3D_6_frequencies.png')
# plt.show()

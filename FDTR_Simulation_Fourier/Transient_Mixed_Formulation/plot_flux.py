import pandas as pd
import matplotlib.pyplot as plt

# File names for flux and temperature
flux_files = ['FDTR_input_Fourier_Mixed_theta_0_freq_1e6_x0_-1_v1_out_flux_x_profile_surface_0012.csv', 'FDTR_input_Fourier_Mixed_theta_0_freq_1e6_x0_-1_v1_out_flux_y_profile_surface_0012.csv', 'FDTR_input_Fourier_Mixed_theta_0_freq_1e6_x0_-1_v1_out_flux_z_profile_surface_0012.csv']
labels = ['X Component', 'Y Component', 'Z Component']
temperature_file = 'FDTR_input_Fourier_Mixed_theta_0_freq_1e6_x0_-1_v1_out_temperature_profile_surface_0012.csv'

# Create a figure with 4 subplots (3 for flux components, 1 for temperature)
fig, axs = plt.subplots(4, 1, figsize=(10, 16))

for i, file in enumerate(flux_files):
    # Read the CSV file for flux components
    data = pd.read_csv(file)
    
    # Extract the relevant columns
    x = data.iloc[:, 2]
    flux = data.iloc[:, 1]
    
    # Plot the flux data
    axs[i].plot(x, flux)
    axs[i].set_title(f'Flux vs. Location - {labels[i]}')
    axs[i].set_xlabel('Location (x-axis)')
    axs[i].set_ylabel(f'Flux {labels[i]}')

# Read the temperature data from the temperature file
temp_data = pd.read_csv(temperature_file)

# Extract location (x-axis) and temperature
x_temp = temp_data.iloc[:, 2]
temperature = temp_data.iloc[:, 1]

# Plot the temperature data
axs[3].plot(x_temp, temperature, color='red')
axs[3].set_title('Temperature vs. Location')
axs[3].set_xlabel('Location (x-axis)')
axs[3].set_ylabel('Temperature')

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

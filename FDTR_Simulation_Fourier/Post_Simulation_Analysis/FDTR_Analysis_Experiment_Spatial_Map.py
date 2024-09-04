import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from Layered_Heat_Conduction import calc_thermal_response

############################################################# USER-DEFINED PARAMETERS #########################################################################################

# This code is used to generate thermal maps from phase data
# It is assumed that the phase data is saved as .txt files of the format Phase_1MHz.txt, Phase_2MHz.txt, Phase_0p5MHz.txt, etc
# It is also assumed that the phase values are in degrees
# In this section, you define the length and breadth of the map, and the number of steps in each direction

# Define map size and resolution parameters
length_x = 100
length_y = 18
steps_x = 33
steps_y = 6

# Directory where phase data files are stored
data_directory = "./Map_Test/"  # User should update this to the actual directory

# Expected phase data files
phase_range = ["0p5MHz", "1MHz", "2MHz", "4MHz"]
frequencies = [0.5e6, 1e6, 2e6, 4e6]  # Corresponding frequency values, write the numerical values


# Define material regions, with an array of material properties for each region
# This section is necessary since sometimes, the investigated area contains more than one type of material
# Here you can define regions (which MUST be rectangular in shape) and define their corresponding material properties
# In this case, we have defined 5 material properties (constants)
# In this case, they are arranged as in this order: kappa_1, rho_1, c_1, rho_2, c_2
# You can define however many/little as you like, but when changing the size of the array, update "fit_function_FDTR" in the function definitions section

regions = [
    {"x_range": (0, 100), "y_range": (0, 9), "material_properties": [194, 19300, 126.4, 2630, 741.79]},
    {"x_range": (0, 100), "y_range": (9, 18), "material_properties": [194, 19300, 126.4, 2630, 741.79]},
    # Add more regions as needed
]


############################################################# END USER-DEFINED PARAMETERS #########################################################################################












############################################################# FUNCTION DEFINITIONS #########################################################################################

# Define a function to determine which region the current position belongs to
def get_material_properties(i, j, regions):
    for region in regions:
        x_range, y_range = region["x_range"], region["y_range"]
        if x_range[0] <= j < x_range[1] and y_range[0] <= i < y_range[1]:
            return region["material_properties"]
    return None  # If no region is found (shouldn't happen if regions cover all areas)   
    

# This is the most important function of this code
# It defines the material properties to be fit, and the ones that remain constant
# Please see the "Layered_Heat_Conduction" file for an explanation on how each row is arranged and passed to calc_thermal_response

# MATERIAL PROPERTIES
# These are properties that remain constant over a spatial domain
# They are not fitted by the optimization code
# Define the material property array in the USER-DEFINED PARAMETERS section, and then come here to place them in their corresponding position
# For example, if you were not fitting kappa_2 and wanted to add it to the (constant) material properties, 
# you would adjust the number of properties provided in the USER-DEFINED PARAMETERS section, and come here to adjust:
# kappa_1, rho_1, c_1, kappa_2, rho_2, c_2 = material_properties


# FITTING PROPERTIES
# In this case, we are fitting 2 material properties, kappa_2, and the interface conductance for a 2-layer system
# If you need to change the number of properties being fit at a time, then you need to adjust the following:

# Bounds & Initial Guesses for the fitting (under FITTING ACTUAL DATA section)
# Size of Fitting Map Array (under FITTING ACTUAL DATA section)
# fit_function_FDTR (right here, under FUNCTION DEFINITIONS)
# plotting results (under GENERATING HEAT MAPS)

# I have also added the comment "CHANGE IF CHANGING FITTING PROPERTIES" to each of those locations to make them searchable

def fit_function_FDTR(freqs, fitting_properties, material_properties):
    phases = []

    kappa_2, conductance_12 = fitting_properties
    kappa_1, rho_1, c_1, rho_2, c_2 = material_properties

    for freq in freqs:
        # Define other parameters required by calc_thermal_response function
        N_layers = 2
        layer2 = [100e-6, kappa_2, kappa_2, rho_2, c_2]
        layer1 = [133e-9, kappa_1, kappa_1, rho_1, c_1]
        layer_props = np.array([layer2, layer1])
        interface_props = [conductance_12]
        r_probe = 1.249e-6
        r_pump = 2.216e-6
        pump_power = 1.5
        calib_consts = [1, 1] # no calibration
        freq = freq * 1e6

        # Calculate analytical phase 
        phase, _ = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)
        phases.append(phase)
        
    return np.array(phases)

# Function to read phase data from text files and convert degrees to radians
def read_phase_data(file_name):
    data = np.loadtxt(file_name)
    data = np.radians(data)  # Convert phase data from degrees to radians
    return data

############################################################# END FUNCTION DEFINITIONS #########################################################################################










############################################################# FITTING ACTUAL DATA #########################################################################################

# Store fitting results
# CHANGE IF CHANGING FITTING PROPERTIES
fitting_map = np.zeros((steps_y, steps_x, 2))  # Assuming we're fitting 2 properties (kappa_2, conductance_12). if more, simply change number

# Perform fitting at each position
for i in range(steps_y):
    for j in range(steps_x):
        # Get the material properties for the current position (i, j)
        material_properties = get_material_properties(i, j, regions)
        if material_properties is None:
            print(f"No material properties found for position ({i}, {j})")
            continue
        
        # Collect phase data for the current position (i, j) across all frequencies
        phase_data = []
        for phase in phase_range:
            file_name = os.path.join(data_directory, f"Phase_{phase}.txt")
            data = read_phase_data(file_name)
            phase_data.append(data[i, j])  # Extract phase for current position

        # Convert to a pandas DataFrame for easier processing
        FDTR_data = pd.DataFrame({
            'frequency': frequencies,
            'phase': phase_data
        })

        # Define initial guesses and bounds for fitting properties
        # CHANGE IF CHANGING FITTING PROPERTIES
        initial_guesses = [3, 40e6]  # Initial guesses for kappa_2 and conductance_12 (you can extend this list)
        bounds_lower = [0, 10e6]     # Lower bounds for the fitting properties
        bounds_upper = [300, 500e6]  # Upper bounds for the fitting properties
        
        # NB: use one initial guess/bounds for all regions, it'll find the correct value eventually


        # Define a wrapper function that passes both fitting properties and material properties
        def fit_wrapper(freqs, *fitting_properties):
            return fit_function_FDTR(freqs, fitting_properties, material_properties)

        # Fit the data to get the fitting properties
        try:
            popt, pcov = curve_fit(
                fit_wrapper,
                FDTR_data['frequency'],   # Frequency data
                FDTR_data['phase'],       # Phase data
                p0=initial_guesses,       # Initial guesses for the fitting properties
                bounds=(bounds_lower, bounds_upper),  # Bounds for the parameters
                method='trf',             # Trust Region Reflective algorithm
                maxfev=10000,             # Maximum function evaluations
                ftol=1e-12,
                xtol=1e-12,
                gtol=1e-12
            )

            fitting_map[i, j] = popt  # Store the fitted parameters (k_Si, conductance)

        except Exception as e:
            print(f"Fitting failed at position ({i}, {j}): {e}")
            fitting_map[i, j] = np.nan

############################################################# END FITTING ACTUAL DATA #########################################################################################








############################################################# GENERATING HEAT MAPS #########################################################################################

# Generate heatmaps for each fitting property
plt.figure(figsize=(12, 6))

# CHANGE IF CHANGING FITTING PROPERTIES
# i.e add or remove another map

# Plot kappa (fitting_properties[0]) map
plt.subplot(1, 2, 1)
plt.imshow(fitting_map[:, :, 0], cmap='hot', extent=[0, length_x, 0, length_y])
plt.colorbar(label='Thermal Conductivity (Si)')
plt.title('Thermal Conductivity Map (Si)')
plt.xlabel('X position')
plt.ylabel('Y position')

# Plot conductance (fitting_properties[1]) map
plt.subplot(1, 2, 2)
plt.imshow(fitting_map[:, :, 1], cmap='hot', extent=[0, length_x, 0, length_y])
plt.colorbar(label='Interface (1-2) Conductance')
plt.title('Interface (1-2) Conductance Map')
plt.xlabel('X position')
plt.ylabel('Y position')

plt.tight_layout()

save_path = f'{data_directory}.png'
plt.savefig(save_path)

plt.show()

############################################################# END GENERATING HEAT MAPS #########################################################################################
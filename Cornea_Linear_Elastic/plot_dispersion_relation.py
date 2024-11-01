import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks
import os
import glob
from Analytical_Antisymmetric_RL_RealOnly import calc_dispersion_relation_asym
from Analytical_Symmetric_RL_RealOnly import calc_dispersion_relation_sym

# Define your excitation frequencies
excitation_frequencies = ["1e3", "1.5e3", "2e3", "2.5e3", "3e3", "3.5e3", "4e3", "4.5e3", "5e3", "5.5e3", "6e3", 
                          "6.5e3", "7e3", "7.5e3", "8e3", "8.5e3", "9e3", "9.5e3", "10e3", "10.5e3", "11e3", 
                          "11.5e3", "12e3", "12.5e3", "13e3", "13.5e3", "14e3", "14.5e3", "15e3", "15.5e3", 
                          "16e3", "16.5e3", "17e3", "17.5e3", "18e3", "18.5e3", "19e3", "19.5e3", "20e3"]  # Frequencies as strings for filename matching
file_template = './Validated_Data/Plate_Harmonic_Perturbation_freq_{freq}_out_wave_profile_*.csv'

# Material and physical properties
thickness = 0.001
density = 1000
poissons_ratio = 0.49
shear_modulus = 100000
freq_min = 1000
freq_max = 20000
num_points = 50

# Function to process each file and calculate wave speeds
def process_file(file_path, excitation_frequency):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract columns
    y_displacement = data.iloc[:, 0].values
    x_position = data.iloc[:, 2].values

    # Compute the Fourier Transform of y displacement
    N = len(y_displacement)
    y_displacement_fft = fft(y_displacement)
    frequencies = fftfreq(N, x_position[1] - x_position[0])

    # Take only the positive half of the frequencies and corresponding FFT results
    frequencies_positive = frequencies[:N//2]
    fft_magnitude = np.abs(y_displacement_fft[:N//2])

    # Scale FFT magnitudes by maximum peak
    fft_magnitude_normalized = fft_magnitude / np.max(fft_magnitude)

    # Find peaks with magnitude > 0.5 (these are spatial frequencies, the cycles per unit distance (1 meter) i.e k = wave number)
    peaks, _ = find_peaks(fft_magnitude_normalized, height=0.2)

    # Calculate wave speeds for peaks
    wave_speeds = []
    excitation_frequency_value = float(excitation_frequency)
    for peak in peaks:
        peak_frequency = frequencies_positive[peak]
        wave_speed = excitation_frequency_value / peak_frequency
        wave_speeds.append(wave_speed)

    return wave_speeds, frequencies_positive[peaks]

# Function to find the latest file based on excitation frequency
def find_latest_file(excitation_frequency):
    search_pattern = file_template.format(freq=excitation_frequency)
    files = glob.glob(search_pattern)

    if not files:
        return None  # Return None if no files are found

    # Extract the wave profile number from the filenames
    def extract_wave_profile(file_name):
        base_name = os.path.basename(file_name)
        number_str = base_name.split('_wave_profile_')[-1].split('.')[0]
        return int(number_str)  # Convert to int for numerical comparison

    # Find the file with the largest wave profile number
    latest_file = max(files, key=lambda f: extract_wave_profile(f))
    return latest_file

# Prepare a figure for plotting
plt.figure(figsize=(10, 6))

# Initialize a variable to track if the label has been added
label_added = False

# Plot numerical dispersion relation points in a single color
for excitation_frequency in excitation_frequencies:
    # Find the latest file for the given excitation frequency
    file_path = find_latest_file(excitation_frequency)

    # Check if the file was found before proceeding
    if not file_path:
        print(f"No file found for frequency {excitation_frequency} Hz")
        continue

    # Process the file and calculate wave speeds for peaks above threshold
    wave_speeds, _ = process_file(file_path, excitation_frequency)

    # Set label only once
    label = "Numerical - FEM" if not label_added else None
    label_added = True  # Mark that the label has been added

    # Plot each wave speed point in the same color
    excitation_frequency = float(excitation_frequency)
    plt.scatter([excitation_frequency] * len(wave_speeds), wave_speeds, color='blue', marker='o', s=30, label=label)

# Plot analytical dispersion relation for the antisymmetric modes
frequencies_analytical_asym, phase_velocities_analytical_asym = calc_dispersion_relation_asym(
    thickness, density, poissons_ratio, shear_modulus, freq_min, freq_max, num_points
)
plt.scatter(np.array(frequencies_analytical_asym), phase_velocities_analytical_asym, color='red', marker='^', s=15, label="Analytical - Antisymmetric")


# Plot analytical dispersion relation for the symmetric modes
# frequencies_analytical_sym, phase_velocities_analytical_sym = calc_dispersion_relation_sym(
    # thickness, density, poissons_ratio, shear_modulus, freq_min, freq_max, num_points
# )
# plt.scatter(np.array(frequencies_analytical_sym), phase_velocities_analytical_sym, color='green', marker='^', s=10, label="Analytical - Symmetric")



# Plot customization
plt.xlabel('Excitation Frequency (Hz)')
plt.ylabel('Wave Speed (m/s)')
plt.title('Dispersion Relation: Frequency vs. Phase Velocity')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('linear_elastic_dispersion_relation.png')
plt.show()

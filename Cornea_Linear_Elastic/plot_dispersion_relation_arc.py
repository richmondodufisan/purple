import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks
import os
import glob

# Define your excitation frequencies
excitation_frequencies = ["1e6", "1.5e6", "2e6", "2.5e6", "3e6", "3.5e6", "4e6", "4.5e6", "5e6", "5.5e6", "6e6", 
                          "6.5e6", "7e6", "7.5e6", "8e6", "8.5e6", "9e6", "9.5e6", "10e6", "10.5e6", "11e6", 
                          "11.5e6", "12e6", "12.5e6", "13e6", "13.5e6", "14e6", "14.5e6", "15e6", "15.5e6", 
                          "16e6", "16.5e6", "17e6", "17.5e6", "18e6", "18.5e6", "19e6", "19.5e6", "20e6"]

file_template = './Cornea_Harmonic_Perturbation_2D_Axisymmetric_freq_{freq}_out_upper_right_z_disp_*.csv'

# Function to process each file and calculate wave speeds
def process_file(file_path, excitation_frequency):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract columns
    z_displacement = data.iloc[:, 0].values
    x_position = data.iloc[:, 2].values
    y_position = data.iloc[:, 3].values

    # Define the radius of the semicircle
    R = 0.025  

    # Define the reference point (top of the semicircle)
    x_ref, y_ref = 0, 0.025

    # Compute vectors
    v1 = np.array([x_ref, y_ref])  # Reference vector (to topmost point)
    v2 = np.column_stack((x_position, y_position))  # Vectors to each point

    # Compute dot product
    dot_product = np.sum(v1 * v2, axis=1)

    # Compute magnitudes
    v1_mag = np.linalg.norm(v1)
    v2_mag = np.linalg.norm(v2, axis=1)

    # Compute theta
    theta = np.arccos(dot_product / (v1_mag * v2_mag))

    # Compute arc length
    arc_length = R * theta  

    # Compute the Fourier Transform of z displacement
    N = len(z_displacement)
    z_displacement_fft = fft(z_displacement)
    frequencies = fftfreq(N, arc_length[1] - arc_length[0])  # Assuming uniform spacing in arc length

    # Take only the positive half of the frequencies and corresponding FFT results
    frequencies_positive = frequencies[:N//2]
    fft_magnitude = np.abs(z_displacement_fft[:N//2])

    # Scale FFT magnitudes by maximum peak
    fft_magnitude_normalized = fft_magnitude / np.max(fft_magnitude)

    # Find peaks with magnitude > 0.2 (these are spatial frequencies, the cycles per unit arc length)
    peaks, _ = find_peaks(fft_magnitude_normalized, height=0.8)

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
        number_str = base_name.split('_upper_right_z_disp_')[-1].split('.')[0]
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

# Plot customization
plt.xlabel('Excitation Frequency (Hz)')
plt.ylabel('Wave Speed (m/s)')
plt.title('Dispersion Relation: Frequency vs. Phase Velocity')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('linear_elastic_dispersion_relation.png')
plt.show()

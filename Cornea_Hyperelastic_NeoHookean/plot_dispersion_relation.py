import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks
import os

# Define your excitation frequencies and stretch ratios
excitation_frequencies = ['1e3', '10e3']  # Excitation frequencies as strings, so they match the file name exactly
stretches = [1.1]  # Example stretch ratios

# Set your file template
file_template = 'Part2_Harmonic_freq_{freq}_stretch_{stretch}_out_wave_profile_0005.csv'







# Function to process each file and calculate wave speeds
def process_file(file_path, excitation_frequency):
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Extract columns
    y_displacement = data.iloc[:, 0].values  # Convert to NumPy array
    x_position = data.iloc[:, 2].values     # Convert to NumPy array

    # Compute the Fourier Transform of y displacement
    N = len(y_displacement)
    y_displacement_fft = fft(y_displacement)
    frequencies = fftfreq(N, x_position[1] - x_position[0])  # Assuming uniform spacing in x_position

    # Take only the positive half of the frequencies and corresponding FFT results
    frequencies_positive = frequencies[:N//2]
    fft_magnitude = np.abs(y_displacement_fft[:N//2])

    # Find the peaks in the FFT magnitude
    magnitude_threshold = 0.00005 #height threshold for peaks
    peaks, _ = find_peaks(fft_magnitude, height=magnitude_threshold) 

    # Calculate wave speeds as excitation_frequency/peak_frequency for each peak
    wave_speeds = []
    excitation_frequency_value = float(excitation_frequency)  # Convert excitation frequency to a numeric value
    for peak in peaks:
        peak_frequency = frequencies_positive[peak]
        wave_speed = excitation_frequency_value / peak_frequency
        wave_speeds.append(wave_speed)

    return wave_speeds, frequencies_positive[peaks]








# Loop over each stretch ratio
for stretch in stretches:
    # Prepare a figure for the current stretch ratio
    plt.figure(figsize=(10, 6))
    
    # Loop over each excitation frequency
    for excitation_frequency in excitation_frequencies:
        # Format the file name based on the current stretch and excitation frequency (use the string as is)
        file_path = file_template.format(freq=excitation_frequency, stretch=f"{stretch:.1f}")
        
        # Check if the file exists before proceeding
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        # Process the file and calculate wave speeds
        wave_speeds, peak_frequencies = process_file(file_path, excitation_frequency)
        
        # Scatter plot of excitation frequency vs wave speed
        plt.scatter([float(excitation_frequency.replace('e3', 'e+03'))] * len(wave_speeds), wave_speeds, label=f"{excitation_frequency} Hz")

    # Plot customization
    plt.xlabel('Excitation Frequency (Hz)')
    plt.ylabel('Wave Speed (m/s)')
    plt.title(f'Dispersion Relation (Stretch = {stretch})')
    plt.grid(True)
    # plt.legend()
    plt.savefig(f'dispersion_relation_stretch_{stretch}.png')
    plt.show()
    

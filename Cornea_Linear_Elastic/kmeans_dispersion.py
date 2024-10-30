import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks
import os
import glob
from sklearn.cluster import KMeans

# Define your excitation frequencies
excitation_frequencies = ["1e3", "1.5e3", "2e3", "2.5e3", "3e3", "3.5e3", "4e3", "4.5e3", "5e3", 
                          "5.5e3", "6e3", "6.5e3", "7e3", "7.5e3", "8e3", "8.5e3", "9e3", "9.5e3", 
                          "10e3", "10.5e3", "11e3", "11.5e3", "12e3", "12.5e3", "13e3", "13.5e3", 
                          "14e3", "14.5e3", "15e3", "15.5e3", "16e3", "16.5e3", "17e3", "17.5e3", 
                          "18e3", "18.5e3", "19e3", "19.5e3", "20e3"] # Frequencies as strings for filename matching
file_template = 'Plate_Harmonic_Perturbation_freq_{freq}_out_wave_profile_*.csv'

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

    # Find peaks with magnitude > 0.5
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

# Collect all wave speeds and peak frequencies across excitation frequencies for clustering
all_wave_speeds = []
all_excitation_freqs = []

# Loop over each excitation frequency and aggregate data
for excitation_frequency in excitation_frequencies:
    file_path = find_latest_file(excitation_frequency)
    if not file_path:
        continue

    wave_speeds, peak_frequencies = process_file(file_path, excitation_frequency)
    all_wave_speeds.extend(wave_speeds)
    all_excitation_freqs.extend([float(excitation_frequency.replace('e3', 'e+03'))] * len(wave_speeds))

# Apply clustering to sort branches (adjust 'n_clusters' based on visible branches)
wave_speed_data = np.array(list(zip(all_excitation_freqs, all_wave_speeds)))
kmeans = KMeans(n_clusters=5).fit(wave_speed_data)  # Adjust n_clusters as needed
labels = kmeans.labels_

# Plotting with clusters as branches
plt.figure(figsize=(10, 6))
for i, label in enumerate(set(labels)):
    label_indices = np.where(labels == label)
    plt.scatter(wave_speed_data[label_indices, 0], wave_speed_data[label_indices, 1], label=f'Branch {i+1}')

plt.xlabel('Excitation Frequency (Hz)')
plt.ylabel('Wave Speed (m/s)')
plt.title('Dispersion Relation Sorted by Clustering')
plt.grid(True)
plt.legend()
plt.savefig('sorted_dispersion_relation.png')
plt.show()

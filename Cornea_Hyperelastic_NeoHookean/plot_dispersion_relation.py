import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks
import os
import glob

# Define your excitation frequencies and stretch ratios

# Excitation frequencies as strings, so they match the file name exactly
# excitation_frequencies = ['1e3', '1.5e3', '2e3', '2.5e3', '3e3', '3.5e3', '4e3', '4.5e3', '5e3', '5.5e3', '6e3', '6.5e3', '7e3', '7.5e3', '8e3', '8.5e3', '9e3', '9.5e3', '10e3', '10.5e3', '11e3', '11.5e3', '12e3', '12.5e3', '13e3']
excitation_frequencies = ['1e3', '1.5e3', '2e3', '2.5e3', '3e3']


stretches = ['1']  # Stretch ratios also as strings

# Define how many top peaks you want to plot and save
n_peaks = 1 

# Set your file template
file_template = 'Part2_Harmonic_freq_{freq}_stretch_{stretch}_out_wave_profile_y_*.csv'

# Prepare a list to collect dispersion data
dispersion_data = []







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
    magnitude_threshold =0.0 #height threshold for peaks
    peaks, _ = find_peaks(fft_magnitude, height=magnitude_threshold) 

    # Sort peaks by magnitude and select the top `n_peaks`
    top_peaks = sorted(peaks, key=lambda peak: fft_magnitude[peak], reverse=True)[:n_peaks]

    # Calculate wave speeds for the selected top `n_peaks`
    wave_speeds = []
    excitation_frequency_value = float(excitation_frequency)  # Convert excitation frequency to a numeric value
    for peak in top_peaks:
        peak_frequency = frequencies_positive[peak]
        wave_speed = excitation_frequency_value / peak_frequency
        wave_speeds.append(wave_speed)

    return wave_speeds, frequencies_positive[peaks]






# Function to find the latest file based on excitation frequency and stretch ratio
def find_latest_file(excitation_frequency, stretch):
    # Use glob to find all matching files with the exact frequency and stretch formatting
    search_pattern = file_template.format(freq=excitation_frequency, stretch=stretch)
    files = glob.glob(search_pattern)

    # Debugging: Print out found files to see what's being matched
    # print(f"Searching for files with pattern: {search_pattern}")
    # print(f"Found files: {files}")

    if not files:
        return None  # Return None if no files are found

    # Extract the wave profile number from the filenames
    def extract_wave_profile(file_name):
        base_name = os.path.basename(file_name)
        # Extract the four-digit number from the pattern: wave_profile_y_XXXX.csv
        number_str = base_name.split('_wave_profile_y_')[-1].split('.')[0]
        return int(number_str)  # Convert to int for numerical comparison, but keep leading zeros in filenames

    # Find the file with the largest wave profile number
    latest_file = max(files, key=lambda f: extract_wave_profile(f))
    return latest_file









# Loop over each stretch ratio
for stretch in stretches:
    # Prepare a figure for the current stretch ratio
    plt.figure(figsize=(10, 6))

    # Initialize lists for storing wave speeds for each peak
    peak_wave_speeds = [[] for _ in range(n_peaks)]
    all_excitation_frequencies = []
    
    # Prepare a list to collect dispersion data
    dispersion_data = []

    # Loop over each excitation frequency
    for excitation_frequency in excitation_frequencies:
        # Find the latest file for the given stretch and excitation frequency
        file_path = find_latest_file(excitation_frequency, stretch)

        # Check if the file was found before proceeding
        if not file_path:
            print(f"No file found for frequency {excitation_frequency} Hz and stretch {stretch}")
            continue

        # Process the file and calculate wave speeds for the top `n_peaks`
        wave_speeds, peak_frequencies = process_file(file_path, excitation_frequency)

        # Store the excitation frequency and corresponding wave speeds
        all_excitation_frequencies.append(float(excitation_frequency.replace('e3', 'e+03')))
        
        # Store wave speeds for each peak
        for i, speed in enumerate(wave_speeds):
            peak_wave_speeds[i].append(speed)
        
        # Prepare the row of data for CSV
        row_data = [float(excitation_frequency.replace('e3', 'e+03'))] + wave_speeds
        dispersion_data.append(row_data)

    # Scatter plot each peak's wave speed in a different color
    colors = ['red', 'blue']
    
    for i in range(n_peaks):
        plt.scatter(all_excitation_frequencies, peak_wave_speeds[i], color=colors[i])

    # Plot customization
    plt.xlabel('Excitation Frequency (Hz)')
    plt.ylabel('Wave Speed (m/s)')
    plt.title(f'Dispersion Relation (Stretch = {stretch})')
    plt.grid(True)
    plt.savefig(f'dispersion_relation_stretch_{stretch}.png')
    plt.show()

    # Create a DataFrame to organize the data
    column_names = ['Excitation Frequency'] + [f'Speed {i+1}' for i in range(n_peaks)]
    df = pd.DataFrame(dispersion_data, columns=column_names)

    # Save the DataFrame to a CSV file for each stretch ratio
    df.to_csv(f'DISPERSION_DATA_{stretch}.csv', index=False)

    # Optionally, print the data to confirm
    print(df)
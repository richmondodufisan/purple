import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks

# Load the CSV file
file_path = './Free_X_Data/Plate_Harmonic_Perturbation_freq_1e3_out_wave_profile_0001.csv'  # Replace with your actual file path
# file_path = 'Plate_Harmonic_Perturbation_freq_1e3_out_wave_profile_y_0001.csv' 


data = pd.read_csv(file_path)

# Extract columns: 4th column for y displacement, 13th column for x position
y_displacement = data.iloc[:, 0].values  # Convert to NumPy array
x_position = data.iloc[:, 2].values     # Convert to NumPy array

# Plot y displacement vs x position
plt.figure(figsize=(10, 6))
plt.plot(x_position, y_displacement, label='Y Displacement vs X Position')
plt.xlabel('X Position')
plt.ylabel('Y Displacement')
plt.title('Y Displacement vs X Position')
plt.grid(True)
plt.legend()
plt.show()

# Compute the Fourier Transform of y displacement
N = len(y_displacement)
y_displacement_fft = fft(y_displacement)
frequencies = fftfreq(N, x_position[1] - x_position[0])  # Assuming uniform spacing in x_position

# Take only the positive half of the frequencies and corresponding FFT results
frequencies_positive = frequencies[:N//2]
fft_magnitude = np.abs(y_displacement_fft[:N//2])

# Scale the FFT magnitude by the maximum peak
max_peak = np.max(fft_magnitude)
fft_magnitude_normalized = fft_magnitude / max_peak  # Now the range is 0 to 1

# Find peaks above 0.5 in the normalized magnitude
peaks, _ = find_peaks(fft_magnitude_normalized, height=0.2)

# Print the frequencies corresponding to the peaks
print("Peaks found at frequencies (in units of 1/x_position):")
for peak in peaks:
    print(f"Frequency: {frequencies_positive[peak]:.4f}, Magnitude: {fft_magnitude_normalized[peak]:.4f}")

# Plot the normalized Fourier Transform (Magnitude of the Fourier coefficients)
plt.figure(figsize=(10, 6))
plt.plot(frequencies_positive, fft_magnitude_normalized, label='Normalized FFT of Y Displacement')
plt.plot(frequencies_positive[peaks], fft_magnitude_normalized[peaks], 'rx', label='Peaks > 0.5')  # Mark the peaks with red 'x'
plt.xlabel('Frequency')
plt.ylabel('Normalized Magnitude')
plt.title('Normalized Frequency Spectrum of Y Displacement with Peaks > 0.5')
plt.ylim(0, 1.1)  # Set the y-axis range to 0 to 1.1 for better visibility of the peak markers
plt.grid(True)
plt.legend()
plt.show()


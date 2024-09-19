import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks

# Load the CSV file
file_path = 'Part2_Harmonic_freq_1.5e3_stretch_1_out_wave_profile_0015.csv'  # Replace with your actual file path
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

# Find the peaks in the FFT magnitude
peaks, _ = find_peaks(fft_magnitude, height=0.001)  # You can adjust the 'height' to filter out small peaks

# Print the frequencies corresponding to the peaks
print("Peaks found at frequencies (in units of 1/x_position):")
for peak in peaks:
    print(f"Frequency: {frequencies_positive[peak]:.4f}, Magnitude: {fft_magnitude[peak]:.4f}")

# Plot the Fourier Transform (Magnitude of the Fourier coefficients)
plt.figure(figsize=(10, 6))
plt.plot(frequencies_positive, fft_magnitude, label='FFT of Y Displacement')
plt.plot(frequencies_positive[peaks], fft_magnitude[peaks], 'rx', label='Peaks')  # Mark the peaks with red 'x'
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum of Y Displacement with Peaks')
plt.grid(True)
plt.legend()
plt.show()

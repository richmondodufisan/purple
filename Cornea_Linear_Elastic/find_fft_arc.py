import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks

# Load the CSV file
file_path = 'Cornea_Harmonic_Perturbation_2D_Axisymmetric_out_upper_right_z_disp_0001.csv'  # Replace with actual path

data = pd.read_csv(file_path)

# Extract columns: 1st column for z displacement, 3rd column for x position, 4th column for y position
z_displacement = data.iloc[:, 0].values  # Convert to NumPy array
x_position = data.iloc[:, 2].values      # Convert to NumPy array
y_position = data.iloc[:, 3].values      # Convert to NumPy array

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
arc_length = R * theta  # Using R * theta formula

# Plot z displacement vs arc length
plt.figure(figsize=(10, 6))
plt.plot(arc_length, z_displacement, label='Z Displacement vs Arc Length')
plt.xlabel('Arc Length (m)')
plt.ylabel('Z Displacement')
plt.title('Z Displacement vs Arc Length')
plt.grid(True)
plt.legend()
plt.show()

# Compute the Fourier Transform of z displacement
N = len(z_displacement)
z_displacement_fft = fft(z_displacement)
frequencies = fftfreq(N, arc_length[1] - arc_length[0])  # Assuming uniform spacing in arc_length

# Take only the positive half of the frequencies and corresponding FFT results
frequencies_positive = frequencies[:N//2]
fft_magnitude = np.abs(z_displacement_fft[:N//2])

# Scale the FFT magnitude by the maximum peak
max_peak = np.max(fft_magnitude)
fft_magnitude_normalized = fft_magnitude / max_peak  # Now the range is 0 to 1

# Find peaks above 0.2 in the normalized magnitude
peaks, _ = find_peaks(fft_magnitude_normalized, height=0.5)

# Print the frequencies corresponding to the peaks
print("Peaks found at frequencies (in units of 1/arc_length):")
for peak in peaks:
    print(f"Frequency: {frequencies_positive[peak]:.4f}, Magnitude: {fft_magnitude_normalized[peak]:.4f}")

# Plot the normalized Fourier Transform (Magnitude of the Fourier coefficients)
plt.figure(figsize=(10, 6))
plt.plot(frequencies_positive, fft_magnitude_normalized, label='Normalized FFT of Z Displacement')
plt.plot(frequencies_positive[peaks], fft_magnitude_normalized[peaks], 'rx', label='Peaks > 0.5')  # Mark the peaks with red 'x'
plt.xlabel('Frequency (1/m)')
plt.ylabel('Normalized Magnitude')
plt.title('Normalized Frequency Spectrum of Z Displacement with Peaks > 0.5')
plt.ylim(0, 1.1)  # Set the y-axis range to 0 to 1.1 for better visibility of peak markers
plt.grid(True)
plt.legend()
plt.show()

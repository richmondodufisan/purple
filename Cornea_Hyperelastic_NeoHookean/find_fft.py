import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

# Load the CSV file
file_path = 'Part2_Harmonic_out_wave_profile_0002.csv'  # Replace with your actual file path
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

# Plot the Fourier Transform (Magnitude of the Fourier coefficients)
plt.figure(figsize=(10, 6))
plt.plot(frequencies[:N//2], np.abs(y_displacement_fft[:N//2]), label='FFT of Y Displacement')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum of Y Displacement')
plt.grid(True)
plt.legend()
plt.show()


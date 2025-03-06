import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path to your CSV file
file_path = 'Cornea_Harmonic_Perturbation_2D_Axisymmetric_out_upper_right_z_disp_0001.csv'

# Read the CSV file
data = pd.read_csv(file_path)

# Extract columns
z_displacement = data.iloc[:, 0]  # 1st column (z displacement)
x_position = data.iloc[:, 2]      # 3rd column (x position)
y_position = data.iloc[:, 3]      # 4th column (y position)

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

# Plot arc length vs z displacement
plt.figure(figsize=(8, 6))
plt.plot(arc_length, z_displacement, marker='o', linestyle='', color='b')

plt.xlabel('Arc Length (m)')
plt.ylabel('Z Displacement')
plt.grid(True)
plt.savefig("arc_length_vs_z_disp.png")
plt.show()

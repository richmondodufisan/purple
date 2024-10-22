import pandas as pd
import matplotlib.pyplot as plt

# Replace 'your_file.csv' with the path to your CSV file
file_path = 'Cornea_Harmonic_Perturbation_2D_Axisymmetric_OldSystem_out_upper_right_z_disp_0001.csv'

# Read the CSV file
data = pd.read_csv(file_path)

# Assuming that the columns are in the order: 1st (y displacement), 3rd (x position)
# You may need to adjust the column indices based on your file structure
y_displacement = data.iloc[:, 0]  # 1st column
# x_position = data.iloc[:, 2]      # 3rd column

# Create equally spaced x values based on the number of y displacements
x_equal = range(len(y_displacement))


# Plot x position vs y displacement
plt.figure(figsize=(8, 6))
plt.plot(x_equal, y_displacement, marker='o', linestyle='-', color='b')

plt.xlabel('equal spacing')
plt.ylabel('Y Displacement')
plt.grid(True)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
filename1 = 'incompressible_neo_hookean_out.csv'  # Replace with your CSV file path
# filename2 = 'compressible_neo_hookean_out.csv'

data1 = pd.read_csv(filename1)
# data2 = pd.read_csv(filename2)

# Extract strain and stress data
strain11_1 = data1.iloc[:, 1]  # 2nd column
stress11_1 = data1.iloc[:, 2]  # 3rd column

# strain11_2 = data2.iloc[:, 1]  # 2nd column
# stress11_2 = data2.iloc[:, 2]  # 3rd column

# Plot the data
plt.figure(figsize=(8, 6))
plt.plot(strain11_1, stress11_1, marker='o', linestyle='-', label='Incompressible Neo-Hookean')
# plt.plot(strain11_2, stress11_2, marker='s', linestyle='--', label='Compressible Neo-Hookean')

# Customize plot
plt.title('Stress xx vs Strain xx')
plt.xlabel('Strain xx')
plt.ylabel('Stress xx')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

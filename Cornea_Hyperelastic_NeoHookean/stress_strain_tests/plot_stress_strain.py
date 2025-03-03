import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
filename1 = 'compressible_neo_hookean_out.csv'
filename2 = 'nearly_incompressible_neo_hookean_out.csv'
filename3 = 'incompressible_neo_hookean_out.csv'

data1 = pd.read_csv(filename1)
data2 = pd.read_csv(filename2)
data3 = pd.read_csv(filename3)

# Extract strain and stress data from each file (assuming the 2nd and 3rd columns)
strain1 = data1.iloc[:, 1]
stress1 = data1.iloc[:, 2]

strain2 = data2.iloc[:, 1]
stress2 = data2.iloc[:, 2]

strain3 = data3.iloc[:, 1]
stress3 = data3.iloc[:, 2]

# Plot the data for all three
plt.figure(figsize=(8, 6))
plt.plot(strain1, stress1, marker='o', linestyle='-', label=r'Compressible Neo-Hookean, $\nu = 0.2$')
plt.plot(strain2, stress2, marker='o', linestyle='-', label=r'Nearly Incompressible Neo-Hookean, $\nu = 0.4999$')
plt.plot(strain3, stress3, marker='o', linestyle='-', label=r'Incompressible Neo-Hookean ($\nu = 0.5$)')

# Customize the plot
plt.title('Stress xx vs Strain xx')
plt.xlabel('Strain xx')
plt.ylabel('Stress xx')
plt.legend()
plt.grid(True)

plt.savefig('stress_strain_neo_hookean')

# Show the plot
plt.show()

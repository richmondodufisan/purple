import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
filename = 'nearly_incompressible_neo_hookean_out.csv'  # Replace with your CSV file path
data = pd.read_csv(filename)

# Extract displacement (2nd column) and force (3rd column)
strain11 = data.iloc[:, 1]  # 2nd column
stress11 = data.iloc[:, 2]         # 3rd column

# Plot the data
plt.figure(figsize=(8, 6))
plt.plot(strain11, stress11, marker='o', linestyle='-')
plt.title('Stress xx vs Strain xx')
plt.xlabel('Strain xx')
plt.ylabel('Stress xx')
plt.grid(True)
plt.show()

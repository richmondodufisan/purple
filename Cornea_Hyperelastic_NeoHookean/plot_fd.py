import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
filename = 'Cornea_Stretch_out.csv'  # Replace with your CSV file path
data = pd.read_csv(filename)

# Extract displacement (2nd column) and force (3rd column)
displacement = data.iloc[:, 1]  # 2nd column
force = data.iloc[:, 2]         # 3rd column

# Plot the data
plt.figure(figsize=(8, 6))
plt.plot(displacement, force, marker='o', linestyle='-')
plt.title('Force vs Displacement')
plt.xlabel('Displacement')
plt.ylabel('Force')
plt.grid(True)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
df = pd.read_csv('Cornea_Harmonic_Perturbation_Steady_freq_1e3_stretch_1.1_out_wave_profile_0001.csv')

# Plot the x column vs the data column
plt.plot(df['x'], df['disp_y'], marker='o', linestyle='-', color='b')

plt.xlabel('x')
plt.ylabel('data')
plt.grid(True)
plt.title('Plot of x vs y disp')

# Show the plot
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# File names
files = [
    ('compressible_neo_hookean_out.csv', r'Compressible, $\nu = 0.2$'),
    ('nearly_incompressible_neo_hookean_out_0_49.csv', r'Nearly Incompressible, $\nu = 0.49$'),
    ('nearly_incompressible_neo_hookean_out_0_499.csv', r'Nearly Incompressible, $\nu = 0.499$'),
    ('nearly_incompressible_neo_hookean_out_0_4999.csv', r'Nearly Incompressible, $\nu = 0.4999$'),
    ('incompressible_neo_hookean_out.csv', r'Incompressible, $\nu = 0.5$')
]

plt.figure(figsize=(8, 6))

# Loop through files and plot
for filename, label in files:
    data = pd.read_csv(filename)
    
    strain = data.iloc[:, 1]
    stress = data.iloc[:, 2]
    
    plt.plot(strain, stress, marker='o', linestyle='-', label=label)

# Customize plot
plt.title('Stress vs Strain for Neo-Hookean Models')
plt.xlabel('Strain')
plt.ylabel('Stress')
plt.legend()
plt.grid(True)

plt.savefig('stress_strain_neo_hookean', dpi=600)

plt.show()
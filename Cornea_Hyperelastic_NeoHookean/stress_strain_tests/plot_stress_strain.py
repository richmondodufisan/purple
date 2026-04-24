import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Geometry / material
l_plate = 0.02      # original length in x
h_plate = 0.002     # original height in y, assuming unit thickness
shear_modulus = 100000.0

plt.figure(figsize=(8, 6))

# Compressible
data = pd.read_csv('compressible_neo_hookean_out.csv')
axial_disp = data.iloc[:, 1]
right_force_x = data.iloc[:, 2]

strain = axial_disp / l_plate
axial_stress = right_force_x / h_plate

plt.plot(strain, axial_stress, marker='o', linestyle='-',
         label=r'Compressible, $\nu = 0.2$')

# # Incompressible
# data = pd.read_csv('incompressible_neo_hookean_out.csv')
# axial_disp = data.iloc[:, 1]
# right_force_x = data.iloc[:, 2]

# strain = axial_disp / l_plate
# axial_stress = right_force_x / h_plate

# plt.plot(strain, axial_stress, marker='o', linestyle='-',
         # label=r'Incompressible, $\nu = 0.5$')

# Analytical incompressible neo-Hookean solution
strain_analytical = np.linspace(0.0, 4.0, 300)
lam = 1.0 + strain_analytical

stress_analytical = shear_modulus * (lam**2 - 1.0 / lam)

plt.plot(strain_analytical, stress_analytical,
         'k--', linewidth=2,
         label='Analytical incompressible')

plt.title('Axial Stress from Reaction Force vs Engineering Strain')
plt.xlabel(r'Engineering Strain, $u_x/L_0$')
plt.ylabel(r'Axial Stress, $F_x/h_0$')
plt.legend()
plt.grid(True)

plt.savefig('stress_strain_neo_hookean.png', dpi=600)
plt.show()
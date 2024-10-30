import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Material properties (update as needed)
E = 210e9           # Young's modulus in Pa
nu = 0.3            # Poisson's ratio
rho = 7800          # Density in kg/m^3
h = 0.001           # Half-thickness of plate in m

# Derived wave speeds
c_L = np.sqrt(E / (rho * (1 - nu**2)))   # Longitudinal wave speed
c_T = np.sqrt(E / (2 * rho * (1 + nu)))  # Shear wave speed

# Frequency range (rad/s)
frequencies = np.linspace(1e3, 1e6, 500)  # Adjust range and resolution as needed

# Rayleigh-Lamb functions for symmetric and antisymmetric modes
def symmetric_mode(k, omega):
    if (omega / c_T)**2 < k**2 or (omega / c_L)**2 < k**2:
        return np.nan  # Skip invalid k values
    p = np.sqrt((omega / c_T)**2 - k**2)
    q = np.sqrt((omega / c_L)**2 - k**2)
    return np.tan(q * h) * np.tan(p * h) + (4 * k**2 * p * q) / (k**2 - q**2)**2

def antisymmetric_mode(k, omega):
    if (omega / c_T)**2 < k**2 or (omega / c_L)**2 < k**2:
        return np.nan  # Skip invalid k values
    p = np.sqrt((omega / c_T)**2 - k**2)
    q = np.sqrt((omega / c_L)**2 - k**2)
    return np.tan(q * h) * (1 / np.tan(p * h)) + (4 * k**2 * p * q) / (k**2 - q**2)**2

# Solve for wavenumber k at each frequency for each mode
wavenumbers_symmetric = []
wavenumbers_antisymmetric = []

for omega in frequencies:
    # Initial guess range for wavenumber k
    k_guess_range = np.linspace(omega / (2 * c_T), omega / c_T, 3)
    
    # Solve for symmetric mode
    k_sym = [fsolve(symmetric_mode, k_guess, args=(omega))[0] for k_guess in k_guess_range]
    k_sym = [k for k in k_sym if k > 0]  # Keep only positive values
    wavenumbers_symmetric.append(min(k_sym) if k_sym else np.nan)

    # Solve for antisymmetric mode
    k_anti = [fsolve(antisymmetric_mode, k_guess, args=(omega))[0] for k_guess in k_guess_range]
    k_anti = [k for k in k_anti if k > 0]  # Keep only positive values
    wavenumbers_antisymmetric.append(min(k_anti) if k_anti else np.nan)

# Convert to arrays for plotting
wavenumbers_symmetric = np.array(wavenumbers_symmetric)
wavenumbers_antisymmetric = np.array(wavenumbers_antisymmetric)

# Plotting the dispersion curves
plt.figure(figsize=(10, 6))
plt.plot(frequencies / (2 * np.pi), wavenumbers_symmetric, label='Symmetric Mode (S)')
plt.plot(frequencies / (2 * np.pi), wavenumbers_antisymmetric, label='Antisymmetric Mode (A)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Wavenumber (1/m)')
plt.title('Rayleigh-Lamb Dispersion Curves')
plt.legend()
plt.grid(True)
plt.show()

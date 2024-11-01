import numpy as np
import cmath
import matplotlib.pyplot as plt

# Material and physical properties
thickness = 0.7387e-3
h_half = thickness / 2
density = 1100
poissons_ratio = 0.4995
shear_modulus = 237.3e3

# Frequency and angular frequency
freq = 1000  
w = 2 * np.pi * freq

# Wave speeds
c_T = np.sqrt(shear_modulus / density)
lame_lambda = (2 * shear_modulus * poissons_ratio) / (1 - (2 * poissons_ratio))
c_L = np.sqrt((lame_lambda + (2 * shear_modulus)) / density)

# Define the dispersion relation function
def D_cp(w, c_T, c_L, c_phase, h):
    k = w / c_phase  # wave number, k

    # Calculate q and p with proper grouping
    q = cmath.sqrt((w**2) / (c_T**2) - k**2)
    p = cmath.sqrt((w**2) / (c_L**2) - k**2)

    # LHS and RHS terms
    LHS_term = cmath.tan(q * h) / cmath.tan(p * h)
    RHS_term = - (4 * (k**2) * p * q) / (((q**2) - (k**2))**2)

    # Dispersion relation D
    D = LHS_term - RHS_term
    return D

# Define range of phase velocities for evaluation
cp_range = np.linspace(0.1, 50, 500)  # From 0.1 to 50 m/s

# Evaluate D_cp for each phase velocity in the range
D_vals = [D_cp(w, c_T, c_L, cp, h_half) for cp in cp_range]

# Extract real, imaginary parts, magnitude, and phase
D_real = [D.real for D in D_vals]
D_imag = [D.imag for D in D_vals]
D_magnitude = [abs(D) for D in D_vals]
D_phase = [cmath.phase(D) for D in D_vals]

# Plot Real and Imaginary Parts
plt.figure(figsize=(10, 6))
plt.plot(cp_range, D_real, label="Real Part of D(cp)", color="blue")
plt.plot(cp_range, D_imag, label="Imaginary Part of D(cp)", color="red")
plt.axhline(0, color="black", linestyle="--", linewidth=0.5)
plt.xlabel("Phase Velocity (m/s)", fontsize=14)
plt.ylabel("D(cp)", fontsize=14)
plt.title("Dispersion Relation D(cp) (Symmetric Modes)", fontsize=16)
plt.legend()
plt.grid(True)
plt.savefig("D_cp_real_imag_sym.png")
plt.show()

# Plot Magnitude of D(cp)
plt.figure(figsize=(10, 6))
plt.plot(cp_range, D_magnitude, label="Magnitude of D(cp)", color="purple")
plt.axhline(0, color="black", linestyle="--", linewidth=0.5)
plt.xlabel("Phase Velocity (m/s)", fontsize=14)
plt.ylabel("|D(cp)|", fontsize=14)
plt.title("Magnitude of Dispersion Relation D(cp) (Symmetric Modes)", fontsize=16)
plt.legend()
plt.grid(True)
plt.savefig("D_cp_magnitude_sym.png")
plt.show()

# Plot Phase of D(cp)
plt.figure(figsize=(10, 6))
plt.plot(cp_range, D_phase, label="Phase of D(cp)", color="green")
plt.axhline(0, color="black", linestyle="--", linewidth=0.5)
plt.xlabel("Phase Velocity (m/s)", fontsize=14)
plt.ylabel("Phase of D(cp) (radians)", fontsize=14)
plt.title("Phase of Dispersion Relation D(cp) (Symmetric Modes)", fontsize=16)
plt.legend()
plt.grid(True)
plt.savefig("D_cp_phase_sym.png")
plt.show()

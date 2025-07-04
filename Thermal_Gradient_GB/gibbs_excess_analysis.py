import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz

# Load temperature data
df = pd.read_csv("Si_Hot_Cold_StepFunction_out_temp_profile_x_0001.csv")
xdata = df["x"].values
Tdata = df["temperature"].values

# Load flux data
flux_df = pd.read_csv("Si_Hot_Cold_StepFunction_out_flux_profile_x_0001.csv")
q_flux = flux_df["q_x"].values[0]  # Use flux at x = 0
x_flux = flux_df["x"].values

# Compute numerical derivative dT/dx
dTdx = np.gradient(Tdata, xdata)
minus_dTdx = -1.0 * dTdx

# Find minimum value and create a constant line
dTdx_min = minus_dTdx[0]
dTdx_const = np.full(len(minus_dTdx), dTdx_min)

# Integrate and subtract to get delta_T
delta_T = trapz(minus_dTdx, x=xdata) - trapz(dTdx_const, x=xdata)

# Compute thermal resistance in m²·K/W
excess_thermal_resistance = delta_T / q_flux


# Define grain boundary width (same unit as xdata, presumably microns or meters)
gb_width = 20.0  # adjust units if needed

# Temperature drop across GB if it were pure bulk
delta_T_bulk = dTdx_min * gb_width

# Total estimated jump (bulk + excess)
delta_T_total = delta_T_bulk + delta_T

# Total thermal resistance
gb_kappa = 56.52
total_thermal_resistance = gb_width/gb_kappa

print("----------------------------------------------------------------------------------------------")

print(f"Heat flux (W/m²): {q_flux:.6f}")
print("\n")
print(f"Bulk temperature gradient: {dTdx_min:.6f}")
print(f"ΔT across GB if finite GB region had same kappa as bulk (K): {delta_T_bulk:.6f}")
print("\n")
print(f"ΔT excess due to reduced kappa of GB (K): {delta_T:.6f}")
print(f"GIBBS EXCESS: Excess Thermal Resistance due to GB (m²·K/W): {excess_thermal_resistance:.8e}")
print("\n")
print(f"Total estimated ΔT across GB (K): {delta_T_total:.6f}")
print("\n")
print(f"T at left end: {Tdata[np.argmin(np.abs(xdata - 50))]:.6f}")
print(f"T at right end: {Tdata[np.argmin(np.abs(xdata - 70))]:.6f}")
print(f"Actual measured ΔT across GB (K): {Tdata[np.argmin(np.abs(xdata - 50))] - Tdata[np.argmin(np.abs(xdata - 70))]:.6f}")
print(f"Total Thermal Resistance (m²·K/W): {total_thermal_resistance:.8e}")
print("----------------------------------------------------------------------------------------------")

plt.rcParams.update({
    "font.size": 16,          # General font size
    "axes.titlesize": 18,     # Title font size
    "axes.labelsize": 16,     # Axis label font size
    "xtick.labelsize": 14,    # Tick font size
    "ytick.labelsize": 14,
    "legend.fontsize": 14,    # Legend font size
    "figure.dpi": 300,        # High-resolution figure
    "savefig.dpi": 600,       # High-resolution save
    "lines.linewidth": 2,     # Thicker lines
    "lines.markersize": 6     # Marker size
})


# Plot Temperature vs x
plt.figure(figsize=(10, 5))
plt.plot(xdata, Tdata, label="Temperature (T)", linewidth=2)
plt.xlabel("x-position")
plt.ylabel("Temperature")
plt.title("Temperature Profile vs. x")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("temperature_v_x.png", dpi = 600)
# plt.show()

# Plot -dT/dx vs x
plt.figure(figsize=(10, 5))
plt.plot(xdata, minus_dTdx, label="-dT/dx", color='orange', linewidth=2)
plt.hlines(dTdx_min, xdata[0], xdata[-1], color='blue', linestyle='--', label="Bulk Gradient")
plt.xlabel("x-position")
plt.ylabel("Temperature Gradient -(dT/dx)")
plt.title("Temperature Gradient vs. x")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("dTdx_gibbs.png", dpi = 600)
# plt.show()

# === Flux Profile Plot ===
# Load flux profile data (assumes it's a 1D profile along x)
flux_df = pd.read_csv("Si_Hot_Cold_StepFunction_out_flux_profile_x_0001.csv")
x_flux = flux_df["x"].values
q_x = flux_df["q_x"].values

plt.figure(figsize=(10, 5))
plt.plot(x_flux, q_x, label="Heat Flux $q_x$", color='green', linewidth=2)
plt.xlabel("x-position")
plt.ylabel("Heat Flux $q_x$ (W/m²)")
plt.title("Heat Flux Profile vs. x")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("flux_profile.png", dpi=600)
# plt.show()




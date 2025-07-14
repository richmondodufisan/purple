import matplotlib.pyplot as plt
import numpy as np


# ISOTROPIC GIBBS EXCESS DATA
# theta_angle = [0, 15, 30, 45, 60, 75]
# theta_angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]

# resistance_2 = [5.562534445054336e-10, 5.372922740407817e-10, 5.4774395170108e-10, 6.690018087595993e-10, 9.272840951673182e-10, 1.4634507460796786e-09] # step function gb, no G fit, 100nm
# resistance_2 = [5.147594847354632e-10, 5.372105293126565e-10, 6.180598706064184e-10, 7.861333358050975e-10, 1.145379143103728e-09, 2.2597610125716646e-09] # step function gb, no G fit, 100nm (finer mesh)
# resistance_2 = [9.223339545500985e-11, 9.544909166825082e-11, 1.0509558647705016e-10, 1.2833918451352638e-10, 1.76925763405763e-10, 3.240058065235056e-10] # step function gb, no G fit, 10nm
# resistance_2 = [2.7404207023421157e-10, 2.74042280308441e-10, 6.520659771127721e-10, 6.52065944818741e-10, 1.2660997835933506e-09, 2.5251999151162495e-09] # perfect interface, no G fit



# Data in Gibbs Excess Paper (ISOTROPIC FIT)
# theta_angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
# resistance_2 = [5.147594846126434e-10, 5.171333042931287e-10, 5.257515183053475e-10, 5.372104739179723e-10, 5.558267334747862e-10, 5.822850608858926e-10, 6.180601742192903e-10, 6.603050331758472e-10, 7.156459553409862e-10, 7.861333085943758e-10, 8.783615309056158e-10, 9.95634466857469e-10, 1.1453791460127568e-09, 1.362245931831531e-09, 1.696072044063303e-09, 2.2597610176826614e-09, 3.368021468439585e-09]
# resistance_2 = [(resistance * 1e9) for resistance in resistance_2]








# ANISOTROPIC GIBBS EXCESS DATA - R COMPONENT
theta_angle_a = [0, 15, 30, 45, 60, 75]


resistance_2a = [4.9291e-10, 5.0751e-10, 5.5724e-10, 6.6759e-10, 9.1679e-10, 1.6335e-09]
resistance_2a = [(resistance * 1e9) for resistance in resistance_2a]




# ANISOTROPIC GIBBS EXCESS DATA - Z COMPONENT
theta_angle_b = [0, 15, 30, 45, 60, 75]


resistance_2b = [3.0834e-10, 3.3876e-10, 4.4007e-10, 6.5782e-10, 1.1420e-09, 2.6852e-09]
resistance_2b = [(resistance * 1e9) for resistance in resistance_2b]








# # Convert theta to radians
# theta_rad = np.radians(theta_angle)

# # Calculate ideal 1/cos(theta) curve, scaled to match the first Gibbs resistance value
# scale_factor = resistance_2[0]  # match the 0° resistance
# ideal_curve = [scale_factor / np.cos(t) for t in theta_rad]




# Smooth analytical-style 1/cos(theta) curve
# theta_smooth_deg = np.linspace(0, 80, 500)  # 500 points from 0 to 80 degrees
# theta_smooth_rad = np.radians(theta_smooth_deg)

# # Scale to match the first resistance value
# scale_factor = resistance_2[0]
# ideal_curve_smooth = scale_factor / np.cos(theta_smooth_rad)





# Calculate the ratio of each resistance value to 1.7e-9
# reference_value = 1.7256681158809706e-09 * 1e9 # through simulations
# reference_value = 1.7699e-09 * 1e9 # calculated
# percent_resistance = [((resistance * 1)/ reference_value) for resistance in resistance_2]





# Compare initial values (theta = 0°)
r0 = resistance_2a[0]
z0 = resistance_2b[0]
ratio_z_to_r = z0 / r0

print(f"Initial resistance at 0°:")
print(f"  r-component: {r0:.4f} m²K/GW")
print(f"  z-component: {z0:.4f} m²K/GW")
print(f"  Ratio z/r: {ratio_z_to_r:.4f}")


# Smooth theta values for plotting
theta_smooth = np.linspace(0, 75, 500)
theta_smooth_rad = np.radians(theta_smooth)

# Scaled 1/cos(theta) curves anchored at theta = 0
r_cos_smooth = resistance_2a[0] / np.cos(theta_smooth_rad)
z_cos_smooth = resistance_2b[0] / np.cos(theta_smooth_rad)


# ----- Set manually -----
alpha = 2.0  # Tune this value to see fit quality
# ------------------------

# Generalized z-component model
z_cos_smooth_alpha = resistance_2b[0] / (np.cos(theta_smooth_rad) ** alpha)



# from scipy.optimize import curve_fit

# # Model: 1 / cos^alpha(theta)
# def model_cos_alpha(theta_deg, alpha):
    # theta_rad = np.radians(theta_deg)
    # return resistance_2b[0] / (np.cos(theta_rad) ** alpha)

# # Fit the alpha parameter
# theta_deg_b = np.array(theta_angle_b)
# res_b = np.array(resistance_2b)
# popt, _ = curve_fit(model_cos_alpha, theta_deg_b, res_b, p0=[2.0])
# alpha_fit = popt[0]
# print(f"Best-fit alpha for z-component: {alpha_fit:.4f}")

from scipy.optimize import curve_fit

# Model: 1 / cos^alpha(theta)
def model_cos_alpha(theta_deg, alpha):
    theta_rad = np.radians(theta_deg)
    return resistance_2b[0] / (np.cos(theta_rad) ** alpha)

# Use only the first 4 points for the fit (0°, 15°, 30°, 45°)
theta_deg_b_subset = np.array(theta_angle_b[:4])
res_b_subset = np.array(resistance_2b[:4])

# Fit alpha to the subset
popt, _ = curve_fit(model_cos_alpha, theta_deg_b_subset, res_b_subset, p0=[2.0])
alpha_fit = popt[0]

#MANUAL ALPHA
alpha_fit = 2.0

print(f"Best-fit alpha (first 4 points only): {alpha_fit:.4f}")

















# Plot
fig, ax1 = plt.subplots()

# Primary y-axis
# ax1.plot(theta_angle, resistance_2, marker='o', linestyle='--', color='blue', label="Gibbs Excess")


# ax1.plot(theta_angle_a, resistance_2a, marker='o', linestyle='--', color='red', label="Gibbs Excess (r component)")
ax1.plot(theta_angle_b, resistance_2b, marker='o', linestyle='--', color='purple', label="Gibbs Excess (z component)")



# ax1.plot(theta_smooth, r_cos_smooth, linestyle=':', color='red', alpha=0.6, label=r"$\propto 1/\cos(\theta)$")    # r component
ax1.plot(theta_smooth, z_cos_smooth, linestyle=':', color='purple', alpha=0.6, label=r"$\propto 1/\cos(\theta)$")   # z component



# Plot updated z fit with alpha
# ax1.plot(theta_smooth, z_cos_smooth_alpha, linestyle=':', color='green', alpha=0.6, label=fr"Scaled $1/\cos^{{{alpha}}}(\theta)$ (z, anchored at $0^\circ$)")

z_cos_smooth_alpha = resistance_2b[0] / (np.cos(theta_smooth_rad) ** alpha_fit)
ax1.plot(theta_smooth, z_cos_smooth_alpha, linestyle='-.', color='purple', alpha=0.5, label=fr"$\propto 1/\cos^{{{alpha_fit:.2f}}}(\theta)$")




# ax1.plot(theta_angle, ideal_curve, linestyle='-', color='gray', label=r"$\propto 1/\cos(\theta)$")
# ax1.plot(theta_smooth_deg, ideal_curve_smooth, linestyle='-', color='black', label=r"$\propto 1/\cos(\theta)$")


ax1.set_xlabel('Angle Between GB Plane and Vertical ($\\theta$)', fontsize=12)
ax1.set_ylabel('Excess Boundary Resistance, $R_{gibbs}$ ($\mathrm{m}^2\mathrm{K/GW}$)', fontsize=12)
ax1.tick_params(axis='y', labelsize=12)
ax1.tick_params(axis='x', labelsize=12)


# ax1.set_title("GB Tilt Angle vs Resistance, R Component")
ax1.set_title("GB Tilt Angle vs Resistance, Z Component")

# ax1.set_ylim(0, 1.5*reference_value)

# Horizontal line at Kapitza Resistance
# plt.axhline(y=reference_value, color='black', linestyle='-', label=f'Thermal Boundary Resistance (TBR)')

# Secondary y-axis for ratio
# ax2 = ax1.twinx()
# ax2.plot(theta_angle, percent_resistance, marker='s', linestyle='-', color='red', label="Gibb's Excess/Kapitza Ratio")
# ax2.set_ylabel('$R_B$/TBR', color='red', fontsize=12)
# ax2.tick_params(axis='y', labelcolor='red', labelsize=12)
# ax2.set_ylim(0, 1.5)


# Show legends for both lines
# lines1, labels1 = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=12)


ax1.legend(loc='upper left', fontsize=12)


plt.grid(True)
# plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION.png", bbox_inches='tight', dpi=600)
# plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION_anisotropic_r.png", bbox_inches='tight', dpi=600)

plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION_anisotropic_z.png", bbox_inches='tight', dpi=600)


# plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION_anisotropic_BOTH.png", bbox_inches='tight', dpi=600)
plt.show()



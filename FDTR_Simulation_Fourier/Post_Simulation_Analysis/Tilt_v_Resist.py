import matplotlib.pyplot as plt

# Data
theta_angle = [0, 15, 30, 45, 60, 75]
resistance_2 = [5.562534445054336e-10, 5.372922740407817e-10, 5.4774395170108e-10, 6.690018087595993e-10, 9.272840951673182e-10, 1.4634507460796786e-09] # step function data, no G fit
resistance_2 = [(resistance * 1e9) for resistance in resistance_2]

# Calculate the ratio of each resistance value to 1.7e-9
reference_value = 1.7256681158809706e-09 * 1e9
percent_resistance = [((resistance * 1)/ reference_value) for resistance in resistance_2]

# Plot
fig, ax1 = plt.subplots()

# Primary y-axis
ax1.plot(theta_angle, resistance_2, marker='o', linestyle='--', color='blue', label="Gibbs Excess")
ax1.set_xlabel('Angle Between GB Plane and Vertical ($\\theta$)', fontsize=12)
ax1.set_ylabel('Excess Boundary Resistance, $R_B$ ($\mathrm{m}^2\mathrm{K/GW}$)', color='blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='blue', labelsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax1.set_ylim(0, 1.1*reference_value)

# Horizontal line at Kapitza Resistance
plt.axhline(y=reference_value, color='black', linestyle='-', label=f'Thermal Boundary Resistance (TBR)')

# Secondary y-axis for ratio
ax2 = ax1.twinx()
# ax2.plot(theta_angle, percent_resistance, marker='s', linestyle='-', color='red', label="Gibb's Excess/Kapitza Ratio")
ax2.set_ylabel('$R_B$/TBR', color='red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red', labelsize=12)
ax2.set_ylim(0, 1.1)


# Show legends for both lines
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='lower left', fontsize=12)

plt.grid(False)
plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION.png", bbox_inches='tight')
plt.show()



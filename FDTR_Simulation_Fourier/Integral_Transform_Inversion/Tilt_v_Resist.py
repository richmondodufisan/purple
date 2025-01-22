import matplotlib.pyplot as plt

# Data
# theta_angle = [0, 15, 30, 45, 60, 75]
theta_angle = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]


# resistance_2 = [5.562534445054336e-10, 5.372922740407817e-10, 5.4774395170108e-10, 6.690018087595993e-10, 9.272840951673182e-10, 1.4634507460796786e-09] # step function gb, no G fit, 100nm
# resistance_2 = [5.147594847354632e-10, 5.372105293126565e-10, 6.180598706064184e-10, 7.861333358050975e-10, 1.145379143103728e-09, 2.2597610125716646e-09] # step function gb, no G fit, 100nm (finer mesh)
# resistance_2 = [9.223339545500985e-11, 9.544909166825082e-11, 1.0509558647705016e-10, 1.2833918451352638e-10, 1.76925763405763e-10, 3.240058065235056e-10] # step function gb, no G fit, 10nm
# resistance_2 = [2.7404207023421157e-10, 2.74042280308441e-10, 6.520659771127721e-10, 6.52065944818741e-10, 1.2660997835933506e-09, 2.5251999151162495e-09] # perfect interface, no G fit

resistance_2 = [5.147594846126434e-10, 5.171333042931287e-10, 5.257515183053475e-10, 5.372104739179723e-10, 5.558267334747862e-10, 5.822850608858926e-10, 6.180601742192903e-10, 6.603050331758472e-10, 7.156459553409862e-10, 7.861333085943758e-10, 8.783615309056158e-10, 9.95634466857469e-10, 1.1453791460127568e-09, 1.362245931831531e-09, 1.696072044063303e-09, 2.2597610176826614e-09, 3.368021468439585e-09]

resistance_2 = [(resistance * 1e9) for resistance in resistance_2]



# Calculate the ratio of each resistance value to 1.7e-9
reference_value = 1.7256681158809706e-09 * 1e9 # through simulations
reference_value = 1.7699e-09 * 1e9 # calculated
percent_resistance = [((resistance * 1)/ reference_value) for resistance in resistance_2]

# Plot
fig, ax1 = plt.subplots()

# Primary y-axis
ax1.plot(theta_angle, resistance_2, marker='o', linestyle='--', color='blue', label="Gibbs Excess")
ax1.set_xlabel('Angle Between GB Plane and Vertical ($\\theta$)', fontsize=12)
ax1.set_ylabel('Excess Boundary Resistance, $R_B$ ($\mathrm{m}^2\mathrm{K/GW}$)', color='blue', fontsize=12)
ax1.tick_params(axis='y', labelcolor='blue', labelsize=12)
ax1.tick_params(axis='x', labelsize=12)
ax1.set_ylim(0, 1.5*reference_value)

# Horizontal line at Kapitza Resistance
# plt.axhline(y=reference_value, color='black', linestyle='-', label=f'Thermal Boundary Resistance (TBR)')

# Secondary y-axis for ratio
ax2 = ax1.twinx()
# ax2.plot(theta_angle, percent_resistance, marker='s', linestyle='-', color='red', label="Gibb's Excess/Kapitza Ratio")
ax2.set_ylabel('$R_B$/TBR', color='red', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red', labelsize=12)
ax2.set_ylim(0, 1.5)


# Show legends for both lines
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=12)

plt.grid(False)
plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION.png", bbox_inches='tight')
plt.show()



import matplotlib.pyplot as plt

# Data
theta_angle = [0, 15, 30, 45, 60, 75]

resistance_1 = [4.763770770058843e-10, 5.174270320521943e-10, 5.10775202795518e-10, 6.339480079165826e-10, 7.849171867503634e-10, 1.2769060616705319e-09] # step function data, G fit

resistance_2 = [5.562534445054336e-10, 5.372922740407817e-10, 5.4774395170108e-10, 6.690018087595993e-10, 9.272840951673182e-10, 1.4634507460796786e-09] # step function data, no G fit

# Plot
# plt.plot(theta_angle, resistance_1, marker='o', linestyle='--', color='red', label='G fit')
plt.plot(theta_angle, resistance_2, marker='o', linestyle='--', color='blue', label='no G fit')
plt.xlabel('Theta Angle')
plt.ylabel('Resistance')
plt.title('Resistance vs GB Tilt Theta Angle')
# plt.legend()
plt.grid(True)
plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION.png", bbox_inches='tight')
plt.show()

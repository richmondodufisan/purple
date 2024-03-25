import matplotlib.pyplot as plt

# Data
theta_angle = [0, 15, 30, 45, 60, 75]
resistance = [4.763770770058843e-10, 5.174270320521943e-10, 5.10775202795518e-10, 6.339480079165826e-10, 7.849171867503634e-10, 1.2769060616705319e-09] # step function data

# Plot
plt.plot(theta_angle, resistance, marker='o', linestyle='--', color='black')
plt.xlabel('Theta Angle')
plt.ylabel('Resistance')
plt.title('Resistance vs GB Tilt Theta Angle')
plt.grid(True)
plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION.png", bbox_inches='tight')
plt.show()

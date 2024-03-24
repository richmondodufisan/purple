import matplotlib.pyplot as plt

# Data
theta_angle = [0, 15, 30, 45, 60, 75]
resistance = [4.760895712670932e-10, 5.17110760479262e-10, 5.104661897101203e-10, 6.335612711254261e-10, 7.844436841757302e-10, 1.276142387997209e-09] # step function data

# Plot
plt.plot(theta_angle, resistance, marker='o', linestyle='--', color='black')
plt.xlabel('Theta Angle')
plt.ylabel('Resistance')
plt.title('Resistance vs GB Tilt Theta Angle')
plt.grid(True)
plt.savefig(f"Tilt_v_Resist_STEP_FUNCTION.png", bbox_inches='tight')
plt.show()

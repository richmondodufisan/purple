from Two_Layer_Phase import calc_thermal_response
import matplotlib.pyplot as plt
import numpy as np

freq = 1 # in MHz
kappa = 130 # in W/(m.K)
conductance = 3e7 # in W/(m2.K)

################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################

# Define other parameters required by calc_thermal_response function
N_layers = 2
layer2 = [40e-6, kappa, kappa, 2329, 689.1]
layer1 = [133e-9, 215, 215, 19300, 128.7]
layer_props = np.array([layer2, layer1])
interface_props = [conductance]
r_probe = 1.34e-6
r_pump = 1.53e-6
pump_power = 0.01
freq = freq * 1e6

# Calculate analytical phase 
phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, freq, pump_power)

print("----------------------------------------------------------------------------------------------")
print("Phase: " + str(phase)) 
print("Amplitude: " + str(amplitude)) 
print("----------------------------------------------------------------------------------------------")

################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################
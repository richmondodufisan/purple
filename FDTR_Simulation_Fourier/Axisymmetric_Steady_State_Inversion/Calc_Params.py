# from Two_Layer_Inversion_Concentric import calc_thermal_response
# from Two_Layer_Inversion_BesselRing import calc_thermal_response
# from Two_Layer_Inversion_SuperGaussianRing import calc_thermal_response
from Two_Layer_Inversion_Traditional_Concentric import calc_thermal_response
import matplotlib.pyplot as plt
import numpy as np

freq = 1.0 # in MHz
kappa = 130.0 # in W/(m.K)
conductance_12 = 30e6 # in W/(m2.K)
conductance_23 = 30e6 # in W/(m2.K)


################################### CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################

# Define other parameters required by calc_thermal_response function
N_layers = 2
layer2 = [40e-6, kappa, kappa, 2329, 689.1]
layer1 = [90e-9, 215, 215, 19300, 128.7]
layer_props = np.array([layer2, layer1])
interface_props = [conductance_12]
w_probe = 1.34e-6
w_pump = 1.53e-6
pump_power = 0.01
freq = freq * 1e6

offset = 3e-6

order = 2.0

si_distance = 1e-6
gb_thickness = 0.01e-6
gb_kappa = 56.52

# Calculate analytical phase 
# phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, freq, pump_power)
# phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, freq, pump_power)
# phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, offset, order, freq, pump_power)

phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, w_pump, w_probe, freq, pump_power, gb_kappa, gb_thickness, si_distance)

print("----------------------------------------------------------------------------------------------")
print("Phase: " + str(phase)) 
print("Amplitude: " + str(amplitude)) 
print("----------------------------------------------------------------------------------------------")

# ################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################




################################## CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################

# # Define other parameters required by calc_thermal_response function
# N_layers = 3
# layer3 = [39.91e-6, kappa, kappa, 2329, 689.1]
# layer2 = [90e-9, kappa, kappa, 2329, 689.1]
# layer1 = [90e-9, 215, 215, 19300, 128.7]
# layer_props = np.array([layer3, layer2, layer1])
# interface_props = [conductance_23, conductance_12]
# r_probe = 1.34e-6
# r_pump = 1.53e-6
# pump_power = 0.01
# freq = freq * 1e6

# # Calculate analytical phase 
# phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, freq, pump_power)

# print("----------------------------------------------------------------------------------------------")
# print("Phase: " + str(phase)) 
# print("Amplitude: " + str(amplitude)) 
# print("----------------------------------------------------------------------------------------------")

################################## END CALCULATE PHASE AND AMPLITUDE FOR A SINGLE FREQUENCY #####################################
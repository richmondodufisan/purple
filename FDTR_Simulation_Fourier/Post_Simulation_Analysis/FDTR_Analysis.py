import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Layered_Heat_Conduction import calc_thermal_response
from Phase_Extraction_Maxima import calculate_phase_amplitude

N_layers = 2

layer2 = [40e-6, 130, 130, 2329, 689.1]
layer1 = [9e-8, 215, 215, 19300, 128.7]

layer_props = np.array([layer2, layer1])

interface_props = [3e7]

r_probe = 1.34e-6
r_pump = 1.53e-6

#calib_consts = [0.9735, 0.997]
calib_consts = [1, 1]

pump_power = 0.01

freq = 1e6

phase, amplitude = calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, calib_consts, freq, pump_power)

print(phase)
print(amplitude)

FDTR_data = pd.read_csv('./Fourier_Standard_Medium.csv', skiprows=1, header=None, usecols=[2, 3])
FDTR_data.columns = ['time', 'temp']

phase2, amplitude2 = calculate_phase_amplitude(FDTR_data, 75)

print(phase2)
print(amplitude2)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import pdb

# This is a helper file for finding the phase difference from time domain data in an FDTR experiment
# It works by finding the time lag between the maxima of the pump and probe signals

# Define a function to extract subframes based on ranges
def extract_subframes(df, start_value, end_value):

    # subtract the start/end value from every entry in the dataframe
    # find the absolute value of that difference
    # find the position of the minimum difference, i.e the position of the entry closest to the start/end value
    start_time = df['time'].sub(start_value).abs().idxmin()
    end_time = df['time'].sub(end_value).abs().idxmin()
    return df.loc[start_time:end_time]
    
    
def calculate_phase_amplitude(simulation_data, end_period, freq):
    end_period = end_period/freq
    begin_period = end_period - (1/freq)
    FDTR_subframe = extract_subframes(simulation_data, begin_period, end_period)
    
    # Separate time and temperature data
    time_array = np.array(FDTR_subframe['time'])
    temp_array = np.array(FDTR_subframe['temp'])
    
    # Define your fitting function
    def fitting_func(t, A, phi, C):
      return A - (A * np.cos(2 * np.pi * freq * t + phi)) + C

    # Define a pump function of the same form as that used in simulations
    # Amplitude of this function does not matter
    def pump_func(t):
      return 5*(1 - np.cos(2* np.pi * freq * t))
      
    # Perform curve fitting
    initial_guess = [10, 0, 0]  # Initial guess for the parameters A and phi
    params, covariance = curve_fit(fitting_func, time_array, temp_array, p0=initial_guess, maxfev=1000)

    # Extract fitted parameters
    A, phi, C = params

    # Define an incredibly fine array that has same time length as fitting time
    # by making the simulation time discretization 5000 times finer
    dt = time_array[1] - time_array[0]
    ddt = dt/5000
    fine_time = np.arange(time_array[0], time_array[-1], ddt)

    # find corresponding pump and probe values for the time array defined
    probe_vals = fitting_func(fine_time, A, phi, C)
    pump_vals = pump_func(fine_time)

    # find maxima of pump and probe- these are used to find phase difference
    max_index_probe = np.argmax(probe_vals)
    max_index_pump = np.argmax(pump_vals)

    # Phase = time difference * (1/period) * 2 * pi
    phase = (fine_time[max_index_pump] - fine_time[max_index_probe]) * freq * 2 * np.pi

    # Amplitude = max_value - min_value
    amplitude = probe_vals[max_index_probe] - probe_vals[0]
    
    # plt.scatter(FDTR_subframe['time'], FDTR_subframe['temp'])
    # plt.plot(fine_time, probe_vals, 'r')
    # plt.scatter(fine_time[max_index_probe], probe_vals[max_index_probe], color='r', label='probe')
    # plt.plot(fine_time, pump_vals, color='green')
    # plt.scatter(fine_time[max_index_pump], pump_vals[max_index_pump], label='pump', color='green')
    # plt.legend()
    # plt.show()
    
    return phase, amplitude
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# This is a helper file for finding the phase difference from time domain data in an FDTR experiment
# It works by fitting an expression similar to the pump signal with a phase lag

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
      
    # Perform curve fitting
    initial_guess = [10, 0, 0]  # Initial guess for the parameters A and phi
    params, covariance = curve_fit(fitting_func, time_array, temp_array, p0=initial_guess, maxfev=1000)

    # Extract fitted parameters
    A, phi, C = params

    # Phase = time difference * (1/period) * 2 * pi
    phase = phi

    # Amplitude = 2 * fitted amplitude (which calculates amplitude as "half" of wave)
    amplitude = A * 2.0
    
    # fitted_curve = fitting_func(FDTR_subframe['time'], A, phi, C)
    # plt.scatter(FDTR_subframe['time'], FDTR_subframe['temp'], label='Original Data')
    # plt.plot(FDTR_subframe['time'], fitted_curve, 'r', label='Fitted Curve')
    # plt.xlabel('Time')
    # plt.ylabel('Temperature')
    # plt.legend()
    # plt.show()
    
    return phase, amplitude
import os
import math
import csv
import re
import numpy as np

x_vals = [0, 1]
y_vals = [0, 1]
frequencies = [1e6, 2e6]

# Sort for consistent indexing
x_vals.sort()
y_vals.sort()

for freq in frequencies:
    phase_map = np.zeros((len(y_vals), len(x_vals)))  # rows = y, cols = x

    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):

            temp_file = f"FDTR_input_GibbsExcess_StepFunction_Concentric_Test_Data_Fourier_Steady_freq_{int(freq/1e6)}e6_x0_{x}_y0_{y}.i"

            output_csv = temp_file.replace(".i", "_out.csv")

            try:
                with open(output_csv, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    next(csv_reader)  # Skip header
                    rows = list(csv_reader)
                    last_row = rows[-1]
                    H_imag = float(last_row[1])
                    H_real = float(last_row[2])

                    # Phase in degrees
                    phase = math.degrees(math.atan2(H_imag, H_real))
                    phase_map[i, j] = phase

            except Exception as e:
                print(f"Error reading output for x={x}, y={y}, freq={freq}: {e}")
                phase_map[i, j] = np.nan  # Fill with NaN if error

    # Save to file
    out_filename = f"Phase_{int(freq/1e6)}MHz.txt"
    np.savetxt(out_filename, phase_map, fmt="%.6f")
    print(f"Saved phase map to {out_filename}")

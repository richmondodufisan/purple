import os
import math
import csv
import re
import numpy as np

# Configuration
x_vals = [-18, -15, -12, -9, -6, -3, 0, 3, 6, 9, 12, 15, 18]
y_vals = [-18, -15, -12, -9, -6, -3, 0, 3, 6, 9, 12, 15, 18]
frequencies = [2e6, 4e6, 6e6, 8e6, 10e6]
input_file = "FDTR_input_GibbsExcess_StepFunction_Concentric.i"

# Sort for consistent indexing
x_vals.sort()
y_vals.sort()

for freq in frequencies:
    phase_row = np.zeros(len(x_vals))  # Only simulate along x for y = 0

    for j, x in enumerate(x_vals):
        temp_file = f"temp_input_freq_{int(freq/1e6)}MHz_x_{x}_y_0.i"

        replacements = {
            'freq_val': freq,
            'x0_val': x,
            'y0_val': 0  # fixed y position
        }

        with open(input_file, 'r') as file:
            lines = file.readlines()

        with open(temp_file, 'w') as file:
            replaced_keys = set()
            for line in lines:
                for key, value in replacements.items():
                    if key in line and key not in replaced_keys:
                        line = re.sub(rf"{key} = \S+", f"{key} = {value}", line, count=1)
                        replaced_keys.add(key)
                file.write(line)

        # Run simulation
        os.system(f"../../purple-opt -i {temp_file} > output_log.txt 2>&1")
        output_csv = temp_file.replace(".i", "_out.csv")

        try:
            with open(output_csv, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip header
                rows = list(csv_reader)
                last_row = rows[-1]
                H_imag = float(last_row[1])
                H_real = float(last_row[2])

                phase = math.degrees(math.atan2(H_imag, H_real))
                phase_row[j] = phase

        except Exception as e:
            print(f"Error reading output for x={x}, y=0, freq={freq}: {e}")
            phase_row[j] = np.nan

    # Duplicate the x-scan across all y to form a full phase map
    phase_map = np.tile(phase_row, (len(y_vals), 1))

    # Save the phase map
    out_filename = f"Phase_{int(freq/1e6)}MHz.txt"
    np.savetxt(out_filename, phase_map, fmt="%.6f")
    print(f"Saved phase map to {out_filename}")
